# TEST Env

llama.cpp server : Nvidia Jetson Xavier

whisper.cpp server : Nvidia Jetson Nano 장착 로봇

Wav2LLM : Nvidia Jetson Nano 장착 로봇

---------------------------------------

# Start llama.cpp server

nvidia@ubuntu:~/llama.cpp/build/bin$ ./llama-server -m /mnt/mnt__data/xavier/models/llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M -ngl 63 -c 2048 --host `hostname -I | awk '{ print $1}'` ^C

-----------------
# Make ramdisk 

cd Talkative

mkdir ramdisk

sudo mount -t ramfs -o size=100M ramfs ./ramdisk

-----------------
# Start  whisper.cpp server   #####

cd whisper.cpp/build/bin

./server -m ./server --language ko -m ../../models/ggml-base.bin

-----------------
# Start Wav2LLM Test on Robot

python3 Wav2LLM.py
