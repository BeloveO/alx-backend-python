from datetime import datetime
import logging
from django.http import HttpResponseForbidden, JsonResponse

# Configure logging
logging.basicConfig(filename='requests.log', level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    # middleware that logs each user’s requests to a file,
    # including the timestamp, user and the request path
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the incoming request method and path
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = (f"{datetime.now()} - User: {user} - Path: {request.path}")
        logger.info(log_message)
        print(log_message)  # For demonstration, print to console

        response = self.get_response(request)

        # Log the response status code
        print(f"Response status: {response.status_code}")

        return response
    
class RestrictAccessByTimeMiddleware:
    # restricts access to the messaging app during certain hours of the day.
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current hour
        current_hour = datetime.now().hour

        # Restrict access to the app outside 21:00 and 18:00
        if current_hour > 18 and current_hour < 21:
            return HttpResponseForbidden("Access to the messaging app is restricted during this time.")

        response = self.get_response(request)
        return response
    
class OffensiveLanguageMiddleware:
    # limits the number of chat messages a user can 
    # send within a certain time window, based on their IP address.

    REQUEST_LIMIT = 5  # Max messages
    TIME_WINDOW = 60  # Time window in seconds
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_request_times = {}

    def __call__(self, request):
        # tracks number of chat messages sent by each ip 
        # address and implement a time based limit i.e 5
        # messages per minute such that if a user exceeds
        # the limit, it blocks further messaging and returns an error.
        if request.method == 'POST' and 'messages' in request.path:
            ip = self.get_client_ip(request)
            current_time = datetime.now().timestamp()
            request_times = self.ip_request_times.get(ip, [])
            # Remove timestamps outside the time window
            request_times = [t for t in request_times if current_time - t < self.TIME_WINDOW]
            if len(request_times) >= self.REQUEST_LIMIT:
                return JsonResponse({"error": "Message limit exceeded. Please wait before sending more messages."}, status=429)
            request_times.append(current_time)
            self.ip_request_times[ip] = request_times

    def get_client_ip(self, request):
        # Get client IP address from request
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    
class RolepermissionMiddleware:
    # checks the user’s role i.e admin, before allowing access to specific actions
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = ['/admin/', '/moderate/']  # Example protected paths

    def __call__(self, request):
        # If the user is not admin or moderator, it should return error 403
        is_admin = request.user.is_authenticated and request.user.role in ['admin', 'moderator']
        if any(request.path.startswith(path) for path in self.protected_paths):
            if not is_admin:
                return JsonResponse({"error": "You do not have permission to access this resource."}, status=403)
        response = self.get_response(request)
        return response