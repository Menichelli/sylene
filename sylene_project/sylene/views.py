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

from models import *
from forms import DocumentVeilleForm

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

#Called by: viewer/
#Le viewer
def viewer(request):
    #with open('resources/document_veille/2013_11/Cyber_-_Veille_-_Espionnage_Industriel_1.pdf', 'r') as pdf:
    #    response = HttpResponse(pdf.read(), mimetype='application/pdf')
    ##    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    #    return response
    #pdf.closed
    return render_to_response('viewer.html',context_instance=RequestContext(request))

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
#Permet de créer un utilisateur
@login_required
def add_user(request):
    if request.user.is_authenticated():
        logged = True
        username = get_user(request).username
        return render_to_response('add_user.html', {'logged' : logged, 'username' : username}, context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden

#Called by: /userpanel/create_user/
#Crée le compte utilisateur à partir du formulaire /userpanel/add_user/
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
#Permet d'ajouter des veilles techno à partir du pdf
@login_required
def add_tech_survey(request):
    request.FILES.clear()
    return render_to_response('add_tech_survey.html', {'logged' : True, 'username' : get_user(request).username}, context_instance=RequestContext(request))

#Called by: /userpanel/conf_tech_survey/
#Récupère les fichiers sélectionnés et les enregistre
def conf_tech_survey(request):
    fichiers_acceptes = []
    fichiers_refuses = []
    for fichier in request.FILES.getlist('doc'):
        try :
            dv = DocumentVeille(nom="todo",prenom="todo",fichier=fichier)
            dv.clean()
            dv.save()
            fichiers_acceptes.append(fichier)
        except Exception as e:
            print(e)
            fichiers_refuses.append(fichier)
        try :
            with Image(filename="/var/resources/"+dv.fichier.name+"[0]") as img:
                img.save(filename="/var/resources/"+dv.fichier.name+".jpg")
                dv.lien_image("/var/resources/"+dv.fichier.name+".jpg")
        except Exception as e:
            print(e)
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
#Permet à l'utilisateur de se déconnecter
def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")

#Called by: /nyi/
#Not Yet Implemented
def nyi(request):
    return render_to_response('nyi.html', {}, context_instance=RequestContext(request))