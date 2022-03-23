# GitBook Visitor Authenticator (AzureAD)

Used to authenticate and authorize AzureAD users to GitBook Spaces with the Visitor Authenticator Feature.

## Workflow

1. User enters GitBook documentation site.
2. GitBook redirects to this service via the "Fallback URL".
3. We redirect to Azure AD and authenticate our users.
4. After successful authentication we authorize the users according to the config.yaml
5. After successful authorization we sign a JWT token with the GitBook Signing Key specified in the config.yaml
6. We redirect the user back to GitBook with the JWT token according to the GitBook Space URL defined in the config.yaml

## Configuration

Configuration is done via the config.yaml inside the same directory.

Inside the config.yaml its possible to use Environment Variables. You can use this for secrets, for example.

You can see an example here:

```yaml
secretkey: ${env:FLASK_SECRET}                       # Secret Key Used for Session Cookie Signing
contact_email: some@mail.com                         # Configure this email for Error Messages (ex. 403)
azuread:
  client_id: 12345678-1234-abcd-1234-123abc456efg    # Azure AD Client ID
  client_secret: ${env:AZUREAD_SECRET}               # Azure AD Client Secret
  openid_connect_url: https://login.microsoftonline.com/blabla/v2.0/.well-known/openid-configuration
                                                     # Open ID Connect URL from you Azure AD App
sites:
  visitor-auth-test:
    url: https://docs.swisstxt.ch/visitor-auth-test  # URL of GitBook Space
    key: ${env:GITBOOK_KEY_VISITOR_AUTH_TEST}        # Key provided by GitBook Visitor Authentication Feature
    groups:
    - STXT-G-CloudDev                                # Security Groups that are allowed as Readers
    users:
    - joshua.huegli@swisstxt.ch                      # Preferred Usernames (E-Mails) that are allowed as Readers
```

## Development

To use this you need to have Python 3.8 and Pipenv installed.

Install the projects requirement inside a virtualenv with Pipenv:

```bash
pipenv install --dev
```

Jump into the virutalenv with:

```bash
pipenv shell
```

Create a `config.yaml` inside the apps directory and run the application:

```bash
FLASK_ENV=development FLASK_APP=server flask run
```

## Build & Publish

Build & Publish is done automatically with GitHub Actions.
