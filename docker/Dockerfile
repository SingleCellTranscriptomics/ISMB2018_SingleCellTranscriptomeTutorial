FROM ubuntu:16.04
MAINTAINER bhaas@broadinstitute.org

RUN apt-get update && apt-get install -y gcc g++ perl python automake make cmake less vim \
                                       wget git curl libdb-dev \
                                       zlib1g-dev bzip2 libncurses5-dev \
                                       texlive-latex-base \
                                       default-jre \
                                       python-pip python-dev \
                                       gfortran \
                                       build-essential libghc-zlib-dev libncurses-dev libbz2-dev liblzma-dev libpcre3-dev libxml2-dev \
                                       libblas-dev gfortran git unzip ftp libzmq3-dev nano ftp fort77 libreadline-dev \
                                       libcurl4-openssl-dev libx11-dev libxt-dev \
                                       x11-common libcairo2-dev libpng12-dev libreadline6-dev libjpeg8-dev pkg-config \
                                       build-essential cmake gsl-bin libgsl0-dev libeigen3-dev libboost-all-dev libssl-dev libssl-dev libcairo2-dev libxt-dev libgtk2.0-dev libcairo2-dev xvfb xauth xfonts-base

RUN apt-get install -y apt-transport-https

## Install R-3.4.1
COPY installR.sh /usr/local/src

RUN /usr/local/src/installR.sh


RUN apt-get install -y sudo locales

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
  && locale-gen en_US.utf8 \
    && /usr/sbin/update-locale LANG=en_US.UTF-8

RUN apt-get install -y gdebi-core

COPY install_rstudio_server.sh /usr/local/src

RUN /usr/local/src/install_rstudio_server.sh

### User setup
RUN groupadd -g 2000 training && useradd -m -u 2000 -g 2000 training
RUN echo 'training:training' | chpasswd
RUN chsh -s /bin/bash training
ENV HOME=/home/training
RUN echo "alias ll='ls -la -G'" >> /home/training/.profile
RUN usermod -G training,www-data training


RUN apt-get install -y openssh-server libncurses5-dev apache2 supervisor


#########
### GateOne SSH interface
#########
RUN git clone https://github.com/liftoff/GateOne/ && \
    cd GateOne && python setup.py install && \
            pip install tornado==4.5.3 && \
                        python run_gateone.py --configure




EXPOSE 22 80 443 8787

RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("devtools", dep = TRUE)'


##
## Seurat 2.0
##



COPY caTools_1.17.1.mod.tar.gz /usr/local/src/
RUN Rscript -e 'install.packages("/usr/local/src/caTools_1.17.1.mod.tar.gz", repos=NULL, type="source");'

RUN Rscript -e 'library(devtools); install_github("satijalab/seurat", ref = "develop");'

COPY tclust_1.3-1.mod.tar.gz /usr/local/src
RUN Rscript -e 'install.packages("/usr/local/src/tclust_1.3-1.mod.tar.gz", repos=NULL, type="source")';

COPY kernlab_0.9-25.mod.tar.gz /usr/local/src
RUN Rscript -e 'install.packages("/usr/local/src/kernlab_0.9-25.mod.tar.gz", repos=NULL, type="source");'

RUN Rscript -e 'library(devtools); install_github("satijalab/seurat", ref = "develop");'


#Trying URL 'https://cran.rstudio.com/src/contrib/caTools_1.17.1.tar.gz'
# https://cran.rstudio.com/src/contrib/kernlab_0.9-25.tar.gz

#/usr/local/lib/R/site-library/

#caTools:  change .c to .cpp
#tclust: include <cstring> to get to compile
#kernlab: same


# needed for combat
RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("sva", dep = TRUE)'

# needed for seurat clustering (hopefully not in a future seurat release)
RUN chmod 777 /usr/local/lib/R/site-library


RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("fastcluster", dep = TRUE);'
RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("colorRamps", dep = TRUE);'

RUN usermod -a -G sudo training

RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("useful", dep = TRUE);'


##################
####  singleCellTK


RUN Rscript -e 'source("http://bioconductor.org/biocLite.R");library(BiocInstaller); biocLite("singleCellTK", dep = TRUE);'






## auto-run setup

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord","-c","/etc/supervisor/conf.d/supervisord.conf"]

