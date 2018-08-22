from django.http import HttpResponse


def access_token_required(func):
    def wrapper(request, *args, **kw):
        access_token = None

        if 'HTTP_AUTHORIZATION' in request.META:
            auth_header = request.META['HTTP_AUTHORIZATION']
            if auth_header:
                if auth_header.split(' ')[0] == 'Bearer':
                    access_token = auth_header.split(' ')[1]

        if access_token:
            # Demo code does not validate access token. Normally, it'd be done here.
            return func(request, access_token, *args, **kw)
        else:
            # no access_token. return 401 (Unauthorized)
            response = HttpResponse()
            response.status_code = 401
            return response
    return wrapper
