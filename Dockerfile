FROM --platform=linux/amd64 ubuntu:20.04

ENV PATH="/ruta/miniconda3/bin:${PATH}"
ARG PATH="/ruta/miniconda3/bin:${PATH}"

RUN apt update \
    && apt install -y python3-dev wget \
    && apt install git -y

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh \
    && mkdir ruta \
    && mkdir ruta/.conda \
    && sh Miniconda3-py39_4.12.0-Linux-x86_64.sh -b -p /ruta/miniconda3 \
    && rm -f Miniconda3-py39_4.12.0-Linux-x86_64.sh

RUN conda create -y -n num-txt python=3.11

COPY . num_to_text/

RUN apt-get update
RUN apt-get install gcc g++ -y


RUN /bin/bash -c "cd num_to_text \
    && source activate num-txt \
    && pip install -r requirements.txt"

CMD ["/bin/bash","-c","cd num_to_text/ && source activate num-txt && python main.py"]