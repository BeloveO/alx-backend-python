from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='requests.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# middleware that logs each user’s requests to a file,
# including the timestamp, user and the request path

class RequestLoggingMiddleware:
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