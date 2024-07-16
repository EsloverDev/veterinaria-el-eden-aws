FROM python:3.9.16

WORKDIR /project

COPY . .

RUN pip install -r requirements.txt

CMD ["sudo", "python3", "server.py"]