
nvidia@ubuntu:~/llama.cpp/build/bin$ ./llama-server -m /mnt/mnt__data/xavier/models/llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M -ngl 63 -c 2048 --host `hostname -I | awk '{ print $1}'` ^C

![image](https://github.com/user-attachments/assets/34a15110-7197-4ae4-b9b2-43535757ac3b)

-----------------
# Make ramdisk 

mkdir ramdisk

sudo mount -t ramfs -o size=100M ramfs ./ramdisk

-----------------
# Start  whisper.cpp    #####

cd whisper.cpp/build/bin

./server -m ./server --language ko -m ../../models/ggml-base.bin

-----------------

cd Talkative

python3 
