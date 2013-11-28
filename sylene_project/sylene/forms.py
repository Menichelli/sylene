# -*- coding: latin-1 -*-

from django.forms import ModelForm
from models import *


class DocumentVeilleForm(ModelForm):
    class Meta:
        model = DocumentVeille
        fields = ['fichier']