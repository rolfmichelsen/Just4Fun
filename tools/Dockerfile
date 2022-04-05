# docker build --tag httpdtest .
#
FROM debian:bullseye
EXPOSE 5000
RUN apt-get update && apt-get install -y python3
WORKDIR /work
COPY httpdtest.py .
CMD python3 ./httpdtest.py 5000
