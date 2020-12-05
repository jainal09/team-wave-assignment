FROM python:3.8
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir /team-wave-assignment
WORKDIR /team-wave-assignment
COPY . /team-wave-assignment
