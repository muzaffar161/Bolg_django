import time


class RequestTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        print(
            f"Path: {request.path} | "
            f"Method: {request.method} | "
            f"Time: {duration:.4f} seconds"
        )

        return response


class AuthenticationCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = [
            "/articles/add/",
            "/profile/",
        ]

        is_protected = request.path in protected_paths or (
            request.path.startswith("/articles/")
            and (
                request.path.endswith("/edit/")
                or request.path.endswith("/delete/")
                or request.path.endswith("/comments/")
            )
        )

        if is_protected and not request.user.is_authenticated:
            print(f"Unauthorized access attempt: {request.path}")

        return self.get_response(request)
