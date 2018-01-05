from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .client.oauth2_client import OAuth2Client
from .client.auth_proxy import AuthClient, SessionsClient
from .client.users_client import UsersClient
import json
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
import base64


API_KEY = settings.API_KEY
OKTA_ORG = settings.OKTA_ORG
AUTH_SERVER_ID = settings.AUTH_SERVER_ID
CUSTOM_LOGIN_URL = settings.CUSTOM_LOGIN_URL
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
GOOGLE_IDP = settings.GOOGLE_IDP
FB_IDP = settings.FB_IDP
LNKD_IDP = settings.LNKD_IDP
SAML_IDP = settings.SAML_IDP

ORG = OKTA_ORG
if CUSTOM_LOGIN_URL and CUSTOM_LOGIN_URL != 'None':
    ORG = CUSTOM_LOGIN_URL
ISSUER = AUTH_SERVER_ID

c = {
    "org": ORG,
    "iss": ISSUER,
    "aud": CLIENT_ID,
    "google": GOOGLE_IDP,
    "fb": FB_IDP,
    "lnkd": LNKD_IDP,
    "saml_idp": SAML_IDP
}


def view_home(request):
    if 'profile' in request.session:
        profile = json.loads(request.session['profile'])
        if 'preferred_username' in profile:
            try:
                u = User.objects.get(username=profile['preferred_username'])
                if u is not None:
                    print('user = {}'.format(u))
                    login(request, u)
            except Exception as e:
                print('exception: {}'.format(e))
        return HttpResponseRedirect(reverse('profile'))
    else:
        print('no profile in request')

    return view_login(request)


def not_authenticated(request):
    return render(request, 'not_authenticated.html')


def view_profile(request):
    if 'profile' in request.session:
        p = {'profile': request.session['profile'],
             'org': ORG
             }
    else:
        return HttpResponseRedirect(reverse('not_authenticated'))

    return render(request, 'profile.html', p)


def view_tokens(request):
    return render(request, 'tokens.html', c)


def view_login(request):
    return render(request, 'index.html', c)


def view_login_css(request):
    return render(request, 'index_css.html', c)


def okta_hosted_login(request):
    return render(request, 'customized-okta-hosted.html', c)


def view_login_custom(request):
    return render(request, 'index_login-form.html', c);


def view_login_raas(request):
    return render(request, 'index_raas.html', c)


def view_login_idp(request):
    return render(request, 'login_idp.html', c)


def view_login_baybridge(request):
    return render(request, 'z-login-baybridge.html');


def view_login_brooklynbridge(request):
    return render(request, 'z-login-brooklynbridge.html');


def hellovue(request):
    return render(request, 'z-hellovue.html');


def view_logout(request):
    if 'profile' in request.session:
        del request.session['profile']
    return render(request, 'logged_out.html', c)


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            fn = form.cleaned_data['firstName']
            ln = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            pw = form.cleaned_data['password1']
            user = {
                "profile": {
                    "firstName": fn,
                    "lastName": ln,
                    "email": email,
                    "login": email
                },
                "credentials": {
                    "password": {"value": pw}
                }
            }
            client = UsersClient('https://' + OKTA_ORG, API_KEY)
            client.create_user(user=user, activate="true")

        try:
            print('create user {0} {1}'.format(fn, ln))

            return HttpResponseRedirect(reverse('registration_success'))
        except Exception as e:
            print("Error: {}".format(e))
            form.add_error(field=None, error=e)

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def registration_success(request):
    return render(request, 'success.html')


def oauth2_callback(request):
    return render(request, 'oauth2_callback.html')


@csrf_exempt
def oauth2_post(request):
    print('in oauth2_postback')
    access_token = None
    id_token = None
    if request.method == 'POST':
        print('POST request: {}'.format(request.POST))
        if 'code' in request.POST:
            code = request.POST['code']
            print('auth code = {}'.format(code))

            client = OAuth2Client('https://' + OKTA_ORG, CLIENT_ID, CLIENT_SECRET)
            tokens = client.token(code, 'http://localhost:8000/oauth2/postback', AUTH_SERVER_ID)
            if tokens['access_token']:
                access_token = tokens['access_token']
            if tokens['id_token']:
                id_token = tokens['id_token']

        if 'access_token' in request.POST:
            access_token = request.POST['access_token']

        if 'id_token' in request.POST:
            id_token = request.POST['id_token']

    if access_token:
        print('access_token = {}'.format(access_token))
        client = OAuth2Client('https://' + OKTA_ORG)
        profile = client.profile(access_token)
        print('profile = {}'.format(profile))
        request.session['profile'] = json.dumps(profile)
        request.session['given_name'] = profile['given_name']
        request.session['user_id'] = profile['sub']

    if id_token:
        print('id_token = {}'.format(id_token))
        if 'profile' not in request:
            try:
                parts = id_token.split('.')
                payload = parts[1]
                payload += '=' * (-len(payload) % 4)  # add == padding to avoid padding errors in python
                decoded = base64.b64decode(payload)
                print('decoded = {}'.format(decoded))
                request.session['profile'] = decoded
            except Exception as e:
                print('exception: {}'.format(e))
        else:
            print('profile = {}'.format(request.session['profile']))

    return HttpResponseRedirect(reverse('home'))


@csrf_exempt
def auth_broker(request):
    print(request)
    cookies = request.COOKIES
    print('cookie: {}'.format(cookies))

    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        auth = AuthClient('https://' + OKTA_ORG)
        res = auth.authn(username, password)
        print('status={}'.format(res.status_code))
        response.status_code = res.status_code

        content = json.dumps(res.json())
        print('response={}'.format(content))
        response.content=content

        return response

    return response


def sessions_broker(request):
    print(request)
    response = HttpResponse()
    response.status_code = 200

    cookies = request.COOKIES
    print('cookie: {}'.format(cookies))

    auth = SessionsClient('https://' + OKTA_ORG)
    res = auth.me()
    response.status_code = res.status_code
    content = json.dumps(res.json())
    print('response={}'.format(content))
    response.content=content

    return response


def view_app_b(request):
    return render(request, 'app_b.html')
