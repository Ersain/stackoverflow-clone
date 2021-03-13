import secrets


def generate_uniq_code():
    return secrets.token_urlsafe(8)
