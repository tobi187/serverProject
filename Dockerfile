FROM python:3.10
COPY . /app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
RUN touch /var/celerylog.log
COPY . .