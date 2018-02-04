from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from .client.oauth2_client import OAuth2Client
from .client.auth_proxy import AuthClient, SessionsClient
from .client.users_client import UsersClient
import json
from .forms import RegistrationForm, TextForm
from django.contrib.auth.models import User
from django.contrib.auth import login
import base64
from django.contrib.staticfiles.templatetags.staticfiles import static
import requests


API_KEY = settings.API_KEY
OKTA_ORG = settings.OKTA_ORG
ISSUER = settings.AUTH_SERVER_ID
CUSTOM_LOGIN_URL = settings.CUSTOM_LOGIN_URL
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

GOOGLE_IDP = settings.GOOGLE_IDP
FB_IDP = settings.FB_IDP
LNKD_IDP = settings.LNKD_IDP
SAML_IDP = settings.SAML_IDP

DEFAULT_BACKGROUND = '/static/img/okta-brand/background/SFbayBridge.jpg'
BACKGROUND_IMAGE = settings.BACKGROUND_IMAGE_DEFAULT
BACKGROUND_IMAGE_CSS = settings.BACKGROUND_IMAGE_CSS
BACKGROUND_IMAGE_AUTHJS = settings.BACKGROUND_IMAGE_AUTHJS
BACKGROUND_IMAGE_IDP = settings.BACKGROUND_IMAGE_IDP

REDIRECT_URI = 'http://localhost:8000/oauth2/callback'

BASE_URL = OKTA_ORG
if CUSTOM_LOGIN_URL and CUSTOM_LOGIN_URL != 'None':
    BASE_URL = CUSTOM_LOGIN_URL

DEFAULT_SCOPES = settings.DEFAULT_SCOPES
scopes = None
if DEFAULT_SCOPES:
    scopes = DEFAULT_SCOPES

c = {
    "org": BASE_URL,
    "iss": ISSUER,
    "aud": CLIENT_ID,
    "background": BACKGROUND_IMAGE if BACKGROUND_IMAGE is not None else DEFAULT_BACKGROUND,
    "background_css": BACKGROUND_IMAGE_CSS if BACKGROUND_IMAGE_CSS is not None else DEFAULT_BACKGROUND,
    "background_authjs": BACKGROUND_IMAGE_AUTHJS if BACKGROUND_IMAGE_AUTHJS is not None else DEFAULT_BACKGROUND,
    "background_idp": BACKGROUND_IMAGE_IDP if BACKGROUND_IMAGE_IDP is not None else DEFAULT_BACKGROUND
}

url_map = {}
pages_js = {}


def view_home(request):
    for key in list(request.session.keys()):
        print('h:session key: {}'.format(key))

    if 'profile' in request.session:
        # profile = json.loads(request.session['profile'])
        # print('profile={}'.format(profile))
        # if 'preferred_username' in profile:
        #     try:
        #         u = User.objects.get(username=profile['preferred_username'])
        #         if u is not None:
        #             print('user = {}'.format(u))
        #             login(request, u)
        #     except Exception as e:
        #         print('exception: {}'.format(e))
        return HttpResponseRedirect(reverse('profile'))
    else:
        print('no profile in request')
    return view_login(request)


def not_authenticated(request):
    return render(request, 'not_authenticated.html')


def view_profile(request):
    if 'profile' in request.session:
        page = pages_js['entry_page']
        if page == 'login_css':
            page = 'login'
        p = {'profile': request.session['profile'],
             'org': BASE_URL,
             "js": _do_format(request, url_map[page], page)
             }
    else:
        return HttpResponseRedirect(reverse('not_authenticated'))
    return render(request, 'profile.html', p)


def view_tokens(request):
    return render(request, 'tokens.html', c)


