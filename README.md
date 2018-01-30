# Okta-API-Demo

#### This project is built on Django and it runs on Python 3.4.

## Run in Docker
There is a Docker container so you can readily run the app with `Docker run`. 
But first you need to provide the container with environment variables. 

1. Create a directory/folder and `cd` into it. 
2. In this directory, create a file named "env.list". 
    There is already a template env.list file in the root of this project repo, 
    so simply copy it and edit it:
    * Edit "env.list" file and provide values to your Okta API-Products configuration values. 
        Note: comments begin with an "#". Be sure to read the comments.
    * Not all the variables in the "env.list" are required. For example, Social Idp and External SAML Idp settings are optional.
   Example completed in env.list looks like the following
   (Note: keys and secrets below are made-up values):
    ```
    AUTH_SERVER_ID=default
    OKTA_ORG=atko.okta.com
    CLIENT_ID=0oa4ox4jzjHj9vWgR1t7
    CLIENT_SECRET=Ar-zht2498sdfxaerjwmsjd9s!je49rw8#a
    API_KEY=00xcfd2308490aeuxcvbEarsddffffdgjfhgf012xz
    DEFAULT_SCOPES=openid,email,profile,com.zeek.p1.resource1.admin,com.zeek.p1.resource1.user
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

3. In your Okta org, you must add CORS and a redirect_uri for your application. 
    Please add the following to your Okta org:
    * Add redirect_uri = `http://localhost:8000/oauth2/callback` to your OpenID Connect app
    * Add a CORS entry for ``http://localhost:8000``

4. Run

    Run the command
    ```
    docker run -p 8000:8000 --env-file=env.list -t zzkhoo/okta-api-demo:v1.2
    ```
    Notes: This project has a Dockerfile which you can use to build your own images. Or, you can
    simply run okta-api-demo from the public repo [https://hub.docker.com/r/zzkhoo/okta-api-demo/tags/] as shown above. 
    Also note: The Dockerfile exposes the project on port 8000, so map your port to 8000. 
    And be sure to inject the env.list into your container with the --env-file option as shown. 

## Local setup
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

