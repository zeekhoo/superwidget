from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from .client.oauth2_client import OAuth2Client
from .client.auth_proxy import AuthClient
from .client.users_client import UsersClient
from .client.oktadelegate_client import OktadelegateClient
from .forms import RegistrationForm, RegistrationForm2, TextForm, ActivationForm, ActivationWithEmailForm
from .configs import *


config = Config()


def view_home(request):
    if is_logged_in(request):
        return HttpResponseRedirect(reverse('profile'))
    else:
        print('no profile in request')
    return view_login(request)


def not_authenticated(request):
    return render(request, 'not_authenticated.html')


def not_authorized(request):
    return render(request, 'not_authorized.html')


def view_profile(request):
    conf = _get_config(request, 'profile')
    if is_logged_in(request):
        _update_conf(request, {
            'profile': json.dumps(get_profile(request)),
            "srv_access_token": get_access_token(request),
            "srv_id_token": get_id_token(request)
        })
    else:
        return HttpResponseRedirect(reverse('not_authenticated'))

    return render(request, 'profile.html', conf)


def edit_profile(request):
    conf = _get_config(request, 'editProfile')
    if is_logged_in(request):
        conf.update({
            'profile': json.dumps(get_profile(request)),
            "srv_access_token": get_access_token(request),
            "srv_id_token": get_id_token(request)
        })
    else:
        return HttpResponseRedirect(reverse('not_authenticated'))
    return render(request, 'edit-profile.html', conf)


def view_tokens(request):
    conf = _get_config(request, 'viewTokens')
    return render(request, 'tokens.html', conf)


def _resolve_redirect_uri(redirect_uri, host):
    return redirect_uri\
        .replace("[[", "{") \
        .replace("]]", "}") \
        .format(host=host)


def _get_config(request, calledFrom=None):
    print('{0}################## getConfig from {1}'.format(datetime.now(), calledFrom))
    conf = config.get_config(request)
    return conf


def _update_conf(request, obj):
    conf = request.session['config']
    conf.update(obj)
    request.session['config'] = conf
    return conf


