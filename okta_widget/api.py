import json
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from okta_widget.decorators import access_token_required

from okta_widget.client.users_client import UsersClient
from okta_widget.client.groups_client import GroupsClient
from okta_widget.client.apps_client import AppsClient

from okta_widget.views import not_authorized, config, _get_config

from .authx import api_access_admin, api_access_company_admin, parse_bearer_token
from .authx import transfer_authorization
from .client.oktadelegate_client import OktadelegateClient


@csrf_exempt
@access_token_required
def transfer_money(request, token):
    post_data = request.POST
    authorized_amount = transfer_authorization(request, token)
    requested_amount = int(post_data['amount'])
    response = HttpResponse("", content_type="application/json; charset=utf-8")
    if requested_amount <= authorized_amount:
        retVal = '{"Status":"SUCCESS", "Message":"Success! Money has been transferred."}'
        response.status_code = 200
    else:
        retVal = '{{"Status":"FAILURE", "Message":"You are unauthorized to transfer this amount of money. Requested: {}, Authorized: {}"}}'.format(requested_amount, authorized_amount)
        response.status_code = 403

    response.content = retVal
    return response


@access_token_required
def list_users(request, access_token):
    conf = _get_config(request)
    get = request.GET
    starts_with = None
    if 'startsWith' in get:
        starts_with = get['startsWith']

    client = UsersClient('https://' + conf['org'], config.get_api_key(request))

    is_org_token = False
    try:
        token_obj = parse_bearer_token(access_token)
        if token_obj['iss'] == 'https://{0}'.format(conf['org']):
            is_org_token = True
    except Exception as e:
        print(e)

    if is_org_token:
        client.set_bearer_token(access_token)
        users = client.list_users(15, starts_with)
    else:
        profile_dict = request.session['profile']
        company_name = profile_dict.get('companyName')
        if api_access_admin(conf, access_token):
            users = client.list_users(15, starts_with)
        elif api_access_company_admin(conf, access_token):
            users = client.list_users_scoped(15, company_name, starts_with)
        else:
            return not_authorized(request)

    response = HttpResponse()
    response.status_code = 200
    response.content = users
    return response


@access_token_required
def list_user(request, access_token):
    conf = _get_config(request)
    get = request.GET
    user_id = None
    if 'user' in get:
        user_id = get['user']
    client = UsersClient('https://' + conf['org'], config.get_api_key(request))

    if api_access_admin(conf, access_token) or api_access_company_admin(conf, access_token):
        users = client.list_user(user_id)
    else:
        return not_authorized(request)

    response = HttpResponse()
    response.status_code = 200
    response.content = users
    return response


@access_token_required
def add_users(request, access_token):
    conf = _get_config(request)

    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST

        email = ''
        first_name = ''
        last_name = ''
        role = ''
        activate = False

        profile_dict = request.session['profile']
        company_name = ''
        if 'companyName' in profile_dict:
            company_name = profile_dict.get('companyName')

        if 'email' in req:
            email = req['email']
        if 'firstName' in req:
            first_name = req['firstName']
        if 'lastName' in req:
            last_name = req['lastName']
        if 'role' in req:
            role = req['role']
        if 'activate' in req:
            activate = req['activate']
        client = UsersClient('https://' + conf['org'], config.get_api_key(request))

        user = {
            "profile": {
                "firstName": first_name,
                "lastName": last_name,
                "email": email,
                "login": email,
                "customer_role": role,
                "companyName": company_name
            }
        }

        if api_access_admin(conf, access_token):
            users = client.create_user(user=user, activate=activate)
        elif api_access_company_admin(conf, access_token):
            users = client.create_user(user=user, activate=activate)
        else:
            return not_authorized(request)

        response.content = users

    return response


@access_token_required
def update_user(request, access_token):
    conf = _get_config(request)

    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST

        if 'user_id' in req:
            user_id = req['user_id']

            email = ''
            first_name = ''
            last_name = ''
            role = ''
            company_name = ''
            deactivate = None

            if 'email' in req:
                email = req['email']
            if 'firstName' in req:
                first_name = req['firstName']
            if 'lastName' in req:
                last_name = req['lastName']
            if 'role' in req:
                role = req['role']
            if 'deactivate' in req:
                deactivate = req['deactivate']
            if 'companyName' in req:
                company_name = req['companyName']
            client = UsersClient('https://' + conf['org'], config.get_api_key(request))

            user = {
                "profile": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "login": email,
                    "customer_role": role,
                    "companyName": company_name
                }
            }

            if api_access_admin(conf, access_token):
                users = client.update_user(user=user, user_id=user_id, deactivate=deactivate)
            elif api_access_company_admin(conf, access_token):
                users = client.update_user(user=user, user_id=user_id, deactivate=deactivate)
            else:
                return not_authorized(request)

            response.content = users

    return response


@access_token_required
def list_groups(request, access_token):
    conf = _get_config(request)

    response = HttpResponse()
    response.status_code = 200

    profile_dict = request.session['profile']
    company_name = ''
    if 'companyName' in profile_dict:
        company_name = profile_dict.get('companyName')

    if api_access_admin(conf, access_token):
        client = GroupsClient('https://' + conf['org'], config.get_api_key(request))
        response.content = client.list_groups(15)
    elif api_access_company_admin(conf, access_token):
        client = GroupsClient('https://' + conf['org'], config.get_api_key(request))
        response.content = client.list_groups(15, company_name)
    else:
        return not_authorized(request)

    return response


