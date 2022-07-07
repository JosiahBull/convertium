FROM python:3

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#TODO: HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD "curl --fail http://localhost:5000/health || exit 1"

CMD [ "python", "./src/convertium.py" ]