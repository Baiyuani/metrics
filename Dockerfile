FROM python:3.9

WORKDIR ./metrics

ADD . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ln -s /dev/stdout ./metrics.log

EXPOSE 5000

CMD ["python", "./src/main.py", ">", "./metrics.log"]