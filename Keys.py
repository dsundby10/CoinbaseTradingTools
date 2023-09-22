import cbpro

# INSERT YOUR CB Pro API CREDENTIALS
key = ""
passphrase = ""
b64secret = ""


def getAuthClient():
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)

    return auth_client

def getAuthClientByKeys(key, b64secret, passphrase):
    auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
    return auth_client
