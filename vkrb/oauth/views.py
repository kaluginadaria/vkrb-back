from oauth2_provider.views import (
    TokenView as OAuthTokenView,
    RevokeTokenView as OAuthRevokeTokenView
)
from oauthlib.oauth2 import (
    LegacyApplicationServer,
)


class TokenView(OAuthTokenView):
    server_class = LegacyApplicationServer


class RevokeTokenView(OAuthRevokeTokenView):
    server_class = LegacyApplicationServer
