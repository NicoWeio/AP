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

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
