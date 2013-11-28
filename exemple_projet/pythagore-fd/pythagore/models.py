from django.db import models

from django.contrib.auth.models import User

class Categorie(models.Model):
   nom = models.CharField(max_length=200)
   desc = models.TextField()
   
   def __unicode__(self):
      return "id: "+str(self.id)+" nom: "+self.nom

class Formation(models.Model):
   nom = models.CharField(max_length=200)
   desc = models.TextField()
   cat = models.ForeignKey(Categorie)

   def __unicode__(self):
      return "id: "+str(self.id)+" cat_id: "+str(self.cat_id)+" description: "+self.desc

class Commande(models.Model):
   client = models.ForeignKey(User)
   formation = models.ForeignKey(Formation)
   date = models.DateField(auto_now_add=True)

   def __unicode__(self):
      return "id: "+str(self.id)+" client_id: "+str(self.client_id)+" formation_id: "+str(self.formation_id)+" date: "+str(self.date)
