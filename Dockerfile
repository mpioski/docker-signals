FROM python:3.7

MAINTAINER Matheus Pioski

WORKDIR /source

ADD . /source

RUN ls -la /source
