FROM python:3.11-alpine AS builder

WORKDIR /tmp

RUN pip install uv
COPY ./pyproject.toml ./uv.lock* ./
RUN uv export --format requirements-txt --no-hashes --no-dev -o ./requirements.txt


FROM python:3.11-alpine
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

COPY --from=builder /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD ["python", "main.py"]