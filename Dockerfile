FROM python:3.9-slim-bullseye

WORKDIR /opt/trackmania_tracker
COPY dist/trackmania_tracker-3.2.2-py2.py3-none-any.whl .

RUN pip install --upgrade pip
RUN pip install waitress
RUN pip3 install trackmania_tracker-3.2.2-py2.py3-none-any.whl

VOLUME /opt/trackmania_tracker/data

ENV TRACK_PASSWORD=""
ENV TRACK_USERNAME=""
#CMD waitress-serve --port 8080 --url-scheme=https --host 0.0.0.0 --call trackmania_tracker:create_app
CMD flask --app trackmania_tracker run --debug --port 8080 --host 0.0.0.0