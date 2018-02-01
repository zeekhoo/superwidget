FROM python:3.4-alpine
RUN mkdir /okta_api_demo
WORKDIR /okta_api_demo
ADD . /okta_api_demo
RUN pip install -r requirements.txt
RUN python manage.py migrate
EXPOSE 8000
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]