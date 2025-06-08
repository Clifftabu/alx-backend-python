import logging


logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logging.info(f"{request.method} request to {request.path}")
        response = self.get_response(request)
        return response
