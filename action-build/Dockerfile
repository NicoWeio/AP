FROM debian:9.5-slim

RUN apt-get update && apt-get install -y \
    biber \
    dvipng \
    latexmk \
    make \
    python3-pip \
    python3-setuptools \
    texlive \
    texlive-latex-extra \
    texlive-luatex \
    texlive-science \
 && rm -rf /var/lib/apt/lists/*

 RUN pip3 install \
     matplotlib \
     numpy \
     scipy \
     uncertainties

# !?
#RUN apt-get install -y locales \
# && locale-gen de_DE de_DE.UTF-8 \
# && update-locale LANG=de_DE \
# && dpkg-reconfigure locales

# https://stackoverflow.com/questions/43356982/docker-python-set-utf-8-locale
#ENV PYTHONIOENCODING=utf-8
#ENV LANG=de_DE.UTF-8
#ENV LC_ALL=de_DE.UTF-8

ENV LANG=C.UTF-8

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
