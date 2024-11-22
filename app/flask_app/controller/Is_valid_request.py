from flask import request

def is_valid_request(req: request) -> bool:
    data = req.get_json()  # Expecting JSON input

    secret = data.get('secretText')
    expire_after_views = data.get('retrievalCount')
    expire_after = data.get('expiryDate')

    if not secret or not expire_after_views or not expire_after or expire_after == 0:
        return False

    try:
        expire_after_views = int(expire_after_views)
        expire_after = int(expire_after)
    except ValueError:
        return False

    return True