FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

# Set correct environment variables.
ENV HOME /home/aleksandr

# RUN apt-get update && apt-get install -y software-properties-common python-software-properties && apt-get update

# Install Python Setuptools
RUN apt-get install -y cron

# RUN apt-get purge -y python-software-properties software-properties-common && apt-get clean -y && apt-get autoclean -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD crontab /etc/cron.d/
ADD . /

RUN chmod 644 /etc/cron.d/crontab

RUN touch /var/log/cron.log

RUN pip install requests
RUN pip install bs4

# RUN chmod a+x main.py run-cron.py

# Set the time zone to the local time zone
# RUN echo "Europe/Helsinki" > /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata

CMD cron && tail -f /var/log/cron.log
