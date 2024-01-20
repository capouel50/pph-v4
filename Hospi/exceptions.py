from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(response.data, dict):
            # C'est un dictionnaire, on peut utiliser 'get'
            response.data['detail'] = response.data.get('detail', str(exc))
        elif isinstance(response.data, list):
            # C'est une liste, on traite différemment
            response.data = {'detail': str(exc), 'errors': response.data}
    return response

