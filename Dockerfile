FROM python:3.10

RUN apt-get update \
    && pip install --upgrade pip

RUN mkdir /src

# Python code
COPY src /src
COPY main.py .

# Models and data
COPY models /src/models
COPY data /src/data

WORKDIR .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords

CMD ["/bin/bash"]