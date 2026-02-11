# mini-RAG
This is a minimal implementation of the RAG model for question answering.

# Requirenments
Python 3.11 or later

### Install python using miniconda

1) Download miniconda from [here] (https://www.anaconda.com/docs/getting-started/miniconda/install)

2) Create a new environment using the follownig command:

```bash
$ conda create -n mini-rag python=3.11
```
3) Activate the environment using the following command:

```bash
$ conda activate mini-rag 
```

### (Optional) Setup your command line for better readability

```bash
$ export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install required packages

```bash
$ pip install -r requirements.txt 
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the `.env ` file. Like `OPENAI_API_KEY` value

## Run astAPI server 

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection
 Download the POSTMAN collection from [assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)