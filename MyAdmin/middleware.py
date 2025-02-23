from django.http import HttpResponseForbidden

class MyAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.user_type == 0:
                response = self.get_response(request)
            elif request.user.user_type == 1:
                response = self.get_response(request)
            elif request.user.user_type == 2:
                response = self.get_response(request)
            
        response = self.get_response(request)
        return response
