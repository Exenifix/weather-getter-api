FROM python:3.10-bullseye

COPY . /app
WORKDIR /app

EXPOSE 5001

RUN pip install -U pip
RUN pip install -r requirements.txt
CMD ["python", "api.py"]
