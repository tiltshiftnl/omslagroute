FROM amsterdam/python
LABEL maintainer="datapunt@amsterdam.nl"

ENV PYTHONUNBUFFERED 1
ARG COMMIT=""
LABEL commit=${COMMIT}
ENV COMMIT_SHA=${COMMIT}

RUN adduser --system datapunt
RUN adduser datapunt sudo

# update
RUN apt-get update

RUN pip install --upgrade pip

# install curl
RUN apt-get install -y curl
# get install script and pass it to execute:
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
# and install node
RUN apt-get install nodejs

# install nginx
RUN apt-get install -y nginx
# RUN apt-get install -y --no-install-recommends apt-utils

RUN mkdir -p /static
RUN mkdir -p /app
RUN mkdir -p /downloads
RUN mkdir -p /certificates
RUN mkdir -p /deploy
RUN mkdir -p /var/log/uwsgi
RUN mkdir -p /var/uwsgi/

COPY ./nginx/vhost.conf /etc/nginx/sites-enabled/
COPY . /app/
COPY deploy /deploy/

WORKDIR /app
RUN npm install
RUN ./node_modules/.bin/node-sass -o ./assets/bundles/ static_src/sass

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/deploy/docker-run.sh"]
