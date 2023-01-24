from bottle import Bottle, request
import kinde_sdk

from kinde_sdk.kinde_api_client import KindeApiClient

app = Bottle()

# TODO: move to .env ???
# KINDE_SITE_URL="http://localhost:3000"
# KINDE_POST_LOGOUT_REDIRECT_URL="http://localhost:3000"
# KINDE_CLIENT_ID="CLIENT_ID"
# KINDE_ISSUER_URL="https://app.kinde.com"
# KINDE_CLIENT_SECRET="CLIENT_SECRET"


domain = "https://softkraft2.kinde.com"
client_id = "CLIENT_ID"
client_secret = "CLIENT_SECRET"
grant_type = "authorization_code"

configuration = kinde_sdk.Configuration(host=domain)
kinde_client = KindeApiClient(
    configuration=configuration,
    domain=domain,
    client_id=client_id,
    client_secret=client_secret,
    grant_type=grant_type,
)


@app.get("/login")
def login():
    kinde_client.login()
    kinde_client.get_authorization_url()

    return f"""<form action="{kinde_client.authorization_url}" method="post">
                    <input value="Sign in" type="submit" />
               </form> 
            """


@app.get("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(request.url)
    return f"{kinde_client.access_token_obj}"


app.run(host="localhost", port=8080)
