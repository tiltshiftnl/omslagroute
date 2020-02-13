FROM amsterdam/python
LABEL maintainer="datapunt@amsterdam.nl"

ENV PYTHONUNBUFFERED 1
ARG COMMIT=""
LABEL commit=${COMMIT}
ENV COMMIT_SHA=${COMMIT}

RUN adduser --system datapunt

RUN pip install --upgrade pip

# update
RUN apt-get update
# install curl
RUN apt-get install curl
# get install script and pass it to execute:
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
# and install node
RUN apt-get install nodejs

RUN mkdir -p /static && chown datapunt /static
RUN mkdir -p /app && chown datapunt /app
RUN mkdir -p /downloads && chown datapunt /downloads
RUN mkdir -p /certificates && chown datapunt /certificates
RUN mkdir -p /deploy && chown datapunt /deploy
RUN mkdir -p /var/log/uwsgi && chown datapunt /var/log/uwsgi

COPY . /app/
COPY deploy /deploy/

WORKDIR /app
RUN npm install
RUN ./node_modules/.bin/node-sass -o ./assets/bundles/ static_src/sass

# when using webpack uncomment line below
# RUN ./node_modules/.bin/webpack --config webpack.config.js


COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
USER datapunt

EXPOSE 8172

CMD ["/deploy/docker-run.sh"]
