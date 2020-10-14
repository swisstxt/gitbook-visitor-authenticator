# Gitbook Visitor Authenticator

Used to authenticate users to GitBook Spaces with the Visitor Authenticator Feature.

## Workflow

1. User enters GitBook documentation site.
2. GitBook redirects to this service via the "Fallback URL".
3. We redirect to Azure AD and authenticate our users.
4. After successful authentication we authorize the users according to the config.yaml
5. After successful authorization we sign a JWT token with the GitBook Signging Key specified in the config.yaml
6. We redirect the user back to GitBook with the JWT token according to the Gitbook Space URL definied in the config.yaml

## Configuration

Configuration is done via the config.yaml inside the same directory.

Inside the config.yaml its possible to use Environment Variables. You can use this for secrets, for example.

You can see an example here:

```yaml
secretkey: ${env:FLASK_SECRET}                       # Secret Key Used for Session Cookie Signing
azuread:
  client_id: 808d5624-6529-408b-a3cd-ba3d6db76f55    # Azure AD Client ID
  client_secret: ${env:AZUREAD_SECRET}               # Azure AD Client Secret
  openid_connect_url: https://login.microsoftonline.com/blabla/v2.0/.well-known/openid-configuration
                                                     # Open ID Connect URL from you Azure AD App
sites:
  visitor-auth-test:
    url: https://docs.swisstxt.ch/visitor-auth-test  # URL of GitBook Space
    key: ${env:GITBOOK_KEY_VISITOR_AUTH_TEST}        # Key provided by GitBook Visitor Authentication Feature
    groups:
    - STXT-G-CloudDev                                # Security Groups that are allowed as Readers
```

## Build & Publish

```shell
docker build -t docker.swisstxt.ch/gitbook-visitor-authenticator:$(git describe --tags --always)
docker push docker.swisstxt.ch/gitbook-visitor-authenticator:$(git describe --tags --always)
```
