docker build \
-m 100G \
--memory-swap -1 \
-t jingyanwang1/llm_service_bloomz_7b1:1.0.1 .

docker run -it \
-p 0.0.0.0:6974:6974 \
jingyanwang1/llm_service_bloomz_7b1:1.0.1

157.230.50.43:6974


rm Dockerfile
vi Dockerfile
i
##########Dockerfile###########
FROM python:3.8.10

RUN apt-get install -y git 

RUN pip3 install Flask==2.2.2
RUN pip3 install flasgger==0.9.5
RUN pip3 install Werkzeug==2.2.2
RUN pip3 install flask-restx==1.0.3

RUN pip3 install torch==1.13.1
RUN pip3 install transformers==4.26.1

RUN pip3 install sentencepiece==0.1.97
RUN pip3 install protobuf==3.20.0

RUN python3 -c 'from transformers import AutoModelForCausalLM;model = AutoModelForCausalLM.from_pretrained("bigscience/bloomz-7b1")'

RUN python3 -c 'from transformers import AutoTokenizer;tokenizer = AutoTokenizer.from_pretrained("bigscience/bloomz-7b1")'

WORKDIR /

####

RUN echo "ds5g1s51g5sd"

RUN git clone https://github.com/jingyanwang/temp.git

WORKDIR /temp

CMD python3 app_path.py
##########Dockerfile###########