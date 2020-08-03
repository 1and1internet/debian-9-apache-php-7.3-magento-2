FROM alpine as magento_source
RUN apk add git \
	&& git -c http.sslVerify=false clone https://git.dev.glo.gb/cloudhostingpublic/magento_source

FROM 1and1internet/debian-9-apache-php-7.3:latest
MAINTAINER developmentteamserenity@fasthosts.co.uk
ARG DEBIAN_FRONTEND=noninteractive
COPY files /
COPY --from=magento_source /magento_source/magento2.tar.gz /tmp/magento2.tar.gz

RUN chmod +x /hooks/supervisord-pre.d/10_magento \
    && chmod 777 /var/www/html \
    && rm -f /etc/supervisor/conf.d/php-fpm.conf /etc/supervisor/conf.d/nginx.conf \
    && apt-get update && apt-get install -y php7.3-redis curl wget telnet

EXPOSE 8080
ENV DOCUMENT_ROOT=html/magento2 \
    MAGENTO_ADMIN_USER=admin \
    MAGENTO_ADMIN_PASSWORD=P@55w0rd \
    MAGENTO_BASE_URL=http://localhost:8080 \
    BACKEND_FRONTNAME=admin
