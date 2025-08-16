# Stage 1: Use a Node.js image for the first stage
FROM ubuntu:latest as ubuntu-stage

# Installing common packages
RUN yes | unminimize
RUN apt-get update -y && apt-get install -y software-properties-common language-pack-en-base debconf-utils curl 
RUN apt-get update -y && apt-get install net-tools wget nano vim less -y
RUN apt-get update -y && apt-get install -y iproute2 python3 python3-pip -y

# Install anything you want here:
RUN apt-get install -y man-db

# Install Paramiko package
RUN pip3 install --break-system-packages paramiko

# Install OpenSSH client
RUN apt-get update -y && apt-get install -y openssh-client

# Setup Environment variables
ENV INSTRUCTOR_SCRIPTS="/home/.evaluationScripts"
ENV LAB_DIRECTORY="/home/labDirectory"
ENV PATH="/home/.evaluationScripts:${PATH}"
ENV TERM=xterm-256color

# Setup Directory Structure
RUN mkdir /home/labDirectory
RUN mkdir /home/.evaluationScripts

# Global Settings
RUN echo "cd /home/labDirectory" > /root/.bashrc
RUN echo "alias ls='ls --color=always'" >> /root/.bashrc
RUN echo "rm -f \`find /home -type f -name \"._*\"\`" >> /root/.bashrc

CMD [ "/bin/bash", "-c", "while :; do sleep 10; done" ]