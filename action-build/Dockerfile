FROM debian:9.5-slim

RUN apt-get update && apt-get install -y \
    biber \
    dvipng \
    latexmk \
    make \
    python3-pip \
    python3-setuptools \
#    texlive \
#    texlive-fonts-extra \
#    texlive-latex-extra \
#    texlive-lang-german \
#    texlive-luatex \
#    texlive-science \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install \
     matplotlib \
     numpy \
     scipy \
     uncertainties

#RUN curl -sSLo miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#RUN bash ./miniconda.sh -p $HOME/conda -b
#RUN source $HOME/conda/etc/profile.d/conda.sh
#RUN conda activate
#RUN conda install --yes matplotlib numpy pandas requests scipy sympy
RUN pip3 install uncertainties jupyter_contrib_nbextensions https://github.com/maxnoe/texlive-batch-installation/archive/v0.2.1.tar.gz

# install texlive minimal with what we need
RUN | python3 -m install_texlive -p $HOME/texlive -t 2020 --collections='-acfghuDFG' \
	-i 'koma-script,babel,babel-french,csquotes,placeins,enumitem,biber,biblatex,siunitx,beamer,xpatch,blindtext,standalone,circuitikz,tikz-feynman,xstring,fontawesome5,mleftright,mhchem,tabulary,tabu,varwidth,lstaddons,tcolorbox,mwe,fira,firamath,firamath-otf,xits,threeparttable,environ,trimspaces,pgfopts,ncctools'
RUN export PATH=$HOME/texlive/2020/bin/x86_64-linux:$PATH
RUN tlmgr install --with-doc tex-overview

ENV LANG=C.UTF-8

ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
