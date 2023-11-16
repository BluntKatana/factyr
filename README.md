# fact-checker
 Practical assignment for the course: Web Data Processing Systems.

> ### Assignment Instructions
> You are called to implement a program that receives as input a question (or more in general a text to be completed), which we henceforth call A and returns as output four things:
>
> - The raw text returned by a large language model (that is, what you would get if you query the language model as is). We call it B
> - The answer extracted from B. This answer can be of two types: either yes/no or a Wikipedia entity
> - The correctness of the extracted answer (correct/incorrect)
> - Entities that have been extracted from A and B

Team (19): Floris Bos, Pooja Mangal, Kshitij Kavimandan and Maik Larooij

## Pipeline / what do we need to do?
- [ ] Large Language Model (LLM)
     - [ ] 1. Choose language model (like Llama 2)
     - [ ] 2. Find a way to load language model in Python
     - [ ] 3. Wrapping up: write function/class to feed a question (input) and get the answer text as output

- [ ] Named Entity Recognition and Disambiguation (linking)
     - [ ] 1. Choose NER model (like SpaCy, NLTK, BERT)
     - [ ] 2. Write function/class to feed raw text (LLM output) and get as output the extracted entities with their types
     - [ ] 3. Find a way/write a function to generate Wikipedia candidates for a single entity
     - [ ] 4. Find a way/write a function to, based on an entity (+ context?), rank the candidates and pick the highest scoring one
     - [ ] 5. Wrapping up: write a class/function to feed the LLM answer (raw text) and get a list of entities with their predicted Wikipedia page as output

- [ ] Answer extraction
     - [ ] 1. Based on the query and answer(?), figure out if the answer should be 'yes/no' or an entity
     - [ ] 2. Find a way/write a function to extract the answer ('yes/no', or entity) from the LLM output
     - [ ] 3. Wrapping up: write a class/function to feed the LLM query and answer and output a single answer ('yes/no', or entity)

- [ ] Fact checking
     - [ ] 1. Choose a knowledge base to use (like Wikidata) 
     - [ ] 2. Based on the query and extracted answer, find a way to check if the answer of the LLM is true or false, with the help of the knowledge base
     - [ ] 3. Wrapping up: write a class/function to feed the LLM query, extracted answer (from last step) and knowledge base and get as output true or false, indicating the correctness of the LLM's answer
