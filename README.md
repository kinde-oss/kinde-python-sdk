# Kinde Python SDK

The Kinde SDK for Python.

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com) [![Kinde Docs](https://img.shields.io/badge/Kinde-Docs-eee?style=flat-square)](https://kinde.com/docs/developer-tools) [![Kinde Community](https://img.shields.io/badge/Kinde-Community-eee?style=flat-square)](https://thekindecommunity.slack.com)

## What you need

- Kinde Python SDK supports Python 3.7+
- A Kinde account - [register for free here](https://app.kinde.com/register) (no credit card required)
- A Kinde domain - you get this when you register, e.g. `yourdomain.kinde.com`

## Get started

### Install

Install [PIP](https://pip.pypa.io/en/stable/installation/) and then execute the following command:

```bash
pip install kinde-python-sdk
```

### Set callback URLs

1. In Kinde, go to **Settings > Applications > [Your app] > View details**. 
2. Add your callback URLs in the relevant fields. For example:
    - Allowed callback URLs (also known as redirect URIs) - for example, `http://localhost:8000/callback`
    - Allowed logout redirect URLs - for example, `http://localhost:8000`
3. Select **Save**.

### Add environments

Kinde comes with a production environment, but you can set up other environments if you want to. Note that each environment needs to be set up independently, so you need to use the Environment subdomain in the code block above for those new environments.

## Configure your app

**Environment variables**

The following variables need to be replaced in the code snippets below.

- `KINDE_HOST` - your Kinde domain, e.g. `https://yourdomain.kinde.com`
- `KINDE_CLIENT_ID` - In Kinde, go to **Settings > Applications > [your application] > View details**.
- `KINDE_CLIENT_SECRET` - In Kinde, go to **Settings > Applications > [your application] > View details**.
- `KINDE_REDIRECT_URL` - your callback urls or redirect URIs, e.g. `http://localhost:8000/callback`
- `KINDE_POST_LOGOUT_REDIRECT_URL` - where you want users to be redirected to after signing out, e.g. `http://localhost:8000`

## Integrate with your app

Create a new instance of the Kinde Auth client object before you initialize your app.

```python
...
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
...

configuration = Configuration(host=KINDE_HOST)
kinde_api_client_params = {
    "configuration": configuration,
    "domain": KINDE_HOST,
    "client_id": KINDE_CLIENT_ID,
    "client_secret": KINDE_CLIENT_SECRET,
    "grant_type": GrantType.AUTHORIZATION_CODE, 
    "callback_url": KINDE_REDIRECT_URL
}
kinde_client = KindeApiClient(**kinde_api_client_params)
```

Other valid values for `grant_type` are:

- `GrantType.AUTHORIZATION_CODE_WITH_PKCE`
- `GrantType.CLIENT_CREDENTIALS`

With **PKCE** flow, the `code_verifier` is required.

```python
from authlib.common.security import generate_token
CODE_VERIFIER = generate_token(48)
kinde_api_client_params["code_verifier"] = CODE_VERIFIER
```

### Sign in and sign up

The Kinde client provides methods for easy sign in and sign up. You can add buttons in your HTML as follows:

```html
<div class="navigation">
		<a href="{{ url_for('login') }}" type="button">Login</a>
		<a href="{{ url_for('register') }}" type="button">Register</a>
</div>
```

You will also need to route `/login` and `/register` to the SDK methods:

```python
@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.get_login_url())

@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.get_register_url())
```

### Manage redirects

When the user is redirected back to your site from Kinde, this will call your callback URL defined in the `KINDE_REDIRECT_URL` variable. You will need to route `/callback` to call a function to handle this.

```python
@app.route("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    print(configuration.access_token) // Token here
```

You can also get the current authentication status with `is_authenticated`.

```python
if kinde_client.is_authenticated():
		// Core here
```

### Logout

The SDK comes with a logout method that returns a logout url.

```python
kinde_client.logout(redirect_to=KINDE_POST_LOGOUT_REDIRECT_URL)

// implementation
@app.route("/api/auth/logout")
def logout():
    return app.redirect(
        kinde_client.logout(redirect_to=KINDE_POST_LOGOUT_REDIRECT_URL)
    )
```

## Get user information

To access the user information, use the `get_user_details` helper function:

```python
kinde_client.get_user_details();
// returns
{
	"given_name":"Dave",
	"id":"abcdef",
	"family_name":"Smith",
	"email":"dave@smith.com", 
	"picture": "https://link_to_avatar_url.kinde.com"
}
```

### View users in Kinde

Go to the **Users** page in Kinde to see who has registered.

### User permissions

After a user signs in and they are verified, the token return includes permissions for that user. [User permissions are set in Kinde](https://kinde.com/docs/user-management/user-permissions/), but you must also configure your application to unlock these functions.

```python
permissions = [
    "create:todos",
    "update:todos",
    "read:todos",
    "delete:todos",
    "create:tasks",
    "update:tasks",
    "read:tasks",
    "delete:tasks",
]
```

We provide helper functions to more easily access permissions:

```python
kinde_client.get_permission("create:todos")
// {"org_code": "org_b235c067b7e4", is_granted: True}

kinde_client.get_permissions()
// {"org_code": "org_b235c067b7e4", permissions: [ "create:users", "view:users" ]}
```

A practical example in code might look something like:

```python
if kinde_client.get_permission("create:todos").get("is_granted")):
		// create new a todo
```

### Feature Flags

We have provided a helper to grab any feature flag from `access_token`:

```python
kinde_client.get_flag("theme");
// returns
{
    "code": "theme", 
    "type": "string", 
    "value": "pink",
    "is_default": False // whether the fallback value had to be used
}

// Another usage case
kinde_client.get_flag("is_dark_mode");
// returns
{
    "code": "is_dark_mode", 
    "type": "boolean", 
    "value": True,
    "is_default": False
}

// This flag does not exist - default value provided
kinde_client.get_flag("create_competition", default_value = False);
// returns
{
    "code": "create_competition",
    "type" => "boolean", 
    "value": False,
    "is_default": True // because fallback value had to be used
}

// The flag type was provided as string, but it is an integer
kinde_client.get_flag("competitions_limit", default_value = 3, flat_type = "s");
// should error out - Flag "competitions_limit" is type integer - requested type string

// This flag does not exist, and no default value provided
kinde_client.get_flag("new_feature");
// should error out - This flag was not found, and no default value has been provided
```

We also provide wrapper functions which should leverage `getFlag` above.

**Get boolean flags**

```python
kinde_client.get_boolean_flag("is_dark_mode");
// True

kinde_client.get_boolean_flag("is_dark_mode", False);
// True

kinde_client.get_boolean_flag("new_feature", False);
// False (flag does not exist so falls back to default)

kinde_client.get_boolean_flag("new_feature");
// Error - flag does not exist and no default provided

kinde_client.get_boolean_flag("theme", False);
// Error - Flag "theme" is of type string not boolean
```

**Get string flags**

```python
kinde_client.get_string_flag("theme");
// "pink"

kinde_client.get_string_flag("theme", False);
// "pink"

kinde_client.get_string_flag("cta_color", False);
// "blue" (flag does not exist so falls back to default)

kinde_client.get_string_flag("cta_color");
// Error - flag does not exist and no default provided

kinde_client.get_string_flag("is_dark_mode", False);
// Error - Flag "is_dark_mode" is of type boolean not string
```

**Get integer flags**

```python
kinde_client.get_integer_flag("competitions_limit");
// 5

kinde_client.get_integer_flag("competitions_limit", 3);
// 5

kinde_client.get_integer_flag("team_count", 2);
// 2 (flag does not exist so falls back to default)

kinde_client.get_integer_flag("team_count");
// Error - flag does not exist and no default provided

kinde_client.get_integer_flag("is_dark_mode", False);
// Error - Flag "is_dark_mode" is of type string not integer
```

## Audience

An `audience` is the intended recipient of an access token - for example the API for your application. The audience argument can be passed to the Kinde client to request an audience be added to the provided token.

The audience of a token is the intended recipient of the token.

```python
kinde_api_client_params["audience"] = "api.yourapp.com"
```

For details on how to connect, see [Register an API](https://kinde.com/docs/developer-tools/register-an-api/)

## Overriding scope

By default the `KindeSDK` requests the following scopes:

- profile
- email
- offline
- openid

You can override this by passing scope into the `KindeSDK`.

```python
kinde_api_client_params["scope"] = "profile email offline openid"
```

### Getting claims

We have provided a helper to grab any claim from your id or access tokens. The helper defaults to access tokens:

```python
kinde_client.get_claim("aud")
// {"name": "aud", "value": ["api.yourapp.com"]}

kinde_client.get_claim("given_name", "id_token")
// {"name": "given_name", "value": "David"}
```

## Organizations

### Create an organization

To create a new organization within your application, you will need to run a similar function to below:

```python
return app.redirect(kinde_client.create_org())
```

### Sign up and sign in to organizations

Kinde has a unique code for every organization. You’ll have to pass this code through when you register a new user or sign into a particular organization. Example function below:

```python
kinde_api_client_params["org_code"] = 'your_org_code'

@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.get_login_url())

@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.get_register_url())
```

Following authentication, Kinde provides a json web token (jwt) to your application. Along with the standard information we also include the `org_code` and the permissions for that organization (this is important as a user can belong to multiple organizations and have different permissions for each).

Example of a returned token:

```python
{
   "aud": [], 
   "exp": 1658475930, 
   "iat": 1658472329, 
   "iss": "https://your_subdomain.kinde.com", 
   "jti": "123457890", 
   "org_code": "org_1234", 
   "permissions": ["read:todos", "create:todos"], 
   "scp": [
		   "openid", 
		   "profile", 
		   "email", 
		   "offline" 
   ],
   "sub": "kp:123457890" 
}
```

The `id_token` will also contain an array of organizations that a user belongs to - this is useful if you wanted to build out an organization switcher for example.

```python
{
		...
		"org_codes": ["org_1234", "org_4567"], 
		...
};
```

There are two helper functions you can use to extract information:

```python
kinde_client.get_organization()
// {"org_code": "org_1234"}

kinde_client.get_user_organizations()
// {"org_codes": ["org_1234", "org_abcd"]}
```

### Token storage

Once the user has successfully authenticated, you'll get a JWT and possibly a refresh token that should be stored securely.

## SDK API reference

| Property | Type | Is required | Default | Description |
| --- | --- | --- | --- | --- |
| domain | string | Yes |  | Either your Kinde instance url or your custom domain. e.g. https://yourapp.kinde.com/ |
| callback_url | string | Yes |  | The url that the user will be returned to after authentication. |
| client_id | string | Yes |  | The ID of your application in Kinde. |
| grant_type | string | Yes |  | Define the grant type when using the SDK |
| client_secret | string | No |  | The Client secret associated with your application in Kinde. |
| code_verifier | string | Not required except for PKCE flow |  | PKCE works by having the app generate a random value at the beginning of the flow called a Code Verifier. |
| scope | string | No | openid profile email offline | The scopes to be requested from Kinde |
| audience | string | No |  | The audience claim for the JWT |
| org_code | string | No |  | Additional parameters that will be passed in the authorization request |

## ****KindeSDK methods****

| Property | Description | Arguments | Usage | Sample output |
| --- | --- | --- | --- | --- |
| get_login_url | Return the URL sign in |  | kinde_client.get_login_url() | https://your_host.kinde.com/oauth2/auth?response_type=code&… |
| get_register_url | Return the URL sign up |  | kinde_client.get_register_url() | https://your_host.kinde.com/oauth2/auth?response_type=code&… |
| logout | Return the url log out | redirect_to: string | kinde_client.logout(redirect_to= "KINDE_POST_LOGOUT_REDIRECT_URL") | https://your_host.kinde.com/logout?redirect=https://….. |
| fetch_token | Returns the raw access token from URL after logged from Kinde | authorization_response: string | kinde_client.fetch_token(authorization_response="https://example.com/github?code=42..e9&state=d..t") | eyJhbGciOiJIUzI1... |
| refresh_token | Get new access token from Kinde if existed refresh_token |  | kinde_client.refresh_token() |  |
| create_org | Return redirect URL to sign up and create a new org for your business |  | kinde_client.create_org() | https://your_host.kinde.com/oauth2/auth?response_type=code&… |
| get_claim | Gets a claim from an access or ID token | claim: string, token_name?: string // default: access_token | kinde_client.get_claim("given_name", "id_token") | {"name": "given_name", "value": "David"} |
| get_permission | Returns the state of a given permission | key: string | kinde_client.get_permission("read:todos") | {org_code: "org_b235c067b7e4", is_granted: true} |
| get_permissions | Returns all permissions for the current user for the organization they are logged into |  | kinde_client.get_permissions() | {orgCode: "org_b235c067b7e4", permissions: [ "create:users", "view:users" ]} |
| get_organization | Get details for the organization your user is logged into |  | kinde_client.get_organization() | {'orgCode': 'org_1234'} |
| get_organizations | Gets an array of all organizations the user has access to |  | kinde_client.get_user_organizations() | {"org_codes": ["org_1234", "org_abcd"]} |
| get_user_details | Returns the profile for the current user |  | kinde_client.get_user_details() | {'given_name': 'Dave', 'id': 'abcdef', 'family_name': 'Smith', 'email': 'mailto:dave@smith.com'} |
| get_flag | Gets a feature flag from an access token | code: str; default_value?: str; flag_type?: str | kinde_client.get_flag("theme"); | {"code": "theme", "type": "string", "value": "pink", "is_default": False } |
| get_boolean_flag | Gets a boolean feature flag from an access token | code: str; default_value?: str; | kinde_client.get_boolean_flag(”is_dark_mode”); | True or False |
| get_string_flag | Gets a string feature flag from an access token | code: str; default_value?: str; | kinde_client.get_string_flag("theme"); | “pink” |
| get_integer_flag | Gets an integer feature flag from an access token | code: str; default_value?: str; | kinde_client.get_integer_flag("competitions_limit"); | “5” |
| is_authenticated() | To check user authenticated or not |  |  | True or False |

If you need help connecting to Kinde, please contact us at [support@kinde.com](mailto:support@kinde.com).

## Publishing

The core team handles publishing.

## Contributing

Please refer to Kinde’s [contributing guidelines](https://github.com/kinde-oss/.github/blob/489e2ca9c3307c2b2e098a885e22f2239116394a/CONTRIBUTING.md).

## License

By contributing to Kinde, you agree that your contributions will be licensed under its MIT License.
