from django.db import models


class MaterialType(models.Model):
    name = models.CharField(max_length=300)


class Emotion(models.Model):
    name = models.CharField(max_length=300)


class Material(models.Model):
    type = models.ForeignKey(MaterialType)
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=300)
    picUrl = models.CharField(max_length=300)
    emotion = models.ManyToManyField(Emotion)
