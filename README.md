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

The default config is only an example and needs to be customized for your environment. You can do this via environment variables, which also makes it suitable for injecting Kubernetes secrets.

Use the `${env:ENVIRONMENT_VARIABLE_NAME}` construct for this purpose.

With the default config, you need to override the following variables:

* **FLASK_SECRET**: Secret Key Used for Session Cookie Signing
* **NOTIFICATION_MAIL**: Configure this email for Error Messages (ex. 403)
* **AZUREAD_CLIENT_ID**: Azure AD Client ID
* **AZUREAD_SECRET**: Azure AD Client Secret
* **AZUREAD_OPENID_URL**: Open ID Connect URL from you Azure AD App
* **GITBOOK_SPACE_URL**: URL of GitBook Space
* **GITBOOK_KEY**: Key provided by GitBook Visitor Authentication Feature

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

```shell
docker build . -t docker.swisstxt.ch/gitbook-visitor-authenticator:$(git describe --tags --always)
docker push docker.swisstxt.ch/gitbook-visitor-authenticator:$(git describe --tags --always)
```
