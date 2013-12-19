# -*- coding: latin-1 -*-
from django.http import *
from django.shortcuts import *
from django.template import *
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.contrib.auth.decorators import *
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.context_processors import csrf
from wand.image import Image
from django.db.models.query import QuerySet
from operator import attrgetter
import functools
from datetime import datetime, timedelta

from models import *

#Called by: /
#
def home(request):
    if request.user.is_authenticated():
        logged = True
        username = get_user(request).username
        return render_to_response('index.html', {'logged' : logged, 'username' : username}, context_instance=RequestContext(request))
    else:
        logged = False
        return render_to_response('index.html', {'logged' : logged}, context_instance=RequestContext(request))

#Called by: /viewer/
#Le viewer
def viewer(request):
    found = False #si on a trouve quelque chose a afficher
    message = ""
    doc_url = ""

    #on recupere un message simple s'il y en a un a afficher
    qs = MessageSimple.objects.all().exclude(dateFin__lt=datetime.datetime.now, dateDebut__gt=datetime.datetime.now()).order_by("dernier_visionnage")
    if qs.count()!=0:
        msgSimple = qs[0]
        msgSimple.dernier_visionnage = datetime.datetime.now()
        msgSimple.save()
        message = msgSimple.message

    #un message pdf toutes les 30min
    qs = MessagePDF.objects.all().exclude(dateFin__lt=datetime.datetime.now(), dateDebut__gt=datetime.datetime.now()).filter(frequence__exact=1).order_by("dernier_visionnage")
    if qs.count()!=0:
        msgPDF = qs[0]
        if msgPDF.dernier_visionnage > datetime.timedelta(minutes=30): # frequence 1: toutes les 30 minutes
            msgPDF.dernier_visionnage = datetime.datetime.now()
            msgPDF.save()
            doc_url = msgPDF.lien_image
            found = True

    #un message pdf toutes les heures
    if found==False:
        qs = MessagePDF.objects.all().exclude(dateFin__lt=datetime.datetime.now(), dateDebut__gt=datetime.datetime.now()).filter(frequence__exact=2).order_by("dernier_visionnage")
        if qs.count()!=0:
            msgPDF = qs[0]
            if msgPDF.dernier_visionnage > datetime.timedelta(hours=1): # frequence 2: toutes les heures
                msgPDF.dernier_visionnage = datetime.datetime.now()
                msgPDF.save()
                doc_url = msgPDF.lien_image
                found = True

    #si on a toujours rien trouve, on va chercher une veille techno
    if found==False:
        listDV = DocumentVeille.objects.all().order_by("-date_publiee")[:settings.NB_ETUDIANT]
        tmp1 = []
        for e in listDV:
            tmp1.append(e)
        tmp2 = sorted(tmp1,lambda x, y: cmp(x.dernier_visionnage,y.dernier_visionnage),reverse=False)
        if len(tmp2)!=0:
            dv = tmp2[0]
            dv.dernier_visionnage = datetime.datetime.now()
            dv.save()
            doc_url = msgPDF.lien_image
            found = True
    if found==True:
        return render_to_response('viewer.html', {'image_url' : doc_url, 'message' : message}, context_instance=RequestContext(request))
    else:
        return HttpResponse(status=500)

#Called by: /userpanel/
#Le panel utilisateur
@login_required
def userpanel(request):
    if request.user.is_authenticated():
        logged = True
        username = get_user(request).username
        return render_to_response('userpanel.html', {'logged' : logged, 'username' : username}, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden

#Called by: /userpanel/add_user/
#Permet de cr�er un utilisateur
@login_required
def add_user(request):
    if request.user.is_authenticated():
        logged = True
        username = get_user(request).username
        return render_to_response('add_user.html', {'logged' : logged, 'username' : username}, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden

#Called by: /userpanel/create_user/
#Cr�e le compte utilisateur � partir du formulaire /userpanel/add_user/
@login_required
def create_user(request):
    username = request.POST['username']
    last_name = request.POST['name']
    first_name = request.POST['first_name']
    email = request.POST['email']
    password = request.POST['pwd1']
    try:
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        user.save
        return render_to_response('add_user.html', {'logged' : True, 'username' : get_user(request).username, 'success' : True, 'msg' : 'Ajout reussi.'}, context_instance=RequestContext(request))
    except Exception as msg:
        return render_to_response('add_user.html', {'logged' : True, 'username' : get_user(request).username, 'success' : False, 'msg' : msg}, context_instance=RequestContext(request))

#Called by: /userpanel/add_tech_survey/
#Permet d'ajouter des veilles techno � partir du pdf
@login_required
def add_tech_survey(request):
    request.FILES.clear()
    return render_to_response('add_tech_survey.html', {'logged' : True, 'username' : get_user(request).username}, context_instance=RequestContext(request))

#Called by: /userpanel/conf_tech_survey/
#R�cup�re les fichiers s�lectionn�s et les enregistre
@login_required
def conf_tech_survey(request):
    fichiers_acceptes = []
    fichiers_refuses = []
    for fichier in request.FILES.getlist('doc'):
        try :
            dv = DocumentVeille(fichier=fichier)
            dv.clean()
            dv.save()
            with Image(filename="/var/resources/"+dv.fichier.name+"[0]",resolution=128) as img:
                img.format = 'png'
                img.save(filename="/var/resources/"+dv.fichier.name+".png")
                dv.lien_image = "/media/"+dv.fichier.name+".png"
            dv.clean()
            dv.save()
            fichiers_acceptes.append(fichier)
        except Exception as e:
            print(e)
            fichiers_refuses.append(fichier)
    request.FILES.clear()
    return render_to_response('conf_tech_survey.html', {'logged' : True, 'username' : get_user(request).username, 'fichiers_acceptes' : fichiers_acceptes, 'fichiers_refuses' : fichiers_refuses}, context_instance=RequestContext(request))

#Called by: login_/
#Permet de logger l'utilisateur
def login_(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    c = {}
    c.update(csrf(request))
    if user!=None:
        if user.is_active:
            login(request,user)
            return HttpResponseRedirect("/userpanel/")
    return HttpResponseRedirect("/")

#Called by: logout/
#Permet � l'utilisateur de se d�connecter
def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")

#Called by: /nyi/
#Not Yet Implemented
def nyi(request):
    return render_to_response('nyi.html', {}, context_instance=RequestContext(request))