# -*- coding: latin-1 -*-

from django.db import models
from django.core.exceptions import ValidationError
import datetime

class Document(models.Model):
    date_publiee = models.DateField('Date publiee',auto_now=True,help_text="La date a laquelle le document est poste")
    dernier_visionnage = models.DateField(default=datetime.datetime.fromtimestamp(0),help_text="La derniere fois que le document a ete visionne.")

    class Meta:
        abstract = True

class DocumentVeille(Document,models.Model):
    fichier = models.FileField(upload_to='document_veille/%Y_%m')
    lien_image = models.CharField(max_length=500,help_text="Le lien vers l'image correspondante")

    def clean(self):
        if not self.fichier.name.endswith('.pdf'):
            raise ValidationError(u'Le fichier doit etre un pdf!')

    def __unicode__(self):
        return self.fichier.name

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
    lien_image = models.CharField(max_length=500,help_text="Le lien vers l'image correspondante")
    frequence = models.IntegerField() # 1 pour toutes les 30min || 2 pour toutes les heures || possiblement extensible, voir views

    def clean(self):
        if self.dateDebut >= self.dateFin:
            raise ValidationError('La date de fin ne peut etre anterieur a la date de debut.')

    class Meta:
        verbose_name_plural = "Messages PDF"

class MessageSimple(Message):
    message = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Messages Simples"