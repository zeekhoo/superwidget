# Okta-API-Demo

This sample project provides an easy to deploy demo app which 
demonstrates out-of-the-box features of Okta API Products.
It showcases the Signin Widget, but also contains one sample each for
log-in using 2 other integration methods: 1) by redirecting to Okta's signin page and 2)
purely using API (AuthJS example). This application provides the presenter the ability to demonstrate:

1. Authentication and Authorization:
2. Inbound Federation (SAML)
3. Social Auth
4. MFA
5. Universal Directory
6. Centralized Identity Management
7. API Access Management


#### This project is built with Django and runs on Python 3.4.
You can either run the django app locally by cloning this repo or even more conveniently, use an available Docker container.

## 1. Run in Docker
There is a Docker container so you can readily run the app with `Docker run`. 
But first you need to provide the container with environment variables. 

1. Create a directory/folder and `cd` into it. 
2. In this directory, create a file named "env.list". 
    There is already a template env.list file in the root of this project repo, 
    so simply copy it and edit it:
    * Edit "env.list" file and provide values to your Okta API-Products configuration values. 
        Note: comments begin with an "#". Be sure to read the comments.
    * You don't need to update all the variables in "env.list", **only the first 5** (And these are clearly marked out in the template env.list file). 
    You can edit the other environment variables to suit the custom needs of your demo, but for out-of-the-box setup, the default values should work fine.
    
   Example completed in env.list looks like the following
   (Note: keys and secrets below are made-up values):
    ```
    AUTH_SERVER_ID=aus8sghq3euRD33KN0h7
    OKTA_ORG=atko.okta.com
    CLIENT_ID=0oa4ox4jzjHj9vWgR1t7
    CLIENT_SECRET=Ar-zht2498sdfxaerjwmsjd9s!je49rw8#a
    API_KEY=00xcfd2308490aeuxcvbEarsddffffdgjfhgf012xz
    DEFAULT_SCOPES=openid,email,profile,com.zeek.p1.resource1.admin,com.zeek.p1.resource1.user
    REDIRECT_URI=http://localhost:8000/oauth2/callback
    CUSTOM_LOGIN_URL=login.atko.com
    GOOGLE_IDP_ID=0oa1bnct4t7RQEwao1t7
    FB_IDP_ID=0oaxmxaszOUXlhDAu1t6
    LNKD_IDP_ID=0oatmj8l3QhUvJ3lQ1t6
    SAML_IDP_ID=0oayqdoj63vdxXHtI1t6
    BACKGROUND_IMAGE=/static/img/okta-brand/background/SFBayBridge.jpg
    BACKGROUND_IMAGE_CSS=/static/img/okta-brand/background/SFBayBridge.jpg
    BACKGROUND_IMAGE_AUTHJS=/static/img/okta-brand/background/focus.jpg
    BACKGROUND_IMAGE_IDP=/static/img/okta-brand/background/NewYork.jpg    
    ```

3. In Okta, configure your App to support both **authorization_code** and **Implicit** flow. Also, be sure to check both boxes ***"Allow ID Token with Implicit grant type"*** and ***"Allow Access Token with implicit grant type"***

4. In your Okta org, you must add CORS and a redirect_uri for your application. 
    Please add the following to your Okta org:
    * Add redirect_uri = `http://localhost:8000/oauth2/callback` to your OpenID Connect app
    * Add a CORS entry for ``http://localhost:8000``

5. Run

    Run the command
    ```
    docker run -it -p 8000:8000 --env-file=env.list -t zzkhoo/okta-api-demo:latest
    ```
    Notes: This project has a Dockerfile which you can use to build your own images. Or, you can
    simply run okta-api-demo from the public repo [https://hub.docker.com/r/zzkhoo/okta-api-demo/tags/] as shown above. 
    Also note: The Dockerfile exposes the project on port 8000, so map your port to 8000. 
    And be sure to inject the env.list into your container with the --env-file option as shown. 

### Demoing Idp Discovery
This app can demo IdP discovery, but there are some configuration steps to take care of. To demo IdP Discovery:
1. Add the settting IDP_DISCO_PAGE in env.list. Set it to the relative path of your App's EMBED_LINK: Example
    ```
    AUTH_SERVER_ID=....
    OKTA_ORG=...
    ...
    IDP_DISCO_PAGE=/home/oidc_client/0oa4ox4jzjHj9vWgR1t7/alntwmdyyUB5fs8d50g4
    ```
    
2. In Okta, configure your OIDC App's settings with the following:

    Login Initiated by = `Either Okta or App`

    Initiate login URI = `http://localhost:8000/login-disco`
    
3. Now you should see an "Idp Discovery" tab in the demo app. 
    
## 2. Local setup
You can also run locally:

1. Clone this repository. Then 'cd' into its directory.
2. Create a virtualenv environment.
    ```
    python3 -m venv venv
    ```
    or
    ```
    virtualenv -p <path-to-Python3.4> venv
    ```
3. Activate the virtualenv
    ```
    source venv/bin/activate
    ```
4. Install requirements
    ```
    pip install -r requirements.txt
    ```
5. Edit the ".env" file and provide values to your Okta API-Products configuration values. 
6. An example of a completed .env file looks like the following
   (Note: keys and secrets below are made-up values):
    ````
    export AUTH_SERVER_ID=default
    export OKTA_ORG=atko.okta.com
    export CLIENT_ID=0oa4ox4jzjHj9vWgR1t7
    export CLIENT_SECRET=Ar-zht2498sdfxaerjwmsjd9s!je49rw8#a
    export API_KEY=00xcfd2308490aeuxcvbEarsddffffdgjfhgf012xz    
    export DEFAULT_SCOPES=openid,email,profile,com.zeek.p1.resource1.admin,com.zeek.p1.resource1.user
    export REDIRECT_URI=http://localhost:8000/oauth2/callback
    export CUSTOM_LOGIN_URL=login.atko.com    
    export GOOGLE_IDP_ID=0oa1bnct4t7RQEwao1t7
    export FB_IDP_ID=0oaxmxaszOUXlhDAu1t6
    export LNKD_IDP_ID=0oatmj8l3QhUvJ3lQ1t6
    export SAML_IDP_ID=0oayqdoj63vdxXHtI1t6
    export BACKGROUND_IMAGE=/static/img/okta-brand/background/SFBayBridge.jpg
    export BACKGROUND_IMAGE_CSS=/static/img/okta-brand/background/SFBayBridge.jpg
    export BACKGROUND_IMAGE_AUTHJS=/static/img/okta-brand/background/focus.jpg
    export BACKGROUND_IMAGE_IDP=/static/img/okta-brand/background/NewYork.jpg   
    ````
7. Source the .env file
    ```
    source .env
    ```
8. Make migrations
    ```
    python manage.py migrate
    ```
9. Start the server
    ```
    python manage.py runserver
    ```

