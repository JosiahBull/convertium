FROM python:3

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg postgresql

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK --start-period=5s CMD ["python", "./src/healthcheck.py"]

CMD [ "./scripts/wait-for-postgres.sh", "python", "./src/convertium.py" ]