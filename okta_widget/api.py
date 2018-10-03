from okta_widget.decorators import access_token_required
from django.views.decorators.csrf import csrf_exempt

from okta_widget.client.users_client import UsersClient
from okta_widget.client.groups_client import GroupsClient
from okta_widget.client.apps_client import AppsClient

from okta_widget.views import OKTA_ORG
from okta_widget.views import API_KEY
from okta_widget.views import CLIENT_ID

from okta_widget.views import IMPERSONATION_VERSION
from okta_widget.views import IMPERSONATION_SAML_APP_ID
from okta_widget.views import IMPERSONATION_V2_ORG
from okta_widget.views import IMPERSONATION_V2_ORG_API_KEY
from okta_widget.views import IMPERSONATION_V2_SAML_APP_ID
from okta_widget.views import not_authorized

from django.http import HttpResponseRedirect, HttpResponse
from .authx import api_access_admin
from .authx import api_access_company_admin

import json
import datetime


@access_token_required
def list_users(request, token):
    get = request.GET
    startsWith = None
    if 'startsWith' in get:
        startsWith = get['startsWith']

    client = UsersClient('https://' + OKTA_ORG, API_KEY)
    profile_dict = request.session['profile']
    #profile_dict = json.loads(profile)
    companyName = profile_dict.get('companyName')

    if api_access_admin(token):
        users = client.list_users(15, startsWith)
    elif api_access_company_admin(token):
        users = client.list_users_scoped(15, companyName, startsWith)
    else:
        return not_authorized(request)

    response = HttpResponse()
    response.status_code = 200
    response.content = users
    return response


@access_token_required
def list_user(request, token):
    get = request.GET
    user_id = None
    if 'user' in get:
        user_id = get['user']
    client = UsersClient('https://' + OKTA_ORG, API_KEY)

    if api_access_admin(token) or api_access_company_admin(token):
        users = client.list_user(user_id)
    else:
        return not_authorized(request)

    response = HttpResponse()
    response.status_code = 200
    response.content = users
    return response


@csrf_exempt
@access_token_required
def add_users(request, token):
    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST

        email = ''
        firstName = ''
        lastName = ''
        role = ''
        activate = False

        #profile_dict = json.loads(request.session['profile'])
        profile_dict = request.session['profile']
        companyName = ''
        if 'companyName' in profile_dict:
            companyName = profile_dict.get('companyName')

        if 'email' in req:
            email = req['email']
        if 'firstName' in req:
            firstName = req['firstName']
        if 'lastName' in req:
            lastName = req['lastName']
        if 'role' in req:
            role = req['role']
        if 'activate' in req:
            activate = req['activate']
        client = UsersClient('https://' + OKTA_ORG, API_KEY)

        user = {
            "profile": {
                "firstName": firstName,
                "lastName": lastName,
                "email": email,
                "login": email,
                "customer_role": role,
                "companyName": companyName
            }
        }

        if api_access_admin(token):
            users = client.create_user(user=user, activate=activate)
        elif api_access_company_admin(token):
            users = client.create_user(user=user, activate=activate)
            # users = client.create_user_scoped(user=user, activate="false", group="")
        else:
            return not_authorized(request)

        response.content = users

    return response


@csrf_exempt
@access_token_required
def update_user(request, token):
    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST

        if 'user_id' in req:
            user_id = req['user_id']

            email = ''
            firstName = ''
            lastName = ''
            role = ''
            companyName = ''
            deactivate = None

            if 'email' in req:
                email = req['email']
            if 'firstName' in req:
                firstName = req['firstName']
            if 'lastName' in req:
                lastName = req['lastName']
            if 'role' in req:
                role = req['role']
            if 'deactivate' in req:
                deactivate = req['deactivate']
            if 'companyName' in req:
                companyName = req['companyName']
            client = UsersClient('https://' + OKTA_ORG, API_KEY)

            user = {
                "profile": {
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email,
                    "login": email,
                    "customer_role": role,
                    "companyName": companyName
                }
            }

            if api_access_admin(token):
                users = client.update_user(user=user, user_id=user_id, deactivate=deactivate)
            elif api_access_company_admin(token):
                users = client.update_user(user=user, user_id=user_id, deactivate=deactivate)
            else:
                return not_authorized(request)

            response.content = users

    return response


@access_token_required
def list_groups(request, token):
    response = HttpResponse()
    response.status_code = 200

    profile_dict = request.session['profile']
    #profile_dict = json.loads(profile)
    companyName = ''
    if 'companyName' in profile_dict:
        companyName = profile_dict.get('companyName')

    if api_access_company_admin(token):
        client = GroupsClient('https://' + OKTA_ORG, API_KEY)
        response.content = client.list_groups(15, companyName)
    else:
        return not_authorized(request)

    return response


