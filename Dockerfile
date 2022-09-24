FROM ubuntu:20.04
WORKDIR /app
RUN apt-get update && \
    apt-get install -y python3.7 python3-pip && \
    pip3 install flask redis datetime requests
CMD python3 -u app.py

# docker build -t server .
# docker run --name grafana -d -p 3000:3000 -rm ghcr.io/redisgrafana/redis-app:latest
# docker run --name redis -d -p 6379:6379 redis/redis-stack-server:latest

# docker run --name server -v /root/stock_crawler:/app server

# redis-cli zrange test 0 100

# https://www.infoq.com/articles/redis-time-series-grafana-real-time-analytics/