# Open-source LLMs


## Introduction

On the previous module we learnt about the general RAG architecture, where we need 2 components whicha are knowledge-base which could be a DB, search engine, or even online search, and LLM that answer queries based on information pieces supplied from the knowledget-based.

In this module, we will run different open-source models from [hugging face](https://huggingface.co/) and also run some of them locally on CPU using [Ollama](https://ollama.com/).

Running LLMs is a heavy process, you need to utilize alot of resources like a powerful GPU to produce the results as fast and efficient as possible. 
So if we can't get a GPU to run the LLMs locally we have to pay for a GPU provide like GCP, AWS, or Saturn. (In my case, I was provided with a paid 15h to run a relatively powerful GPU on Saturn).

Remember that on the previous module we used an API provided from GROQ or OpenAI which is an interface for a running LLM service that waits only for our prompt. Even though GROQ provides this service for free OpenAI doesn't. Those LLM providers do the part of running powerful GPUs and you need to pay for this service instead of buying a GPU.

## Prerequisites

Please, make sure you have the following tools installed on your system: 
1. Python3: You can install it from the following [official website](https://www.python.org/downloads/).
2. Docker:  which is a containerization tool, we will use it to run Ollama server without any overhead. you can download it through [Docker official website](https://www.docker.com/products/docker-desktop/).

## Scenario

The RAG System consists of:
1. Knowledge-base: we will use `minsearch` which is a home-made search engine and `elastic search`
2. Retriver: The piece of code that getting documents from the DB.
3. Prompt Builder: building the prompt than contains our query besides the docs retrived from the database.
4. Large Language Model

As we are going to make use of different LLMs, I will make the first three parts to be fixed and make use of the prompt and send it to the different LLMs.

### Base Code
#### Knowledge base
On the previous modele, we'd already used minsearch and elasticsearch so lets setup them quieckly (you may only need to use one of them).

```python
# Downloading docs
import os
import requests

# Downloading docs
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)
```

##### Minsearch
First [download](https://raw.githubusercontent.com/alexeygrigorev/minsearch/main/minsearch.py) this engine's file to use it.
```python
import minsearch

# Indexing the documents on minsearch
index = minsearch.Index(
    text_fields=["question", "text", "section"],
    keyword_fields=["course"]
)

index.fit(documents)
```

##### Elasticsearch
```python
from elasticsearch import Elasticsearch

# connectingg to elasticsearch server
es_client = Elasticsearch('http://localhost:9200')

# configure and create index
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} # primary key in RDBMS taste
        }
    }
}
index_name = "course-questions"
es_client.indices.create(index=index_name, body=index_settings)

# Indexing documents inside elasticsearch
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)
```

#### Retriver
##### minsearch based retriever
```python
def search(query):
    boost = {'question': 3.0, 'section': 0.5}

    results = index.search(
        query=query,
        filter_dict={'course': 'data-engineering-zoomcamp'},
        boost_dict=boost,
        num_results=5
    )

    return results
```

##### elasticsearch based retriever
```python
def search(query, size=5, search_words=[]):
    def filter_builder():
        return list(map(lambda word: {"term": {**word}}, search_words))
        
    search_query = {
        "size": size,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        # don't forget to customize the weight of each field "word^{weight}"
                        "fields": ["question", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": filter_builder()
            }
        }
    }

    return es_client.search(index=index_name, body=search_query)
```

#### Prompt Builder
```python
def build_prompt(query, search_results):
    # feel free to make prompt engineering to customize the prompt for the suitable LLM
    prompt_template = """
You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.Use only the facts from the CONTEXT when answering the QUESTION.

QUESTION: {question}

CONTEXT:
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt
```

Now we have built the first 3 coomponents of out rag system, the 4th is set the LLM component.

### Setting up LLM

> [!TIP] Common pattern
> For open-source models, we need to download the the tokenizer used to tranform the query string to the language that the model understand. Also the tokenizer is used to convert back the output of the LLM to human readable text.
>
> Each model uses a certain tokenizer, that produces its own language.
>
> You may need also to customize some model params to get the best results.

#### google/flan-t5-xl

```python
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Loading the model with its tokenizer
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl", device_map="auto")

def llm(prompt, generate_params=None):
    if generate_params is None:
        generate_params = {}

    # encoding the prompt
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")

    # sending the encoded prompt
    outputs = model.generate(
        input_ids,
        max_length=generate_params.get("max_length", 100),
        num_beams=generate_params.get("num_beams", 5),
        do_sample=generate_params.get("do_sample", False),
        temperature=generate_params.get("temperature", 1.0),
        top_k=generate_params.get("top_k", 50),
        top_p=generate_params.get("top_p", 0.95),
    )

    # decoding the result
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result
```

#### microsoft/phi3-mini

This model needs besides the tokenizer to build a pipeline that takes the reponsibility of encoding and decoding text.

```python
import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# making the output reproducable
torch.random.manual_seed(0) 

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-128k-instruct")
model = AutoModelForCausalLM.from_pretrained( 
    "microsoft/Phi-3-mini-128k-instruct",  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
) 

def llm(prompt):
    def pipe_builder(model, tokenizer):
        return pipeline("text-generation", model=model, tokenizer=tokenizer)
    
    messages = [
        {"role": "user", "content": prompt},
    ]

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False,
    }
    
    pipe = pipe_builder(model, tokenizer)

    output = pipe(messages, **generation_args)
    return output[0]['generated_text'].strip()
```
> [!IMPORTANT] Lego Bricks
> As you can notice building RAG system, is like [lego brick](https://www.lego.com/en-us/pick-and-build/pick-a-brick) in a block you take one and set the other that match your needs. The google/flan-t5-xl and microsoft/phi3-mini are lego bricks you put on a larger construct.

#### Running LLM on CPU using OLLAMA
> I wrote another document to summerize what I've learnt about Ollama platform.

## Conclusion

Building RAG systems is like SW design patterns you need to analyze your problem and define your requirements and ask some question:
1. Which knwolegdge-base is suitable for my app?
2. Do I have enough powerful hardware to run a LLM locally?
3. Do my app need a locally running LLM or should I buy for a service provider?