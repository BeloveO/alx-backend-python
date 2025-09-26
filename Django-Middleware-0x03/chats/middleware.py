from datetime import datetime
import logging
from django.http import HttpResponseForbidden

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