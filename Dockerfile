FROM python:3

RUN apt-get update && apt-get install -y lp-solve
RUN pip install pandas

COPY generate_lp.py /usr/local/bin/generate_lp
COPY entrypoint.sh /usr/local/bin/entrypoint
RUN mkdir /data

ENTRYPOINT ["entrypoint"]
