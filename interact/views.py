from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse
from RUOK.tools import *
from threading import Thread
import soundfile as sf
import requests
import time
import io
import json
import random

context = ""
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
    global context
    content = request.body.decode()
    rett = []
    ret = None
    if context == "":
        dic = {
            "context": "",
            "input": ""
        }
    else:
        dic = {
            "context": context,
            "input": {"text": content}
        }
        analyze = toneAnnalyze(content={"text": content})
        ret = foo(analyze)
    url = "http://localhost:3000/api/message"
    headers = {'Content-Type': 'application/json'}
    print(json.dumps(dic))
    r = requests.post(url=url, data=json.dumps(dic), headers=headers)
    text = json.loads(r.text)
    r.close()
    reply = text['output']['text']
    context = text['context']
    rett.append({
        "type": "plain",
        "content": reply
    })
    if ret is not None:
        rett.append({
            "type": "plain",
            "content": getReply(ret['materialType'])
        })
        rett.append(ret)
    return JsonResponse(rett, safe=False)


def speechToContext():
    data = open('output.flac', 'rb')
    url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
    headers = {"Content-Type": "audio/flac"}
    r = requests.post(url=url, data=data, headers=headers,
                      auth=("6ae3ccae-5cd6-4b51-9d50-0929c13cdd10", "M6cohYbk2YuG"))
    text = json.loads(r.text)
    r.close()
    if len(text["results"]) == 0:
        return None
    text = text["results"][0]["alternatives"][0]["transcript"]
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


def foo(data):
    data = json.loads(data)
    tones = data['document_tone']['tones']
    emotion = ""
    score = 0
    for tone in tones:
        if tone['score'] > score:
            emotion = tone['tone_id']
            score = tone['score']
    if score < 0.6:
        return None
    else:
        return material(emotion)


def material(name):
    if Emotion.objects.filter(name=name).exists() == False:
        return None
    emotion = Emotion.objects.get(name=name)
    materials = emotion.material_set.all()
    material = materials[getRnd(len(materials))]
    dict = {
        'type': 'text-image',
        'url': material.url,
        'title': material.title,
        'content': material.content,
        'picUrl': material.picUrl,
        'materialType': material.type.name
    }
    return dict


def getReply(type):
    ret = {
        "movie": [],
        "book": [],
        "music": []
    }
    ret["movie"].append("Let's watch a movie together!")
    ret["movie"].append("A movie a day, keeps the sadness away!")
    ret["book"].append("Why not just read a book?")
    ret["book"].append("How about read a book together?")
    ret["book"].append("This book may help you~")
    ret["music"].append("Get relaxed with some songs~")
    ret["music"].append("This song is just for you(づ￣ 3￣)づ")
    return ret[type][getRnd(len(ret[type]))]


def getRnd(n):
    s = random.random() * 1000
    return s % n
