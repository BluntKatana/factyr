# factyr
Practical assignment for the course: Web Data Processing Systems.

> ### Assignment Instructions
> You are called to implement a program that receives as input a question (or more in general a text to be completed), which we henceforth call A and returns as output four things:
>
> - The raw text returned by a large language model (that is, what you would get if you query the language model as is). We call it B
> - The answer extracted from B. This answer can be of two types: either yes/no or a Wikipedia entity
> - The correctness of the extracted answer (correct/incorrect)
> - Entities that have been extracted from A and B

Team (19): Floris Bos, Pooja Mangal, Kshitij Kavimandan and Maik Larooij

## Usage

### Installation with Docker (**RECOMMENDED**)

We recommend running the program with Docker. This way, you do not have to install any packages manually. Also, all the models used by the program are already installed in the Docker image.

To run the program, you need to have Docker installed. To install Docker, follow the instructions on the [Docker website](https://docs.docker.com/get-docker/). Pull the latest Docker image from Docker Hub by running: 
```
docker pull larooij/factyr:latest
```
Simply run the program by running the Docker image:
```
docker run -it larooij/factyr
```

To use an input file, you can copy the file to the Docker container by running:
```
docker cp <input_file> <container_id>:/factyr-app/example.txt
```
However, we recommend running the program with an input file by mounting the directory containing the input file to the Docker container. This way, you can easily access the output file. To do this, run:
```
docker run -it -v <local_input_file_directory>:/factyr-app/inputs larooij/factyr
```
The inputs are now available in the `inputs` directory in the Docker container.

Inside the Docker container, you can run the program by running `main.py`:
```
usage: main.py [-h] --input INPUT [--output OUTPUT] [--verbose]

factyr: an answer/entity extraction and fact checking pipeline.

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input file (txt)
  --output OUTPUT, -o OUTPUT
                        output file (txt)
  --verbose, -v         verbose mode
```

Example:
```
python3 main.py -v --input inputs/example.txt --output example.txt
```
This will run the program with the input file `inputs/example.txt` and output the results to `example.txt`, while printing the results to the terminal.

### Installation without Docker (**NOT RECOMMENDED**)

While the program can run without Docker, it is recommended to use Docker to run the program. Otherwise, you can install the required packages manually by running `pip install -r requirements.txt`. You also need the download Spacy's English model by running `python -m spacy download en_core_web_sm`, NLTK's stopwords by running `python -m nltk.downloader stopwords` and NLTK's punkt by running `python -m nltk.downloader punkt`.

You can now run the program by running `main.py`:
```
usage: main.py [-h] --input INPUT [--output OUTPUT] [--verbose]

factyr: an answer/entity extraction and fact checking pipeline.

options:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        input file (txt)
  --output OUTPUT, -o OUTPUT
                        output file (txt)
  --verbose, -v         verbose mode
```

## Project structure

The project is structured as follows:
```
/factyr-app
├── Dockerfile
├── README.md
├── main.py                                 # main file to run the program
├── requirements.txt
├── src
    ├── AnswerExtraction.py                 # answer extraction module
    ├── EntityExtraction.py                 # entity extraction module
    ├── FactChecking.py                     # fact checking module
    ├── LanguageModel.py                    # language model module   
    ├── Pipeline.py                         # pipeline module (combines all modules)
    ├── WikiAPI.py                          # Wiki API module -> gateway to Wikidata/Wikipedia
    ├── utils                               # utility functions        
    │   ├── openie.py                       # imported OpenIE module            
├── models                                  # models used by the program -> not on GitHub, but included in Docker image
    ├── entity_model                        # model used for entity answer extraction
    ├── yes_no_model                        # model used for yes/no answer extraction
    ├── stanford-corenlp-4.5.3              # Stanford CoreNLP library
    ├── qc_model_cv.pkl                     # CountVectorizer used for question type classification     
    ├── qc_model_lr.pkl                     # LogisticRegression used for question type classification
    ├── llama-2-7b-chat.Q5_K_M.gguf         # LLAMA language model
    ├── zephyr-7b-beta.Q5_K_M.gguf          # Zephyr language model
├── data                                    # data used for the program / evaluation           
├── test                                    # test/example files
```