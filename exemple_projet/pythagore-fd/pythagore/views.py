# -*- coding: latin-1 -*-

from django.http import *
from django.shortcuts import *
from django.template import *
from pythagore.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.core.context_processors import csrf

# Appelée pour l'url /
# Affiche la page de présentation
def home(request):
   categories = Categorie.objects.all()
   if request.user.id != None:
      logged = True
   else:
      logged = False
   return render_to_response('presentation.html', { 'categories' : categories, 'logged' : logged}, context_instance=RequestContext(request))

# Appelée pour l'url /panier/vider uniquement si l'utilisateur est loggé
# Permet à l'utilisateur de vider son panier
@login_required
def vider_panier(request):
   request.session["commandes"] = []
   categories = Categorie.objects.all()
   return render_to_response('panier_view.html', { 'categories' : categories, 'logged' : True, 'formations' : [], 'message' : "Le panier a été vidé."}, context_instance=RequestContext(request))

# Appelée pour l'url /panier/valider uniquement si l'utilisateur est loggé
# Permet à l'utilisateur de valider son panier
@login_required
def valider_panier(request):
   for formation_id in request.session["commandes"]:
      commande = Commande(client_id=request.user.id, formation_id=formation_id)
      commande.save()
   request.session["commandes"] = []
   categories = Categorie.objects.all()
   return render_to_response('panier_view.html', { 'categories' : categories, 'logged' : True, 'formations' : [], 'message' : "La commande a été passée avec succès!"}, context_instance=RequestContext(request))

# Appelée pour l'url /commander/formation_id uniquement si l'utilisateur est loggé
# Permet à l'utilisateur d'ajouter une formation à son panier
@login_required
def commander(request, formation_id):
   if formation_id in request.session["commandes"]:
      message = "Vous avez déjà commandé cette formation!"
   else:
      message = "Formation ajoutée à votre panier."
      request.session["commandes"] += formation_id
   categories = Categorie.objects.all()
   logged = True
   return render_to_response('presentation.html', { 'categories' : categories, 'logged' : logged, 'message' : message}, context_instance=RequestContext(request))

# Appelée pour l'url /chart/ uniquement si l'utilisateur est loggé
# Permet à l'utilisateur de voir le contenu de son panier
@login_required
def panier_view(request):
   categories = Categorie.objects.all()
   formations = []
   for i in request.session["commandes"]:
      formations.append(Formation.objects.get(id = i))
   return render_to_response('panier_view.html', { 'categories' : categories, 'logged' : True, 'formations' : formations}, context_instance=RequestContext(request))

# Appelée pour l'url /cat/
# Permet à l'utilisateur de voir le catalogue des formations
def catalogue(request):
   categories = Categorie.objects.all()
   if request.user.id != None:
      logged = True
   else:
      logged = False
   return render_to_response('catalogue.html', { 'categories' : categories, 'logged' : logged }, context_instance=RequestContext(request))

# Appelée pour l'url /cat/cat_id
# Permet à l'utilisateur de voir les formations présentes dans cette catégorie
def cat_detail(request, cat_id):
   categories = Categorie.objects.all()
   formations = Formation.objects.filter(cat = cat_id)
   nom_cat = Categorie.objects.get(id = cat_id).nom
   if request.user.id != None:
      logged = True
   else:
      logged = False
   return render_to_response('cat_detail.html', {'nom_cat' : nom_cat, 'categories' : categories, 'formations' : formations, 'logged' : logged }, context_instance=RequestContext(request))

# Appelée pour l'url /formation/formation_id
# Permet à l'utilisateur d'avoir le détail de la formation
def formation_detail(request, formation_id):
   categories = Categorie.objects.all()
   formation = Formation.objects.get(id = formation_id)
   if request.user.id != None:
      logged = True
   else:
      logged = False
   return render_to_response('formation_detail.html', {'categories' : categories, 'formation' : formation, 'logged' : logged }, context_instance=RequestContext(request))

# Appelée pour l'url /register/
# Permet à un utilisateur de s'enregistrer
def register_form(request):
   categories = Categorie.objects.all()
   logout(request)
   logged = False
   return render_to_response('register_form.html', {'categories' : categories, 'logged' : logged}, context_instance=RequestContext(request))

# Appelée pour l'url /register/validate
# Permet de valider l'inscription de l'utilisateur
def register_validate(request):
   username = request.POST['username']
   password = request.POST['password']
   email = request.POST['email']
   
   try:
      User.objects.create_user(username, email, password)
      return HttpResponseRedirect("/")
   except Exception as exc:
      categories = Categorie.objects.all()
      logged = False
      return render_to_response('register_form.html', {'categories' : categories, 'logged' : logged, 'message' : exc}, context_instance=RequestContext(request))

# Appelée pour l'url /login/
# Permet à l'utilisateur de s'authentifier
def login_(request):
   username = request.POST['username']
   password = request.POST['password']
   user = authenticate(username=username, password=password)
   c = {}
   c.update(csrf(request))
   if user!=None:
      if user.is_active:
         request.session["commandes"] = []
         login(request, user)
         return HttpResponseRedirect("/")
   categories = Categorie.objects.all()
   return render_to_response('presentation.html', { 'categories' : categories, 'logged' : False, 'message' : "Erreur de login/mot de passe"}, context_instance=RequestContext(request))

# Appelée pour l'url /logout/
# Permet à l'utilisateur de se déconnecter
@login_required
def logout_(request):
   logout(request)
   return HttpResponseRedirect("/")
