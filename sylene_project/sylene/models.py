# -*- coding: latin-1 -*-

from django.db import models
from django.core.exceptions import ValidationError
import datetime

class Document(models.Model):
    """
    Objet abstrait qui defini les points communs a tous les documents.
    C'est a dire, une date de publication ainsi qu'une date du dernier visionnage.
    Cette derniere est fixee par defaut au 1er Janvier 1970 a la creation de l'objet.
    """
    date_publiee = models.DateField('Date publiee',auto_now=True,help_text="La date a laquelle le document est poste")
    dernier_visionnage = models.DateTimeField(default=datetime.datetime.fromtimestamp(0),help_text="La derniere fois que le document a ete visionne.")

    class Meta:
        """Permet de definir que l'objet est abstrait"""
        abstract = True

class DocumentVeille(Document,models.Model):
    """
    Un document de veille est typiquement un document au format pdf founi par les etudiants de Cyberdefense.
    Un document de veille est une sous classe de Document, a laquelle on ajoute un fichier au format pdf,
    ainsi qu'un lien vers l'image du png qui sera genere lors de la saisie du document.
    """
    fichier = models.FileField(upload_to='document_veille/%Y_%m')
    lien_image = models.CharField(max_length=500,help_text="Le lien vers l'image correspondante")

    def clean(self):
        """
        Permet de verifier la validite de l'objet document veille.
        """
        if not self.fichier.name.endswith('.pdf'):
            raise ValidationError(u'Le fichier doit etre un pdf!')

    def __unicode__(self):
        """
        Defini la representation sous forme de chaine de caractere de cette objet comme
        le nom du fichier qui lui est associe.
        """
        return self.fichier.name

    class Meta:
        """Permet de definir le pluriel de DocumentVeille pour l'interface d'administration"""
        verbose_name_plural = "Documents Veilles"

class Message(Document):
    """
    Objet abstrait, heritant de Document, permettant de definir les points communs aux differents Messages.
    Soit une date de debut et une date de fin.
    """
    dateDebut = models.DateTimeField('Date de debut')
    dateFin = models.DateTimeField('Date de fin')

    def clean(self):
        """Permet de verifier que la date de debut est bien anterieur a la date de fin."""
        if self.dateDebut >= self.dateFin:
            raise ValidationError('La date de fin ne peut etre anterieur a la date de debut.')

    class Meta:
        abstract = True

class MessagePDF(Message):
    """
    Objet qui represente un message au format PDF. Un MessagePDF est compose d'un fichier au format PDF
    ainsi qu'un lien vers l'image, generee a la creation de l'objet, du PDF et d'une frequence d'apparition.
    La frequence est geree par un nombre entier, 1 pour toutes les 30mins, 2 pour toutes les heures.
    """
    fichier = models.FileField(upload_to='msg_pdf/')
    lien_image = models.CharField(max_length=500,help_text="Le lien vers l'image correspondante")
    frequence = models.IntegerField(help_text="0 affichage permanent || 1 pour toutes les 30min || 2 pour toutes les heures") # 0 affichage permanent || 1 pour toutes les 30min || 2 pour toutes les heures || possiblement extensible, voir views

    def __unicode__(self):
        """Defini la representation sous forme de chaine de caracteres d'un MessagePDF comme le nom du fichier pdf associe."""
        return self.fichier.name

    class Meta:
        """Permet de definir le pluriel de MessagePDF"""
        verbose_name_plural = "Messages PDF"

class MessageSimple(Message):
    """
    Un MessageSimple est un Message compose uniquement d'une chaine de caractere qui sera affichee sous forme
    de bandeau dans la visionneuse.
    """
    message = models.CharField(max_length=200)

    def __unicode__(self):
        """Defini la representation sous forme de chaine de caracteres d'un MessageSimple comme le contenu du message."""
        return self.message

    class Meta:
        """Permet de definir le pluriel de MessageSimple"""
        verbose_name_plural = "Messages Simples"