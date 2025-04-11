from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

class ResponseBuilder(object):
    """
    API response builder
    """

    def __init__(self):
        self.results={}
        self.status_code= 1
        self.status_message= ""
        self.status= status.HTTP_200_OK

    def fail(self):
        self.status_code= -1
        return self
    
    """
    This enables app to handle messages differently than error code -1. 
    In general cases use fail() only. 
    Use this when you specifically wants app to handle this error message differently.
    """

    def message(Self, status_message):
        Self.status_message= status_message
        return Self
    
    def success(Self):
        Self.status_code=1
        return Self
    
    def ok_200(Self):
        Self.status= status.HTTP_200_OK
        return Self
    
    def accepted_202(Self):
        Self.status= status.HTTP_202_ACCEPTED
        return Self
    
    def not_found_400(Self):
        Self.status= status.HTTP_400_BAD_REQUEST
        return Self
    
    def bad_request_404(Self):
        Self.status= status.HTTP_404_NOT_FOUND
        return Self
    
    def user_unauthorized_401(Self):
        Self.status = status.HTTP_401_UNAUTHORIZED
        Self.status_message = "User Unauthorized"
        return Self
    
    def internal_error_500(Self):
        Self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Self
    
    def result_object(self, result):
        self.results= result
        return self
    
    def get_response(Self):
        content= Self.get_json()
        return Response(content, status=Self.status)
    
    def get_json(Self):
        return{
            "status_code":Self.status_code,
            "status_message":Self.status_message,
            "data":Self.results
        }

    def get_json_response(self):
        content = self.get_json()
        return JsonResponse(content)
    
    @staticmethod
    def return_failed_json_response(message):
        return ResponseBuilder().ok_200().fail().message(message).get_json_response()
   
    
