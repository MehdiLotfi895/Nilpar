from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):

        ip = request.META.get("REMOTE_ADDR")

        key = f"rate_limit_{ip}"

        count = cache.get(key, 0)

        limit = 100
        seconds = 60

        if count >= limit:
            return JsonResponse(
                {
                    "error": "Too many requests"
                },
                status=429
            )

        if count == 0:
            cache.set(
                key,
                1,
                seconds
            )
        else:
            cache.incr(key)

        response = self.get_response(request)

        return response