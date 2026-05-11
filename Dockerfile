FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk upgrade --no-cache && pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python","app.py"]