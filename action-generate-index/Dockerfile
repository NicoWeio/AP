FROM debian:9.5-slim

ENV LANG=C.UTF-8

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
