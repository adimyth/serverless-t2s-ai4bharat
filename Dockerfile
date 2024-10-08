FROM runpod/base:0.4.0-cuda11.8.0

# Set working directory
RUN mkdir -p /usr/ai-inference/
WORKDIR /usr/ai-inference/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LOG_LEVEL INFO

# Install system dependencies
RUN apt-get update \
    && apt-get -y install git g++ gcc postgresql libpq-dev python3-dev wget unzip vim curl \
    && apt-get -y install poppler-utils ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install nltk
RUN python3.10 -m pip install nltk
RUN python3.10 -c "import nltk; nltk.download('punkt')"

# Download Indic-TTS models 
RUN mkdir -p /usr/ai-inference/models/v1
# Hindi
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/hi.zip && unzip hi.zip -d /usr/ai-inference/models/v1 && rm hi.zip
# Kannada
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/kn.zip && unzip kn.zip -d /usr/ai-inference/models/v1 && rm kn.zip
# Tamil
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/ta.zip && unzip ta.zip -d /usr/ai-inference/models/v1 && rm ta.zip
# Telugu
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/te.zip && unzip te.zip -d /usr/ai-inference/models/v1 && rm te.zip
# Marathi
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/mr.zip && unzip mr.zip -d /usr/ai-inference/models/v1 && rm mr.zip
# Malayalam
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/ml.zip && unzip ml.zip -d /usr/ai-inference/models/v1 && rm ml.zip
# Bengali
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/bn.zip && unzip bn.zip -d /usr/ai-inference/models/v1 && rm bn.zip
# Gujarati
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/gu.zip && unzip gu.zip -d /usr/ai-inference/models/v1 && rm gu.zip
# Punjabi
RUN wget https://github.com/AI4Bharat/Indic-TTS/releases/download/v1-checkpoints-release/pa.zip && unzip pa.zip -d /usr/ai-inference/models/v1 && rm pa.zip

# Install TTS dependencies
RUN git clone https://github.com/adimyth/TTS 
RUN cd TTS && python3.10 -m pip install -e .

# Install necessary packages
COPY builder/requirements.txt /requirements.txt
RUN python3.10 -m pip install pip==23.2.1 && \
    python3.10 -m pip install --upgrade -r /requirements.txt --no-cache-dir --ignore-installed && \
    rm /requirements.txt

# Add src files
ADD src .

CMD python3.10 -u /usr/ai-inference/handler.py