FROM python:3.8.5-slim-buster

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install wheel && pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "main.py"]