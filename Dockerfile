FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYHTONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install gcc make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

WORKDIR /src/app

COPY ./requirements.txt /src/app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python BookRec.py

ENTRYPOINT ["python"]

CMD ["app.py"]