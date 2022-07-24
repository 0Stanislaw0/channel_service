FROM python:3.9-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN ["chmod", "+x", "comands.sh"]

ENTRYPOINT ["/comands.sh"]






