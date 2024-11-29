# Convert GGUF

## prepare model (for example, you can download llama3.2 Korean Bllossom Model.)

mkdir models

cd models

python3 model_download.py

(you can change any model if you want.) 

## git clone llama.cpp Server or Colab at any place

git clone https://github.com/ggerganov/llama.cpp

## you can convert hf to gguf without build

python3 convert_hf_to_gguf.py ../models/Bllossom/ --outtype f16




