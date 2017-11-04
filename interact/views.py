from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from RUOK.tools import *
import _thread
import requests


def start(request):
    _thread.start_new_thread(record())


def stop(request):
    stopRecord()


def process(request):
    # return HttpResponse(toneAnnalyze())
    return HttpResponse(speechToContext())


def speechToContext():
    data = open('D:/HowRU/audio-file.flac', 'rb')
    url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
    headers = {"Content-Type": "audio/flac"}
    r = requests.post(url=url, data=data, headers=headers,
                      auth=("6ae3ccae-5cd6-4b51-9d50-0929c13cdd10", "M6cohYbk2YuG"))
    text = r.text
    r.close()
    return text


def toneAnnalyze():
    data = open('D:/HowRU/tone.json', 'rb')
    url = "https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2017-09-21"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, data=data, headers=headers,
                      auth=("a9ea6f28-f65b-4de5-9646-07c33cb6560d", "LvCBRJjsdfBB"))
    text = r.text
    r.close()
    return text
