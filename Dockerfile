FROM python:3.10

RUN apt-get update \
    && pip install --upgrade pip \
    && apt-get -y install default-jre

WORKDIR /factyr-app

# Python code
COPY src src
COPY main.py .

# Models and data
COPY models models
COPY data data

# Add simple example
COPY test/example_input.txt test/example_input.txt

COPY requirements.txt .
COPY README.md .

# Dependencies
RUN pip install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords

CMD ["/bin/bash"]