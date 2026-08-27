def success_response(message: str, data=None):
    return {
        "status": True,
        "message": message,
        "data": {} if data is None else data,
    }


def error_response(message: str):
    return {
        "status": False,
        "message": message,
    }
