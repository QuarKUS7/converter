FROM python:3.7-alpine

RUN set -ex && mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod 644 app.py

CMD python app.py

