FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install mysql-connector-python
RUN pip install matplotlib

CMD ["python", "main.py"]
