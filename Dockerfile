FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
# Different src directory for pip to prevent 'pip install -e' packages to be installed in /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

COPY . /usr/src/app

# Install dockerize https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.2.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

CMD ["/usr/src/app/docker/cmd-run.sh"]