@csrf_exempt
def view_login(request, recoveryToken=None):
    conf = _get_config(request, 'default')
    unused = recoveryToken
    page = 'login'
    request.session['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        conf = _update_conf(request, {"js": _do_format(request, '/js/oidc_base.js', page)})
    return render(request, 'index.html', conf)


def view_auth_groupadmin(request):
    conf = _get_config(request, 'groupadmin')
    if not is_admin(request):
        return HttpResponseRedirect(reverse('not_authorized'))

    page = 'login_groupadmin'

    referrer = ''
    if 'from' in request.GET:
        referrer = request.GET['from']

    if referrer and referrer != '':
        request.session['entry_page'] = referrer

    _update_conf(request, {"js": _do_format(request, '/js/groupadmin_delegate.js', page)})
    return render(request, 'index_get_without_prompt.html', conf)


def view_login_auto(request):
    conf = _get_config(request, 'auto')
    page = 'login_noprompt'

    referrer = ''
    if 'from' in request.GET:
        referrer = request.GET['from']
    if referrer and referrer != '':
        request.session['entry_page'] = referrer

    conf.update({"js": _do_format(request, '/js/get_without_prompt.js', page)})

    saved_entry_page = request.session['entry_page']
    logout(request)
    request.session['entry_page'] = saved_entry_page
    return render(request, 'index_get_without_prompt.html', conf)


def _do_refresh(request, page):
    key = 'pages_js_{}'.format(page)
    if 'Update' not in request.POST:
        if key in request.session:
            del request.session[key]
        return HttpResponseRedirect(reverse(page))

    form = TextForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['myText']
        request.session[key] = text
        print('js {0} updated'.format(key))
        return HttpResponseRedirect(reverse(page))
    return HttpResponseRedirect('/')


def _do_format(request, url, page, idps='[]', btns='[]', embed_link=None):
    key = 'pages_js_{}'.format(page)
    cfg = _get_config(request, 'doFormat')

    list_scopes = ['openid', 'profile', 'email']
    if cfg['scopes']:
        list_scopes = cfg['scopes'].split(',')
    scps = ''.join("'" + s + "', " for s in list_scopes)
    scps = '[' + scps[:-2] + ']'

    if key in request.session:
        print('found {}'.format(key))
        return request.session[key]
    else:
        try:
            s = requests.session()
            a = requests.adapters.HTTPAdapter(max_retries=2)
            s.mount('http://', a)
            response = s.get(cfg['host'] + static(url))

            text = str(response.content, 'utf-8') \
                .replace("{", "{{").replace("}", "}}") \
                .replace("[[", "{").replace("]]", "}") \
                .format(base_icon=cfg['base_icon'],
                        base_url=cfg['base_url'],
                        org=cfg['org'],
                        iss=cfg['iss'],
                        aud=cfg['aud'],
                        redirect=cfg['redirect_uri'],
                        auth_groupadmin_redirect=cfg['auth_groupadmin_redirect_uri'],
                        scopes=scps,
                        idps=idps,
                        btns=btns,
                        idp_disco=embed_link)
            request.session[key] = text
        except Exception as e:
            text = e
        return text


@csrf_exempt
def view_login_css(request):
    conf = _get_config(request, 'css')
    page = 'login_css'
    request.session['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        conf = _update_conf(request, {"js": _do_format(request, '/js/oidc_css.js', page)})

    return render(request, 'index_css.html', conf)


@csrf_exempt
def view_login_custom(request):
    conf = _get_config(request, 'custom')
    page = 'login_custom'
    request.session['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        conf = _update_conf(request, {"js": _do_format(request, '/js/custom_ui.js', page)})
    return render(request, 'index_login-form.html', conf);


@csrf_exempt
def okta_hosted_login(request):
    page = 'okta_hosted_login'
    request.session['entry_page'] = page
    conf = _update_conf(request, {"js": _do_format(request, '/js/default-okta-signin-pg.js', page)})
    return render(request, 'customized-okta-hosted.html', conf)


@csrf_exempt
def view_login_idp(request):
    conf = _get_config(request, 'idp')
    idps = '['
    if conf['google_idp'] is not None and (len(conf['google_idp'])>0):
        idps += "\n      {{type: 'GOOGLE', id: '{}'}},".format(conf['google_idp'])
    if conf['fb_idp'] is not None and (len(conf['fb_idp'])>0):
        idps += "\n      {{type: 'FACEBOOK', id: '{}'}},".format(conf['fb_idp'])
    if conf['lnkd_idp'] is not None and (len(conf['lnkd_idp'])>0):
        idps += "\n      {{type: 'LINKEDIN', id: '{}'}},".format(conf['lnkd_idp'])
    idps += ']'

    btns = '['
    if conf['saml_idp'] and (len(conf['saml_idp'])>0):
        if conf['saml_idp'] is not None:
            btns += "{title: 'Login SAML Idp',\n" \
                    + "        className: 'btn-customAuth',\n" \
                    + "        click: function() {\n" \
                    + "          var link =  '{issuer}/v1/authorize'\n".format(
                issuer='https://' + conf['org'] + '/oauth2/' + conf['iss']) \
                    + "          + '?response_type=code'\n" \
                    + "          + '&client_id={client_id}'\n".format(client_id=conf['aud']) \
                    + "          + '&scope=openid+email+profile'\n" \
                    + "          + '&redirect_uri={redirect}'\n".format(redirect=conf['redirect_uri']) \
                    + "          + '&state=foo'\n" \
                    + "          + '&nonce=foo'\n" \
                    + "          + '&idp={idp_id}'\n".format(idp_id=conf['saml_idp']) \
                    + "          window.location.href = link;\n" \
                    + "        }\n" \
                    + "    }"
    btns += ']'

    page = 'login_idp'
    request.session['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        conf = _update_conf(request, {"js": _do_format(request, '/js/oidc_idp.js', page, idps=idps, btns=btns)})
    return render(request, 'index_idp.html', conf)


# Demo: IdP discovery
@csrf_exempt
def view_login_disco(request):
    conf = _get_config(request, 'disco')
    page = 'login_idp_disco'
    request.session['entry_page'] = page
    if request.method == 'POST':
        return _do_refresh(request, page)
    else:
        conf = _update_conf(request, {"js": _do_format(request, '/js/idp_discovery.js', page, embed_link=conf['idp_disco_page'])})
    return render(request, 'index_idp_disco.html', conf)


def view_admin(request):
    conf = _get_config(request, 'admin')
    if not is_admin(request):
        return HttpResponseRedirect(reverse('not_authorized'))

    if can_delegate(request):
        _update_conf(request, {"allow_impersonation": True, "js": ""})

    return render(request, 'admin.html', conf)


def view_logout(request):
    conf = _get_config(request, 'logout')
    if 'entry_page' in request.session:
        page = 'login' if request.session['entry_page'] == 'okta_hosted_login' else request.session['entry_page']
    else:
        page = 'login'

    logout(request)

    conf.update({"page": reverse(page)})
    print('logout back to page {}'.format(conf['page']))
    return render(request, 'logged_out.html', conf)


def clear_session(request):
    conf = _get_config(request, 'logout')
    logout_all(request)
    return render(request, 'logged_out.html', conf)


# Sample custom registration form
def registration_view(request):
    cfg = _get_config(request, 'reg')
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
            client = UsersClient('https://' + cfg['org'], config.get_api_key(request))
            client.create_user(user=user, activate="false")

        try:
            print('create user {0} {1}'.format(fn, ln))

            return HttpResponseRedirect(reverse('registration_success'))
        except Exception as e:
            print("Error: {}".format(e))
            form.add_error(field=None, error=e)

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def registration_view2(request):
    cfg = _get_config(request, 'reg2')
    if request.method == 'POST':
        form = RegistrationForm2(request.POST)
        if form.is_valid():
            fn = form.cleaned_data['firstName']
            ln = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            user = {
                "profile": {
                    "firstName": fn,
                    "lastName": ln,
                    "email": email,
                    "login": email
                }
            }
            client = UsersClient('https://' + cfg['org'], config.get_api_key(request))
            client.create_user(user=user, activate="false")
        try:
            print('create user {0} {1}'.format(fn, ln))
            return HttpResponseRedirect(reverse('registration_success2'))
        except Exception as e:
            print("Error: {}".format(e))
            form.add_error(field=None, error=e)
    else:
        form = RegistrationForm2()
    return render(request, 'register2.html', {'form': form})


def activation_view(request, slug):
    cfg = _get_config(request, 'activate')
    name = None
    username = None
    user_id = None
    if slug:
        auth = AuthClient('https://' + cfg['org'])
        response = auth.recovery(slug)
        if response.status_code == 200:
            user = json.loads(response.content)['_embedded']['user']
            name = user['profile']['firstName']
            username = user['profile']['login']
            user_id = user['id']
        else:
            return HttpResponseRedirect(reverse('not_authenticated'))

    if request.method == 'POST':
        if user_id is None:
            return HttpResponseRedirect(reverse('not_authenticated'))

        try:
            form = ActivationForm(request.POST)
            if form.is_valid():
                pw = form.cleaned_data['password1']
                user = {
                    "credentials": {
                        "password": {"value": pw}
                    }
                }
                client = UsersClient('https://' + cfg['org'], config.get_api_key(request))
                client.set_password(user_id=user_id, user=user)
                res = auth.authn(username, pw)
                if res.status_code == 200:
                    session_token = json.loads(res.content)['sessionToken']
                    return redirect('https://{0}{1}?sessionToken={2}'.format(cfg['org'], cfg['login_noprompt_bookmark'], session_token))
                    # FIXME: login_noprompt_bookmark is deprecated

            return HttpResponseRedirect(reverse('registration_success'))
        except Exception as e:
            print("Error: {}".format(e))
            form.add_error(field=None, error=e)
    else:
        form = ActivationForm()
    return render(request, 'activate.html', {'form': form, 'slug': slug, 'firstName': name})


# A custom registration flow where user is created STAGED. Then an OTP is sent via Email to activate the account
def activation_wo_token_view(request):
    cfg = _get_config(request, 'activate2')
    state = None
    if request.method == 'POST':
        form = ActivationWithEmailForm(request.POST)
        if form.is_valid():
            state = request.session['activation_state']
            print('state={}'.format(state))

            email = form.cleaned_data['email']
            print('email={}'.format(email))
            otp = form.cleaned_data['verificationCode']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            client = UsersClient('https://' + cfg['org'], config.get_api_key(request))
            user = json.loads(client.get_user(email))

            if state == 'verify-email':
                for key in list(request.session.keys()):
                    if key in ['activation_state', 'email_factor_id', 'verification_username', 'verification_user_id']:
                        del request.session[key]

                request.session['activation_state'] = 'verify-token'
                if user['status'] == 'STAGED':
                    enroll_status = client.enroll_email_factor(user['id'], email)
                    #if enroll_status.status_code == 200:
                    response = client.list_factors(user['id'])
                    factors = json.loads(response)
                    for factor in factors:
                        if factor['factorType'] == 'email':
                            request.session['email_factor_id'] = factor['id']
                            request.session['verification_username'] = email
                            request.session['verification_user_id'] = user['id']
                            client.verify_email_factor(user['id'], factor['id'])
                            break

            elif state == 'verify-token':
                request.session['activation_state'] = 'set-password'
                response = client.verify_email_factor(user_id=request.session['verification_user_id'],
                                                      factor_id=request.session['email_factor_id'],
                                                      pass_code=otp)
            elif state == 'set-password':
                payload = {
                    "credentials": {
                        "password": {"value": password1}
                    }
                }
                setpassword = client.set_password(user_id=request.session['verification_user_id'], user=payload)
                activate = client.activate(user_id=request.session['verification_user_id'])
                auth = AuthClient('https://' + cfg['org'])
                res = auth.authn(request.session['verification_username'], password1)
                if res.status_code == 200:
                    session_token = json.loads(res.content)['sessionToken']
                    return redirect('https://{0}{1}?sessionToken={2}'.format(cfg['org'], cfg['idp_disco_page'], session_token))
                    # FIXME: idp_disco_page is deprecated

        else:
            print('invalid form')
    else:
        state = 'verify-email'
        request.session['activation_state'] = state
        form = ActivationWithEmailForm()

    return render(request, 'activate_w_email.html', {'form': form, 'state': state})


def registration_success(request):
    return render(request, 'success.html')


def registration_success2(request):
    return render(request, 'success2.html')


def oauth2_callback(request):
    return render(request, 'oauth2_callback.html')


@csrf_exempt
def oauth2_post(request):
    conf = _get_config(request, 'oauth2')
    access_token = None
    id_token = None
    code = None
    if request.method == 'POST':
        print('POST request: {}'.format(request.POST))
        if 'code' in request.POST:
            code = request.POST['code']
        if 'access_token' in request.POST:
            access_token = request.POST['access_token']
        if 'id_token' in request.POST:
            id_token = request.POST['id_token']
    elif request.method == 'GET':
        print('GET request: {}'.format(request.GET))
        if 'code' in request.GET:
            code = request.GET['code']
        if 'state' in request.GET:
            state = request.GET['state']

    if code:
        client = OAuth2Client('https://' + conf['org'], conf['iss'], conf['aud'], config.get_client_secret(request))
        tokens = client.token(code, conf['redirect_uri'])
        print('Tokens from the code retrieval {}'.format(tokens))
        if tokens['access_token']:
            access_token = tokens['access_token']
        if tokens['id_token']:
            id_token = tokens['id_token']

    if access_token:
        # In the real world, you should validate the access_token. But this demo app is going to skip that part.
        print('access_token = {}'.format(access_token))
        client = OAuth2Client('https://' + conf['org'], conf['iss'])
        profile = client.profile(access_token)
        set_profile(request, profile)
        set_access_token(request, access_token)

    if id_token:
        # In the real world, you should validate the id_token. But this demo app is going to skip that part.
        print('id_token = {}'.format(id_token))
        set_id_token(request, id_token)

    return HttpResponseRedirect(reverse('home'))


# IMPERSONATION Demo
@csrf_exempt
def delegate_init(request):
    cfg = _get_config(request, 'delegate')
    if request.method == 'POST':
        client = OktadelegateClient(cfg['delegation_service_endpoint'],
                                    request.META["HTTP_AUTHORIZATION"].split(" ")[1],
                                    config.get_api_key(request))
        result = client.delegate_init(json.loads(request.body)["delegation_target"])
        return JsonResponse(json.loads(result.content))


@csrf_exempt
def process_creds(request):
    print('#####################################PROCESS CREDS START#####################################')
    print(request.POST)
    time_to_sleep = 5
    start = time.ctime()
    print("Start : %s" % start)
    time.sleep(time_to_sleep)
    end = time.ctime()
    print("End : %s" % end)
    print('#####################################PROCESS CREDS END#####################################')

    response = HttpResponse()
    response.content = 'Slept for {0} seconds. Start time: {1} - End time: {2}'.format(time_to_sleep, start, end)
    response.status_code = 200
    return response


# IMPERSONATION Demo (Deprecated)
# def login_delegate(request):
#     cfg = _get_config(request)
#     if 'profile' in request.session:
#         del request.session['profile']
#     for key in list(request.session.keys()):
#         del request.session[key]
#
#     cfg.update({"js": _do_format(request, '/js/login-delegate.js', 'login_delegate')})
#     return render(request, 'login_delegate.html', cfg)

# def view_login_baybridge(request):
#     return render(request, 'z-login-baybridge.html');

# def view_login_brooklynbridge(request):
#     return render(request, 'z-login-brooklynbridge.html');

# def hellovue(request):
#     return render(request, 'z-hellovue.html');


# def proxy_callback(request):
#     if 'profile' in request.session:
#         del request.session['profile']
#     for key in list(request.session.keys()):
#         del request.session[key]
#     return render(request, 'z-proxy-callback.html')


# @csrf_exempt
# def auth_broker(request):
#     print(request)
#     cookies = request.COOKIES
#     print('cookie: {}'.format(cookies))
#
#     response = HttpResponse()
#     response.status_code = 200
#
#     if request.method == 'POST':
#         body = json.loads(request.body)
#         username = body['username']
#         password = body['password']
#         auth = AuthClient('https://' + OKTA_ORG)
#         res = auth.authn(username, password)
#         print('status={}'.format(res.status_code))
#         response.status_code = res.status_code
#
#         content = json.dumps(res.json())
#         print('response={}'.format(content))
#         response.content = content
#
#         return response
#
#     return response
#
#
# def sessions_broker(request):
#     print(request)
#     response = HttpResponse()
#     response.status_code = 200
#
#     cookies = request.COOKIES
#     print('cookie: {}'.format(cookies))
#
#     auth = SessionsClient('https://' + OKTA_ORG)
#     res = auth.me()
#     response.status_code = res.status_code
#     content = json.dumps(res.json())
#     print('response={}'.format(content))
#     response.content = content
#
#     return response

# def view_debug(request):
#     return render(request, 'debug.html', {'meta': request.META})
