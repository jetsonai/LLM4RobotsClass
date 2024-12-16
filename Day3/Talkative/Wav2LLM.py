import pyaudio
import wave
import os
from queue import Queue
from _thread import *
import logging
import requests
import json
from gtts import gTTS
import playsound
import argparse

VERBOSE = True

STT_URL = 'http://127.0.0.1:8080/inference'
#LLM_URL = 'http://192.168.100.55:8080/completion'
LLM_URL = 'http://192.168.100.55:8080/v1/chat/completions'
LLM_N_PREDICT = 70 

########################################
# #####      Make ramdisk     #####
#
# mkdir ramdisk
# sudo mount -t ramfs -o size=100M ramfs ./ramdisk
#
########################################
# #####      Start  whisper.cpp    #####
#
# cd whisper.cpp/build/bin
#./server -m ./server --language ko -m ../../models/ggml-base.bin
#
########################################
# #####      Start  llama.cpp    #####
#
# cd llama.cpp/build/bin
#./llama-server -m /mnt/mnt__data/xavier/models/llama-3.2-Korean-Bllossom-3B-gguf-Q4_K_M -ngl 63 -c 2048 --host `hostname -I | awk '{ print $1}'`
#
########################################

wav_output_filename = './ramdisk/voice.wav'

source_file = wav_output_filename
output_file = "./ramdisk/voice1.wav"
mp3_filename = "./ramdisk/voice1.mp3"

print(wav_output_filename)

def logger(txt:str = ""):
    if VERBOSE:
        logging.info(txt)
    else:
        return

def rmExistFile(filename):
    if os.path.isfile(filename):
        rmcommand = "rm " + filename
        os.system(rmcommand)  
         
def RecordConvert(q_wave_path):
    logger("RecordConvert: start")
    form_1 = pyaudio.paInt16
    chans=1
    samp_rate = 44100
    chunk = 4096
    record_secs = 5     #record time
    dev_index = 11
    
    rmExistFile(output_file)    
    
    #global source_file, output_file
    audio = pyaudio.PyAudio()
    #setup audio input stream
    stream=audio.open(format = form_1,rate=samp_rate,channels=chans, input_device_index = dev_index, input=True, frames_per_buffer=chunk)
    logger("recording")
    frames=[]
     
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data=stream.read(chunk,exception_on_overflow = False)
        frames.append(data)
     
    logger("finished recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    #creates wave file with audio read in
    #Code is from the wave file audio tutorial as referenced below
    wavefile=wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()

    #cmd_str = f"ffmpeg -i {source_file} -ac 1 -ar 44000 {output_file}"
    cmd_str = f"ffmpeg -i {source_file} -ar 16000 -ac 1 -c:a pcm_s16le {output_file}"
    print(cmd_str)
    os.system(cmd_str)
    #q_wave_path.put(output_file)
    #logger("send output_file")
    logger("RecordConvert: end")

def RecognizeWisper(q_wave_path, q_txt_stt):
    logger("RecognizeWisper: start")
    def ready_query(wave_path:str):
        assert os.path.isfile(wave_path)
        query = {
            'file': open(wave_path, 'rb'),
            'response-format': (None, 'json'),
        }
        return query
    RecText = "Fail Recog"
    try:
        #wave_path = q_wave_path.get()
        wave_path = output_file
        query = ready_query(wave_path=wave_path)
        response = requests.post(STT_URL, files=query)
        recRecText = json.loads(response.text)["text"]
        lines = recRecText.split('\n')
        print("[" + recRecText + "]")
        RecText = lines[0]
        print("[" + RecText + "]")
        #q_txt_stt.put(result1)
        #logger("send whisper result:"+ text)
        pass
    except Exception as e:
        logger("RecognizeWisper: end by except {}".format(e))
    logger("RecognizeWisper: end")
    return RecText

def callLlama(stt_text):
    logger("LLM thread: start")
    llm_header = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer no-key'
    }
    def ready_query(stt_text:str):
        stt_text = "안 녕? "
        query = {"model": "gpt-3.5-turbo","messages": [ { "role": "user", "content": stt_text} ] }
      
        return query
    outputText = "fail to LLM"
    try:
        #while True:
        #logger("get stt text")
        #stt_text = q_txt_stt.get()
        query = ready_query(stt_text=stt_text)
        #logger("send text to xavier: {}".format(stt_text))
        response = requests.post(LLM_URL, headers=llm_header, json=query)
        outputText = json.loads(response.text)['choices'][0]['message']['content']

        logger("get text from xavier: {}".format(outputText))
        #q_txt_llm.put(text)
        logger("send xavier result")
        #pass
    except Exception as e:
        logger("LLM thread: end by except {}".format(e))
    logger("LLM thread: end")
    return outputText

def callTTS(outputText):
    logger("TTS thread: start")
    def speak(text):
        #logger("speak text: {}".format(text))
        tts = gTTS(text=text, lang='ko')
        tts.save(mp3_filename)
        playsound.playsound(mp3_filename)
    try:
        #while True:
        #tts_text = q_txt_llm.get()
        rmExistFile(mp3_filename)  
        speak(outputText)
    except Exception as e:
        logger("TTS thread: end by except {}".format(e))
    logger("TTS thread: end")
             

def main(args):
    logger("start main")
    VERBOSE = args.verbose
    STT_URL = args.stt_url
    LLM_URL = args.llm_url
    LLM_N_PREDICT = args.llm_n_predict
    q_wave_path = Queue(maxsize=1)
    q_txt_stt = Queue(maxsize=1)
    #q_txt_llm = Queue(maxsize=1)
    thread_started = False
    #while True:
    try:
        if not thread_started:
            #logger("main: start TTS thread")
            #start_new_thread(thread_TTS, (q_txt_llm, ))
            #logger("main: start LLM thread")
            #start_new_thread(thread_LLM, (q_txt_stt, q_txt_llm, ))
            #logger("main: start RecognizeWisper")
            #RecordConvert(q_wave_path)
            #start_new_thread(RecordConvert, (q_wave_path, ))
            
            #logger("main: start RecognizeWisper")
            #stt_text = RecognizeWisper(q_wave_path, q_txt_stt)
            #start_new_thread(RecognizeWisper, (q_wave_path, q_txt_stt, ))
            stt_text = "안녕"
            outputText = callLlama(stt_text)
            callTTS(outputText)
            
            thread_started=True
        else:
            pass
    except Exception as e:
        logger("main thread: end by except {}".format(e))

    logger("main thread: finish")
     

     
if __name__=="__main__":
    '''
    cd /home/nvidia/whisper.cpp/build/bin && \
    ./server --language ko -m ../../models/ggml-base.bin
    '''
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)#, datefmt="%H:%M:%S")
    parser = argparse.ArgumentParser(description='RSSAEM Bot')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--stt_url', type=str, default=STT_URL)
    parser.add_argument('--llm_url', type=str, default=LLM_URL)
    parser.add_argument('--llm_n_predict', type=int, default=LLM_N_PREDICT)
 
    args = parser.parse_args()
    main(args)
#plays the audio file
#playcommand = "aplay " + output_file
#os.system(playcommand)
