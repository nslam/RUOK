from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from RUOK.tools import *
from threading import Thread
import soundfile as sf
import requests
import time
import io
import json

q = queue.Queue()


def start(request):
    t1 = Thread(target=record, args=(q,))
    t1.start()
    return HttpResponse('start')


def stop(request):
    t2 = Thread(target=stopRecord, args=(q,))
    t2.start()
    time.sleep(0.2)
    data, samplerate = sf.read('output.wav')
    sf.write('output.flac', data, samplerate)
    return HttpResponse(speechToContext())


def process(request):
    content = request.body.decode()
    text = toneAnnalyze(content={"text": content})
    return HttpResponse(text)


def speechToContext():
    data = open('output.flac', 'rb')
    url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
    headers = {"Content-Type": "audio/flac"}
    r = requests.post(url=url, data=data, headers=headers,
                      auth=("6ae3ccae-5cd6-4b51-9d50-0929c13cdd10", "M6cohYbk2YuG"))
    text = r.text
    r.close()
    return text


def toneAnnalyze(content):
    with open('1.json', 'w') as f:
        f.write(json.dumps(content))
        f.close()
    data = open('1.json', 'rb')
    url = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, data=data, headers=headers,
                      auth=("a9ea6f28-f65b-4de5-9646-07c33cb6560d", "LvCBRJjsdfBB"))
    text = r.text
    r.close()
    return text
