FROM python:3

RUN apt-get update && apt-get install -y lp-solve
RUN pip install pandas

COPY src/ src/
WORKDIR src/
RUN mkdir /data

ENTRYPOINT ["./entrypoint.sh"]
