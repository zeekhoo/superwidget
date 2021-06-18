FROM python:3.6
RUN mkdir /okta_api_demo
WORKDIR /okta_api_demo
ADD . /okta_api_demo
RUN pip install -r requirements.txt
RUN rm -f db.sqlite3
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
EXPOSE 8000

# CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]

# Use below when deploying
ENTRYPOINT ["gunicorn", "--bind", ":8000", "--workers", "8"]
CMD ["okta_widget.wsgi:application"]
