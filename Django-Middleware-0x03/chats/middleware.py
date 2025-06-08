from datetime import datetime, time
from django.conf import settings
import os
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """One-time configuration and initialization"""
        self.get_response = get_response


    def __call__(self, request):
        """
        Create a middleware that logs each user’s requests to a file,
        including the timestamp, user and the request path.
        """
        response = self.get_response(request)
        
        try:
            log_dir = os.path.join(settings.BASE_DIR)
            file_path = os.path.join(log_dir, "requests.log")
            user = request.user.user_id if request.user.is_authenticated else "Anonymous"

            with open(file_path, 'a') as logs: 
                logs.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        except Exception as e:
            print("Logging failed:", e)

        return response



class RestrictAccessByTimeMiddleware:
    """
    implement a middleware that restricts access to the
    messaging up during certain hours of the day
    """

    def __int__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        """
        Create a middleware that logs each user’s requests to a file,
        including the timestamp, user and the request path.
        """

        # Check if the path is for chat
        if request.path.startswith("/api/v1/conversations/"):
            now = datetime.now()
            start_time = time(18, 0) # 6pm
            end_time = time(21, 0) # 9pm

            # Check the time range
            if not (start_time <= now <= end_time):
                return HttpResponseForbidden
        response = self.get_response(request)

        return response