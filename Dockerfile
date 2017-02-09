FROM ubuntu:16.04
MAINTAINER Nodar Nutsubidze <nodar.nutsubidze@gmail.com>
ENV HOSTNAME localhost

# Install packages
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qy \
  git \
  python-dev \
  python-pip

# Download git repo
RUN git clone https://github.com/Darless/python_project_template.git /opt/python_project_template

# Move to the directory so we install the libraries in correct folder
RUN cd /opt/python_project_template && make docker

WORKDIR /opt/python_project_template
CMD ["make", "test"]
