from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

class CustomException(Exception):
    def __init__(self, message, code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is None:
        if isinstance(exc, CustomException):
            return Response({
                'error': exc.message
            }, status=exc.code)
        return Response({
            'error': str(exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response