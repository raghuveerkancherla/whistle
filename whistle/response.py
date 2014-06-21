
def create_response(response_type, meta=None, data=None):
    return dict(
        response_type=response_type,
        data=data if response_type is 'success' else None,
        meta=meta)
