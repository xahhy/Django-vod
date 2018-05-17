FROM python:3.6

WORKDIR /app

COPY requirements.txt /app/

# RUN apk add --no-cache curl libxml2-dev libxslt-dev \
#  libjpeg-turbo-dev libffi-dev musl-dev libgcc \
#  zlib-dev openssl-dev jpeg-dev freetype-dev lcms2-dev \
#  gcc openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install -r /app/requirements.txt

COPY . /app

ENV DJANGO_PORT=8000 \
  DJANGO_LOG=$PWD \
  DJANGO_DB_HOST=vod_db \
  TSRTMP_DB_HOST=vod_db \
  NAME="mysite_app" \
  # Name of the application
  ADDRESS=0.0.0.0 \
  LOG_DIR=logs \
  ERROR_LOG=error.log \
  PID_FILE=logs/vod.pid \
  NUM_WORKERS=4 \
  # how many worker processes should Gunicorn spawn
  TIME_OUT=900000 \
  #set time out!!!!!
  DJANGO_SETTINGS_MODULE=mysite.settings \
  # which settings file should Django use
  DJANGO_WSGI_MODULE=mysite.wsgi
  # WSGI module name


HEALTHCHECK --interval=30s --timeout=3s CMD curl -fs http://localhost:$DJANGO_PORT/admin || exit 1

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]
