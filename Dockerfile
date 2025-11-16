FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    libwebp-dev \
    tcl-dev tk-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


RUN pip install --upgrade pip


COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]