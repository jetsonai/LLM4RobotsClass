# Convert GGUF

### Make models folder 

cd 

mkdir models

### git clone llama.cpp Server or Colab at any place

git clone https://github.com/ggerganov/llama.cpp

-----------------

## 1. Convert Bllossom Model

### prepare model (for example, you can download llama3.2 Korean Bllossom Model.)

./python3 model_download.sh

## you can convert hf to gguf 

./model_converter.sh

-----------------

## 2. Convert My Model

### prepare model (for example, you can download rssaem/Llama3_2_ModelBTS Model.)

./python3 my_model_download.sh

## you can convert hf to gguf 

./my_model_converter.sh

