import logging
import os
from pprint import pprint

from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt
from flask import (Flask, abort, make_response, redirect,
                   render_template_string, request, session, url_for)
from omegaconf import OmegaConf

app = Flask(__name__)

# If started by Gunicorn
if "gunicorn" in os.environ.get("SERVER_SOFTWARE", ""):
    # Set Logging
    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_error_logger.handlers
    app.logger.setLevel(gunicorn_error_logger.level)

    app.logger.info("Gunicorn Detected. Starting with additional configuration.")

    # Proxy Fix for use with Ingress Controller
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.logger.warning('ProxyFix is enabled. \
X_Forwarded_For, X_Host, X_Proto are used to determine clients information. \
ONLY USE THIS WITH A PROXY!')
    app.wsgi_app = ProxyFix(app.wsgi_app , x_proto=1, x_host=1, x_for=1)

    # Gunicorn Metrics
    from prometheus_flask_exporter.multiprocess import \
        GunicornPrometheusMetrics
    metrics = GunicornPrometheusMetrics(app)

# If not started with gunicorn
else:
    from prometheus_flask_exporter import PrometheusMetrics
    metrics = PrometheusMetrics(app)

# Load YAML Configuration
config = OmegaConf.load('config.yaml')

# Set Flask Config
app.secret_key = config["secretkey"]
app.config.update(
    AZUREAD_CLIENT_ID = config["azuread"]["client_id"],
    AZUREAD_CLIENT_SECRET = config["azuread"]["client_secret"]
)

# Configure Azure OpenID Connect
oauth = OAuth(app)
oauth.register(
    name='azuread',
    server_metadata_url= config["azuread"]["openid_connect_url"],
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/<site>')
def login(site):
    if site not in config['sites']:
        abort(404)

    redirect_uri = url_for('auth', _external=True)
    resp = make_response(oauth.azuread.authorize_redirect(redirect_uri))
    session['site'] = site
    session['location'] = request.args.get('location', '')
    return resp


@app.route('/auth')
def auth():
    site = session.get('site')
    location = session.get('location')
    if not site:
        abort(400)

    if site not in config['sites']:
        abort(404)

    token = oauth.azuread.authorize_access_token()
    user = oauth.azuread.parse_id_token(token, None)
    preferred_username = user["preferred_username"].lower()

    usergroup_set = set(user['groups'] or [])
    sitegroup_set = set(config['sites'][site]['groups'] or [])
    allowed_users = config['sites'][site]['users'] or []
    if not (len(usergroup_set.intersection(sitegroup_set)) > 0 or preferred_username in allowed_users):
        abort(403, description=f"User {preferred_username} has no read access to space {site}.")

    header = {'alg': 'HS256'}
    payload = {
        'iss': 'Gitbook Visitor Authenticator',
        'exp': user['exp'], # Use AzureAD token expiry & issuing date
        'iat': user['iat']  #
    }
    key = config['sites'][site]['key']
    gitbooktoken = jwt.encode(header, payload, key).decode("utf-8")

    redirecturl = f"{config['sites'][site]['url']}/{location}?jwt_token={gitbooktoken}"

    return redirect(redirecturl)

@app.route("/healthz")
def healthz():
    return "ok"

@app.errorhandler(403)
def page_not_found(e):
    pprint(e)
    return render_template_string(
"""
<h1>Forbidden</h1>
<p>{{ error }}
<p>Please contact {{ contact_email }} to request access.
""", error=e, contact_email=config['contact_email']), 403
