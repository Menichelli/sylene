# -*- coding: latin-1 -*-

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime

class Document(models.Model):
    date_publiee = models.DateField('Date publiee',auto_now=True,help_text="La date a laquelle le document est poste")

    class Meta:
        abstract = True

class DocumentVeille(Document,models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    actif = models.BooleanField(default=True,help_text="Seul les documents actifs seront affiches sur le Viewer")
    fichier = models.FileField(upload_to='document_veille/%Y_%m')
    lien_image = models.CharField(max_length=500,help_text="Le lien vers l'image correspondate")

    def clean(self):
        if not self.fichier.name.endswith('.pdf'):
            raise ValidationError(u'Le fichier doit etre un pdf!')

    class Meta:
        verbose_name_plural = "Documents Veilles"

class Message(Document):
    dateDebut = models.DateTimeField('Date de debut')
    dateFin = models.DateTimeField('Date de fin')

    def clean(self):
        if self.dateDebut >= self.dateFin:
            raise ValidationError('La date de fin ne peut etre anterieur a la date de debut.')

    class Meta:
        abstract = True

class MessagePDF(Message):
    fichier = models.FileField(upload_to='msg_pdf/')
    important = models.BooleanField(default=False,help_text="Si le message est important, alors il sera prioritaire sur les veilles techno")

    def clean(self):
        if self.dateDebut >= self.dateFin:
            raise ValidationError('La date de fin ne peut etre anterieur a la date de debut.')

    class Meta:
        verbose_name_plural = "Messages PDF"

class MessageSimple(Message):
    message = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Messages Simples"