@access_token_required
def get_group(request, token):
    get = request.GET
    response = HttpResponse()
    response.status_code = 200

    group_id = None
    if 'group_id' in get:
        group_id = get['group_id']
    client = GroupsClient('https://' + OKTA_ORG, API_KEY)

    if api_access_company_admin(token):
        response.content = client.get_group_by_id(group_id)
    else:
        return not_authorized(request)

    return response


@access_token_required
def app_schema(request, token):
    response = HttpResponse()
    response.status_code = 200

    if api_access_company_admin(token):
        client = AppsClient('https://' + OKTA_ORG, API_KEY, CLIENT_ID)
        schema = client.get_schema()
        response.content = schema
    else:
        return not_authorized(request)

    return response


@access_token_required
def list_perms(request, token):
    get = request.GET
    response = HttpResponse()
    response.status_code = 200

    if api_access_company_admin(token):
        client = AppsClient('https://' + OKTA_ORG, API_KEY, CLIENT_ID)

        group_id = None
        if 'group_id' in get:
            group_id = get['group_id']

        perms = client.get_app_group_by_id(group_id)
        response.content = perms
    else:
        return not_authorized(request)

    return response


@csrf_exempt
@access_token_required
def update_perm(request, token):
    req = request.POST

    group_id = None
    perms = None

    if 'group_id' in req:
        group_id = req['group_id']
    if 'perms' in req:
        perms = req['perms']

    response = HttpResponse()
    response.status_code = 200

    if api_access_company_admin(token) and group_id and group_id and perms:
        if perms[-1:] == ',':
            perms = perms[:-1]
        perms = perms.split(',')
        print(perms)

        perm = {
            "profile": {
                "role_permissions": perms
            }
        }

        client = AppsClient('https://' + OKTA_ORG, API_KEY, CLIENT_ID)
        perms = client.update_app_group(group_id, perm)
        response.content = perms
    else:
        return not_authorized(request)
    return response


@csrf_exempt
@access_token_required
def add_group(request, token):
    response = HttpResponse()
    response.status_code = 200

    if request.method == 'POST':
        req = request.POST
        profile_dict = request.session['profile']
        #profile_dict = json.loads(profile)

        if 'groupName' in req and 'companyName' in profile_dict:
            prefix = None
            if 'companyName' in profile_dict:
                prefix = profile_dict.get('companyName')
                if prefix == '':
                    prefix = None

            group_name = req['groupName']
            if prefix:
                group_name = prefix + '_' + group_name

            client = GroupsClient('https://' + OKTA_ORG, API_KEY)

            group = {
                "profile": {
                    "name": group_name,
                }
            }

            if api_access_admin(token):
                response.content = client.create_group(group)
            elif api_access_company_admin(token):
                response.content = client.create_group(group)
            else:
                return not_authorized(request)

    return response

# IMPERSONATION Demo
@csrf_exempt
@access_token_required
def setNameId(request, token):
    post = request.POST
    print(post)

    response = HttpResponse()
    if 'nameid' in post:
        name_id = post['nameid']
        admin = request.session['profile']['preferred_username']

        version = '{}'.format(IMPERSONATION_VERSION)
        if version == "1":
            client = AppsClient('https://' + OKTA_ORG, API_KEY, IMPERSONATION_SAML_APP_ID)
            response.status_code = client.set_name_id(request.session['id_token']['sub'], name_id)
        if version == "2":

            u_client = UsersClient('https://' + OKTA_ORG, API_KEY)
            target = u_client.list_user(name_id)
            target = json.loads(target)
            target_profile = target["profile"]
            target_groups = u_client.get_user_groups(target["id"])
            target_groups = json.loads(target_groups)
            groupsIds = []
            for g in target_groups:
                if g["type"] != 'BUILT_IN':
                    groupsIds.append(g["id"])

            now = datetime.datetime.now()
            new_login = "IM" + now.strftime('%Y%m%d%H%M%S') + admin.split("@")[0].replace(".", "") + "AS" + target_profile["login"]
            target_profile["login"] = new_login
            target_profile["email"] = new_login
            temp_user = {
                "profile": target_profile,
                "groupIds": groupsIds
            }
            u_client.create_user(user=temp_user, activate=True)

            u_client = UsersClient('https://' + IMPERSONATION_V2_ORG, IMPERSONATION_V2_ORG_API_KEY)
            users = u_client.list_user(admin)
            users = json.loads(users)
            if "id" in users:
                client = AppsClient('https://' + IMPERSONATION_V2_ORG, IMPERSONATION_V2_ORG_API_KEY, IMPERSONATION_V2_SAML_APP_ID)
                response.status_code = client.set_name_id(users["id"], new_login)
                for key in list(request.session.keys()):
                    del request.session[key]
    return response
