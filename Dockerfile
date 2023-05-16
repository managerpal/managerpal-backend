FROM pywps/gunicorn-alpine
WORKDIR /home/managerpal

COPY ./managerpal /home/managerpal

EXPOSE 