@csrf_exempt
def view_login(request):
    page = 'login'
    pages_js['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        c.update({"js": _do_format(request, '/js/oidc_base.js', page)})
    return render(request, 'index.html', c)


def _do_refresh(request, key):
    if 'Update' not in request.POST:
        if key in pages_js:
            del pages_js[key]
        return HttpResponseRedirect(request.build_absolute_uri())

    form = TextForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['myText']
        pages_js[key] = text
        return HttpResponseRedirect(request.build_absolute_uri())
    return HttpResponseRedirect('/')


def _do_format(request, url, key, org_url=BASE_URL, issuer=ISSUER, audience=CLIENT_ID,
               idps='[]', btns='[]'):
    url_map.update({key: url})

    list_scopes = ['openid', 'profile', 'email']
    if scopes:
        list_scopes = scopes.split(',')
    scps = ''.join("'" + s + "', " for s in list_scopes)
    scps = '[' + scps[:-2] + ']'

    if key in pages_js:  # request.session:
        #return request.session[key]
        return pages_js[key]
    else:
        response = requests.get(request.build_absolute_uri(static(url)))
        text = str(response.content, 'utf-8')\
            .replace("{", "{{").replace("}", "}}")\
            .replace("[[", "{").replace("]]", "}")\
            .format(org=org_url,
                    iss=issuer,
                    aud=audience,
                    redirect=REDIRECT_URI,
                    scopes=scps,
                    idps=idps,
                    btns=btns)
        # request.session[key] = text
        pages_js[key] = text
        return text


@csrf_exempt
def view_login_css(request):
    page = 'login_css'
    pages_js['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, 'login')
    else:
        c.update({"js": _do_format(request, '/js/oidc_base.js', 'login')})
    return render(request, 'index_css.html', c)


@csrf_exempt
def view_login_custom(request):
    page = 'login_custom'
    pages_js['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        c.update({"js": _do_format(request, '/js/custom_ui.js', page)})
    return render(request, 'index_login-form.html', c);


@csrf_exempt
def okta_hosted_login(request):
    page = 'okta_hosted_login'
    pages_js['entry_page'] = page
    c.update({"js": _do_format(request, '/js/default-okta-signin-pg.js', page)})
    return render(request, 'customized-okta-hosted.html', c)


@csrf_exempt
def view_login_raas(request):
    page = 'login_raas'
    pages_js['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        c.update({"js": _do_format(request, '/js/oidc_raas.js', page)})
    return render(request, 'index_raas.html', c)


@csrf_exempt
def view_login_idp(request):
    idps = '['
    if GOOGLE_IDP:
        if GOOGLE_IDP != 'None':
            idps += "\n      {{type: 'GOOGLE', id: '{}'}},".format(GOOGLE_IDP)
        if FB_IDP != 'None':
            idps += "\n      {{type: 'FACEBOOK', id: '{}'}},".format(FB_IDP)
        if LNKD_IDP != 'None':
            idps += "\n      {{type: 'LINKEDIN', id: '{}'}},".format(LNKD_IDP)
    idps += ']'

    btns = '['
    if SAML_IDP:
        if SAML_IDP != 'None':
            btns += "{title: 'Login SAML Idp',\n" \
                    + "        className: 'btn-customAuth',\n" \
                    + "        click: function() {\n" \
                    + "          var link =  '{issuer}/v1/authorize'\n".format(issuer='https://' + OKTA_ORG + '/oauth2/' + ISSUER) \
                    + "          + '?response_type=code'\n" \
                    + "          + '&client_id={client_id}'\n".format(client_id=CLIENT_ID) \
                    + "          + '&scope=openid+email+profile'\n" \
                    + "          + '&redirect_uri={redirect}'\n".format(redirect=REDIRECT_URI) \
                    + "          + '&state=foo'\n" \
                    + "          + '&nonce=foo'\n" \
                    + "          + '&idp={idp_id}'\n".format(idp_id=SAML_IDP) \
                    + "          window.location.href = link;\n" \
                    + "        }\n" \
                    + "    }"
    btns += ']'

    page = 'login_idp'
    pages_js['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        c.update({"js": _do_format(request, '/js/oidc_idp.js', page, idps=idps, btns=btns)})
    return render(request, 'index_idp.html', c)


def view_login_baybridge(request):
    return render(request, 'z-login-baybridge.html');


def view_login_brooklynbridge(request):
    return render(request, 'z-login-brooklynbridge.html');


def hellovue(request):
    return render(request, 'z-hellovue.html');


def view_logout(request):
    if 'profile' in request.session:
        del request.session['profile']
    page = 'login' if pages_js['entry_page'] == 'okta_hosted_login' else pages_js['entry_page']
    print('logout back to page {}'.format(page))
    print('url = {}'.format(reverse(page)))
    c.update({"page": reverse(page)})

    for key in list(request.session.keys()):
        print('deleting {}'.format(key))
        del request.session[key]
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
    print('in /oauth2/callback')
    access_token = None
    id_token = None
    state = None
    code = None
    if request.method == 'POST':
        print('POST request: {}'.format(request.POST))
        if 'code' in request.POST:
            code = request.POST['code']
        if 'access_token' in request.POST:
            access_token = request.POST['access_token']
        if 'id_token' in request.POST:
            id_token = request.POST['id_token']
        if 'state' in request.POST:
            state = request.POST['state']
    elif request.method == 'GET':
        print('GET request: {}'.format(request.GET))
        if 'code' in request.GET:
            code = request.GET['code']
        if 'state' in request.GET:
            state = request.GET['state']

    if code:
        print('auth code = {}'.format(code))
        client = OAuth2Client('https://' + OKTA_ORG, CLIENT_ID, CLIENT_SECRET)
        tokens = client.token(code, REDIRECT_URI, ISSUER)
        if tokens['access_token']:
            access_token = tokens['access_token']
        if tokens['id_token']:
            id_token = tokens['id_token']

    print('state: {}'.format(state))

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
        if 'profile' not in request.session:
            try:
                parts = id_token.split('.')
                payload = parts[1]
                payload += '=' * (-len(payload) % 4)  # add == padding to avoid padding errors in python
                decoded = str(base64.b64decode(payload), 'utf-8')
                print('decoded = {}'.format(decoded))
                profile = json.loads(decoded)
                request.session['profile'] = decoded
                request.session['given_name'] = profile['given_name']
                request.session['user_id'] = profile['sub']
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
