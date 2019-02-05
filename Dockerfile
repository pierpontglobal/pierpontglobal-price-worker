FROM python:2.7-stretch

RUN apt-get update && apt-get install -yq \
    firefox-esr \
    chromium \
    git-core \
    xvfb \
    xsel=1.2.0-2+b1 \
    unzip=6.0-21 \
    python-pytest=3.0.6-1 \
    libgconf2-4=3.2.6-4+b1 \
    libncurses5=6.0+20161126-1+deb9u2 \
    libxml2-dev=2.9.4+dfsg1-2.2+deb9u2 \
    libxslt-dev \
    libz-dev \
    xclip=0.12+svn84-4+b1

WORKDIR /

COPY . /
COPY chromedriver /
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]