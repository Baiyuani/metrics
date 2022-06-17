FROM python:3.9

WORKDIR /web_metrics

ADD web_metrics/* .

RUN pip install -r requirements.txt
RUN mkdir logs || true
RUN ln -s /dev/stdout ./logs/web_metrics.log

EXPOSE 5000

CMD ["python", "/web_metrics/main.py", ">", "/web_metrics/logs/web_metrics.log"]