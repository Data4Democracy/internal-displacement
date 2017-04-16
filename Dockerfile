FROM ubuntu:latest

RUN mkdir /internal-displacement
VOLUME /internal-displacement
WORKDIR /internal-displacement

RUN apt-get update
RUN apt-get -y install python3 python3-pip python3-dev libffi-dev
RUN pip3 install cld2-cffi
RUN apt-get -y install libxslt1-dev antiword unrtf poppler-utils pstotext \
        tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev \
        postgresql libpq-dev git

RUN pip3 install --upgrade pip && \
    pip3 install NumPy SciPy spacy && \
    pip3 install git+git://github.com/aerkalov/ebooklib.git && \
    pip3 install textract

COPY . /internal-displacement

RUN pip3 install -r /internal-displacement/requirements.txt

CMD jupyter notebook --no-browser --ip=0.0.0.0
