from aiogoogle.auth.creds import ServiceAccountCreds

from bot.core.const import SCOPES, INFO


def get_service():
    return ServiceAccountCreds(scopes=SCOPES, **INFO)
