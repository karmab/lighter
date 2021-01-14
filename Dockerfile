FROM centos:8
MAINTAINER Karim Boumedhel <karimboumedhel@gmail.com>

EXPOSE 9000

RUN yum -y install epel-release && yum -y install python-pip && yum clean all && rm -rf /var/cache/yum
RUN pip install flask
ADD main.py /tmp
# COPY templates /tmp/templates
# COPY static /tmp/static

ENTRYPOINT  ["python", "/tmp/main.py"]
