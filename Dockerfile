ARG ALPINE_VERSION=3.20
ARG PYTHON_VERSION=3.11
ARG PYTHON_TAG=${PYTHON_VERSION}-alpine${ALPINE_VERSION}
ARG UV_TAG=alpine${ALPINE_VERSION}


FROM ghcr.io/astral-sh/uv:${UV_TAG} AS uv_tool


FROM python:${PYTHON_TAG} AS dependencies
WORKDIR /app
COPY ./uv.lock ./pyproject.toml ./
COPY --from=uv_tool /usr/local/bin/uv /bin/
RUN uv export --format requirements-txt --no-hashes --no-dev -o ./requirements.txt


FROM python:${PYTHON_TAG}
WORKDIR /app

ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl
ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
    && unzip musl-locales-master.zip \
    && cd musl-locales-master \
    && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
    && cd .. && rm -r musl-locales-master
RUN apk update
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN pip install --upgrade pip
COPY --from=dependencies /app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python", "main.py"]
