from flask import request

def is_valid_request(req: request) -> bool:
    # Use .get() to avoid KeyErrors when fields are missing

    # Use .get() to avoid KeyErrors when fields are missing
    data = req.get_json()  # Expecting JSON input

    secret = data.get('secretText')
    expire_after_views = data.get('retrievalCount')
    expire_after = data.get('expiryDate')

    # Check if any required field is missing or has an empty value
    if not secret or not expire_after_views or not expire_after:
        # Return False if any field is missing or empty
        return False

    try:
        # Check if expireAfterViews and expireAfter are valid integers
        expire_after_views = int(expire_after_views)
        expire_after = int(expire_after)
    except ValueError:
        # If any of these fields can't be converted to integers, return False
        return False

    # If all conditions are met, return True
    return True