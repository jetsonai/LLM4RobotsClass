#-*- coding:utf-8 -*-

import requests
import json
import os
import time
import numpy
 
url = 'http://127.0.0.1:8080/inference'
 
files1 = {
    'file': open('/home/nvidia/wav/goforward1.wav', 'rb'),
    'response-format': (None, 'json'),
}

files2 = {
    'file': open('/home/nvidia/wav/goback1.wav', 'rb'),
    'response-format': (None, 'json'),
}
 
response1 = requests.post(url, files=files1)
result1 = json.loads(response1.text)["text"]

print("[" + result1 + "]")

text11 = result1.replace("\n" , "")
print("[" + text11 + "]")

text12 = " 앞으로 가"

if(text11 == text12):
    print("go")
    os.system('cansend can0 001#64.00.00.00.64.00.00.00')
    time.sleep(3)

else:
    print("don't")

response2 = requests.post(url, files=files2)
result2 = json.loads(response2.text)["text"]

print("[" + result2 + "]")

text21 = result2.replace("\n" , "")
print("[" + text21 + "]")

text22 = " 뒤로 가"
    
if(text21 == text22):
    print("go")
    os.system('cansend can0 001#64.00.01.00.64.00.01.00')
    time.sleep(3)
    os.system('cansend can0 001#64.00.01.01.64.00.01.01')
    time.sleep(2)
else:
    print("don't")    


