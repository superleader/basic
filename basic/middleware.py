from basic.models import Location


class HttpRequestMiddleware(object):
    def process_request(self, request):
        loc = Location(name=request.get_full_path())
        loc.save()