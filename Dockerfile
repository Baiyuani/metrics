FROM python:3.9

WORKDIR /metrics

ADD . .

RUN pip install -r requirements.txt
RUN mkdir logs || true
RUN ln -s /dev/stdout ./logs/metrics.log

EXPOSE 5000

CMD ["python", "./src/main.py", ">", "./logs/metrics.log"]