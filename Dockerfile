FROM python:3.10

RUN apt-get update \
    && pip install --upgrade pip

RUN mkdir /src
COPY *.py /src
COPY models /src/models
COPY data /src/data
WORKDIR /src
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords

CMD ["/bin/bash"]