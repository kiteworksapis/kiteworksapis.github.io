import time
import uuid
import jwt
import requests
from cryptography.hazmat.primitives import serialization

class OAuthJWTAssertionClient:
    """
    Demonstration of OAuth 2.0 JWT Assertion Flow with RSA signatures.

    The Authorization Server expects:
      - 'client_id'
      - 'client_secret'
      - 'grant_type' = "urn:ietf:params:oauth:grant-type:jwt-bearer"
      - 'assertion' = <signed-JWT>

    The JWT includes the following claims:
      iss (Issuer)
      sub (Subject)
      aud (Audience)
      iat (Issued At)
      nbf (Not Before)
      exp (Expiration Time)
      jti (JWT ID)
    """

    def __init__(self, issuer, subject, audience, private_key, token_endpoint,
                 client_id, client_secret, algorithm="RS256"):
        """
        :param issuer: The issuer of the JWT i.e. the KW domain URL.
        :param subject: The Kiteworks User Account the client is logged in as
        :param audience: The audience of the JWT, such as the client name.
        :param private_key: RSA private key (PEM string) used to sign the JWT.
        :param token_endpoint: URL of the OAuth 2.0 token endpoint.
        :param algorithm: The JWT signing algorithm (default "RS256").
        """
        self.issuer = issuer
        self.subject = subject
        self.audience = audience
        self.private_key = private_key
        self.token_endpoint = token_endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.algorithm = algorithm

    def create_jwt_assertion(self, validity_seconds=300):
        """
        Create and sign a JWT assertion using the specified RSA private key.
        :param validity_seconds: How long (in seconds) before the JWT expires.
        """
        now = int(time.time())

        # Build the JWT claims
        payload = {
            "iss": self.issuer,
            "sub": self.subject,
            "aud": self.audience,
            "iat": now,            # Issued at
            "nbf": now,            # Not valid before now
            "exp": now + validity_seconds,  # Expires in 'validity_seconds'
            "jti": str(uuid.uuid4())        # Unique JWT ID
        }

        # Sign the JWT with the RSA private key
        jwt_assertion = jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm
        )
        return jwt_assertion

    def get_access_token(self, scope=None, validity_seconds=300):
        """
        Request an OAuth 2.0 access token using the JWT Bearer assertion.
        :param scope: (Optional) scope of the requested access token, if required by your AS.
        :param validity_seconds: Validity period for the signed JWT (in seconds).
        :return: Access token as a string, or raise an exception on error.
        """
        # Create the signed JWT
        assertion = self.create_jwt_assertion(validity_seconds=validity_seconds)

        # Prepare the token request
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion
        }
        if scope:
            # Some providers require a "scope" parameter
            data["scope"] = scope

        # Call the token endpoint
        response = requests.post(self.token_endpoint, data=data)
        print(response.text)
        response.raise_for_status()

        token_response = response.json()
        access_token = token_response.get("access_token")
        if not access_token:
            raise ValueError("No access_token returned from the token endpoint.")

        return access_token


if __name__ == "__main__":
    host_name = input("Enter KW instance domain: ")
    token_endpoint = f"{host_name}/oauth/token"


    private_key_path = input("Enter Private Key File Path: ")
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    client = OAuthJWTAssertionClient(
        issuer=host_name,
        subject=input("Enter Username: "),
        audience=input("Enter JWT Audience: "),
        private_key=private_key,
        token_endpoint=token_endpoint,
        client_id=input("Enter your Client ID: "),
        client_secret=input("Enter your Client Secret: ")
    )

    access_token = client.get_access_token(validity_seconds=300)
    print("Got Access Token:", access_token)
