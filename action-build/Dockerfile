FROM debian:9.5-slim

RUN apt-get update && apt-get install -y \
    biber \
    latexmk \
    make \
    python3-pip \
    python3-setuptools \
    texlive \
    texlive-luatex \
    texlive-science \
 && rm -rf /var/lib/apt/lists/*

 RUN pip3 install \
     matplotlib \
     numpy \
     scipy \
     uncertainties

# https://stackoverflow.com/questions/43356982/docker-python-set-utf-8-locale
ENV PYTHONIOENCODING=utf-8
ENV LANG=de_DE.UTF-8
ENV LC_ALL=en_US.UTF-8

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
