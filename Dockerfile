FROM python:alpine AS python_gwa_common

WORKDIR /srv

# UPDATE APK CACHE AND INSTALL PACKAGES
RUN apk add --update --no-cache \
    make \
    build-base \
    jq \
    curl \
    tzdata \
    git \
    libffi-dev \
    postgresql-dev \
    gcc g++ \
    ca-certificates && \
    update-ca-certificates

# ADD APP
ADD . .

# INSTALL FROM REQUIREMENTS FILE
RUN pip install -U pip && pip install -r requirements.txt

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && \
    echo "America/Sao_Paulo" > /etc/timezone

EXPOSE 8000

# ENTRYPOINT
ENTRYPOINT ["sh", "app.sh", "gwa_common:app"]