@access_token_required
def get_group(request, access_token):
    conf = _get_config(request)

    get = request.GET
    response = HttpResponse()
    response.status_code = 200

    group_id = None
    if 'group_id' in get:
        group_id = get['group_id']
    client = GroupsClient('https://' + conf['org'], config.get_api_key(request))

    if api_access_company_admin(conf, access_token):
        response.content = client.get_group_by_id(group_id)
    else:
        return not_authorized(request)

    return response


@access_token_required
def app_schema(request, access_token):
    conf = _get_config(request)

    response = HttpResponse()
    response.status_code = 200

    if api_access_company_admin(conf, access_token):
        client = AppsClient('https://' + conf['org'], config.get_api_key(request), conf['aud'])
        schema = client.get_schema()
        response.content = schema
    else:
        return not_authorized(request)

    return response


@access_token_required
def list_perms(request, access_token):
    conf = _get_config(request)

    get = request.GET
    response = HttpResponse()
    response.status_code = 200

    if api_access_admin(conf, access_token) or api_access_company_admin(conf, access_token):
        client = AppsClient('https://' + conf['org'], config.get_api_key(request), conf['aud'])

        group_id = None
        if 'group_id' in get:
            group_id = get['group_id']

        perms = client.get_app_group_by_id(group_id)
        response.content = perms
    else:
        return not_authorized(request)

    return response


@access_token_required
def update_perm(request, access_token):
    conf = _get_config(request)

    req = request.POST

    group_id = None
    perms = None

    if 'group_id' in req:
        group_id = req['group_id']
    if 'perms' in req:
        perms = req['perms']

    response = HttpResponse()
    response.status_code = 200

    if (api_access_admin(conf, access_token) or api_access_company_admin(conf, access_token))\
            and group_id and group_id and perms:
        if perms[-1:] == ',':
            perms = perms[:-1]
        perms = perms.split(',')
        print(perms)

        perm = {
            "profile": {
                "role_permissions": perms
            }
        }

        client = AppsClient('https://' + conf['org'], config.get_api_key(request), conf['aud'])
        perms = client.update_app_group(group_id, perm)
        response.content = perms
    else:
        return not_authorized(request)
    return response


@access_token_required
def add_group(request, access_token):
    conf = _get_config(request)

    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST
        profile_dict = request.session['profile']

        if 'groupName' in req and 'companyName' in profile_dict:
            prefix = None
            if 'companyName' in profile_dict:
                prefix = profile_dict.get('companyName')
                if prefix == '':
                    prefix = None

            group_name = req['groupName']
            if prefix:
                group_name = prefix + '_' + group_name

            client = GroupsClient('https://' + conf['org'], config.get_api_key(request))

            group = {
                "profile": {
                    "name": group_name,
                }
            }

            if api_access_admin(conf, access_token):
                response.content = client.create_group(group)
            elif api_access_company_admin(conf, access_token):
                response.content = client.create_group(group)
            else:
                return not_authorized(request)

    return response


# IMPERSONATION Demo
@access_token_required
def delegate_init(request, access_token):
    cfg = _get_config(request, 'delegate')
    if request.method == 'POST':
        client = OktadelegateClient(cfg['delegation_service_endpoint'],
                                    request.META["HTTP_AUTHORIZATION"].split(" ")[1],
                                    config.get_api_key(request))
        result = client.delegate_init(json.loads(request.body)["delegation_target"])
        return JsonResponse(json.loads(result.content))

# IMPERSONATION Demo (Deprecated)
# @csrf_exempt
# @access_token_required
# def setNameId(request, token):
#     post = request.POST
#     print(post)
#
#     response = HttpResponse()
#     if 'nameid' in post:
#         name_id = post['nameid']
#         admin = request.session['profile']['preferred_username']
#
#         version = '{}'.format(cfg['impersonation_version'])
#         if version == "1":
#             client = AppsClient('https://' + cfg['org'], config.get_api_key(), cfg['impersonation_saml_app_id'])
#             response.status_code = client.set_name_id(request.session['id_token']['sub'], name_id)
#         if version == "2":
#             u_client = UsersClient('https://' + cfg['org'], config.get_api_key())
#             target = json.loads(u_client.list_user(name_id))
#             target_profile = target["profile"]
#             target_groups = json.loads(u_client.get_user_groups(target["id"]))
#             groupsIds = []
#             for g in target_groups:
#                 if g["type"] != 'BUILT_IN':
#                     groupsIds.append(g["id"])
#
#             now = datetime.datetime.now()
#             new_login = "IM" + now.strftime('%Y%m%d%H%M%S') + admin.split("@")[0].replace(".", "") + "AS" + target_profile["login"]
#             target_profile["login"] = new_login
#             target_profile["email"] = new_login
#             temp_user = {
#                 "profile": target_profile,
#                 "groupIds": groupsIds
#             }
#             u_client.create_user(user=temp_user, activate=True)
#
#             u_client = UsersClient('https://' + cfg['impersonation_v2_org'], cfg['impersonation_v2_org_api_key'])
#             users = u_client.list_user(admin)
#             users = json.loads(users)
#             if "id" in users:
#                 client = AppsClient('https://' + cfg['impersonation_v2_org'], cfg['impersonation_v2_org_api_key'], cfg['impersonation_v2_saml_app_id'])
#                 response.status_code = client.set_name_id(users["id"], new_login)
#                 for key in list(request.session.keys()):
#                     del request.session[key]
#     return response
