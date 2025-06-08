from datetime import datetime, time, timedelta
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
    

ip_post_cache = {}

class OffensiveLanguageMiddleware:
    """
    Implement middleware that limits the number of chat messages
    a user can send within a certain time window, based on their
    IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response


    def __init__(self, request):
        """
        tracks number of chat messages sent by each ip address
        and implement a time based limit i.e 5 messages per minutes
        """
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize cache for new ip
            if ip not in ip_post_cache:
                ip_post_cache[ip] = {
                    "timestamps": [now]
                }
                
            else:
                timestamps = ip_post_cache[ip]["timestamps"]

                # Remove older timestamp of more than 1 mins
                timestamps = [
                    ts for ts in timestamps
                    if now - ts < timedelta(minutes=1)
                ]

                timestamps.append(now)

                ip_post_cache[ip]["timestamps"] = timestamps

                if len(timestamps) > 5:
                    return HttpResponseForbidden(
                        "You can only send 5 messages per minutes"
                    )


        response = self.get_response


        return response
    

    def get_client_ip(self, request):
        """Returns client ip address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        
        return ip
    

class RolepermissionMiddleware:
    """
    define a middleware that checks the user’s role i.e admin,
    before allowing access to specific actions
    """

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        """
        user is not admin or moderator, return error 403
        """
        user = request.user
        if not user.admin or not user.moderator:
            return HttpResponseForbidden(
                "You are not allow to perform this action"
            )
        
        response = self.get_response

        return response