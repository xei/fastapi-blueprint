FROM python:slim-buster

LABEL Description="This image can be used to setup a production-ready FastAPI service."
LABEL maintainer="Hamidreza Hosseinkhani <hamidreza@hosseinkhani.me>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade fastapi uvicorn[standard]
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

WORKDIR /app
COPY ./app /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]