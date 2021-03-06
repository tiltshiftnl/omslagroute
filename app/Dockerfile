FROM amsterdam/python
LABEL maintainer="datapunt@amsterdam.nl"

ENV PYTHONUNBUFFERED 1

ARG COMMIT_HASH
ARG BRANCH_NAME
ARG INVENTORY
ENV COMMIT_HASH=${COMMIT_HASH}
ENV BRANCH_NAME=${BRANCH_NAME}
ENV INVENTORY=${INVENTORY}

RUN adduser --system datapunt
RUN adduser datapunt sudo

# update
RUN apt-get update

RUN pip install --upgrade pip

RUN apt-get -y install locales

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

RUN sed -i -e 's/# nl_NL.UTF-8 UTF-8/nl_NL.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG nl_NL.UTF-8
ENV LANGUAGE nl_NL:nl
ENV LC_ALL nl_NL.UTF-8

WORKDIR /app

RUN npm install
RUN ./node_modules/.bin/node-sass -o ./assets/bundles/ static_src/sass
RUN ./node_modules/.bin/webpack --config webpack.config.js --mode production

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["/deploy/docker-run.sh"]
