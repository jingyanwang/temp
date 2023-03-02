#####################
FROM openjdk:8

RUN apt-get update
RUN apt-get install -y build-essential 
RUN apt-get install -y wget
RUN apt-get install -y git 
RUN apt-get install -y curl
RUN apt-get install -y vim
RUN apt-get install -y tar
RUN apt-get install -y bzip2
RUN apt-get install -y gcc
RUN apt-get install -y make
RUN apt-get install -y libssl-dev 
RUN apt-get install -y zlib1g-dev 
RUN apt-get install -y libbz2-dev 
RUN apt-get install -y libreadline-dev 
RUN apt-get install -y libsqlite3-dev 
RUN apt-get install -y libncursesw5-dev 
RUN apt-get install -y xz-utils 
RUN apt-get install -y tk-dev 
RUN apt-get install -y file
RUN apt-get install -y libncurses5-dev
RUN apt-get install -y libxml2-dev
RUN apt-get install -y libffi-dev
RUN apt-get install -y liblzma-dev 

RUN apt-get install -y python3-dev
RUN apt-get install -y python3-pip

RUN pip3 install torch==1.13.1
RUN pip3 install torchvision==0.14.1
RUN pip3 install torchaudio==0.13.1
RUN pip3 install transformers==4.26.1
RUN pip3 install langchain==0.0.88

RUN pip3 install Flask==2.2.2
RUN pip3 install flasgger==0.9.5
RUN pip3 install Werkzeug==2.2.2
RUN pip3 install flask-restx==1.0.3

RUN python3 -c 'from transformers import pipeline, set_seed;generator = pipeline("text-generation", model="gpt2")'

RUN python3 -c 'from transformers import AutoModelForSeq2SeqLM, AutoTokenizer;model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base");tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")'

#RUN python3 -c 'from transformers import pipeline, set_seed;generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")'

WORKDIR /

####

RUN echo "s6dg1ds5g5d1"

COPY *.py /
COPY *.conf /

CMD python3 app_path.py

#####################