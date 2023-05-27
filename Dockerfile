FROM python:3.11-alpine
WORKDIR /home/managerpal

COPY requirements.txt /home/managerpal/requirements.txt
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary
COPY ./managerpal /home/managerpal

WORKDIR /home/managerpal
# RUN pip install gunicorn

# RUN gunicorn -w 2 appcore/run
CMD python3 wsgi.py

EXPOSE 5000