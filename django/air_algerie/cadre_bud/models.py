from django.contrib.auth.models import User
from django.db import models


class compte(models.Model):
    scf = models.IntegerField(unique=True,null=True,blank=True)
    rubrique = models.CharField(max_length=100,null=True,blank=True)
    type_compte = models.CharField(max_length=50)
    reseau_compte= models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.scf)




# khaliha
class profile(models.Model):
    nom_user = models.CharField(max_length=100,null=True,blank=True)
    prenom_user = models.CharField(max_length=100,null=True,blank=True)
    type_user = models.CharField(max_length=100,null=True,blank=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    


    def __str__(self):
        return '{} {}'.format(self.nom_user , self.prenom_user)

  


# khaliha
class monnaie(models.Model):
    code_monnaie=models.CharField(max_length=3,null=True, blank=True)
    lib_monnaie=models.CharField(max_length=10,null=True, blank=True)

    def __str__(self):
        return self.code_monnaie




# khaliha
class unite_1(models.Model):
    code_unite=models.CharField(max_length=50,null=True, blank=True)
    reseau = models.CharField(max_length=50,null=True, blank=True)
    pays = models.CharField(max_length=50,null=True, blank=True)
    lib_monnaie=models.ForeignKey(monnaie,on_delete=models.CASCADE,default=None)
    commeriale=models.CharField(max_length=1,null=True, blank=True)
    etranger=models.CharField(max_length=1,null=True, blank=True)
    tresorie=models.CharField(max_length=1,null=True, blank=True)
    Trafic_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Emission_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Recette_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    Exploitation_Indicateur=models.CharField(max_length=1,null=True, blank=True)
    def __str__(self):
        return self.code_unite



# khaliha
class taux_change(models.Model):
    code_moneeée = models.ForeignKey(monnaie,on_delete=models.CASCADE,default=None)
    Taux = models.FloatField(null=True,blank=True)
    mois = models.CharField(max_length=20,null=True,blank=True)
    annee = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.Taux)

class unite_profile(models.Model):
        unite = models.ForeignKey(unite_1,on_delete=models.CASCADE,default=None)
        pro =  models.ForeignKey(profile,on_delete=models.CASCADE,default=None)

        def __str__(self):
          return'{} {}'.format(self.unite,self.pro)


# khaliha
class entete_pv(models.Model):
    annee = models.IntegerField(null=True,blank=True)
    unite = models.ForeignKey(unite_1,on_delete=models.CASCADE,default=None)
    rempli=models.BooleanField(default=False,blank=True)  
    type = models.CharField(max_length=20,null=True,blank=True)
    
    def __str__(self):
        return '{} {} {}'.format(self.type,str(self.annee),self.unite)

class runion(models.Model):
    annee = models.IntegerField(null=True,blank=True)
    etat = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return str(self.annee)

# class entete_realisation2(models.Model):
#     annee = models.IntegerField(null=True,blank=True)
#     unite = models.ForeignKey(unite_1,on_delete=models.CASCADE,default=None)
#     type = models.CharField(max_length=20,null=True,blank=True)

#     def __str__(self):
#         return '{} {} {}'.format(self.type,str(self.annee),self.unite)


class realisation2(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    realisation = models.FloatField(null=True,blank=True)
    type1= models.CharField(max_length=20,null=True,blank=True)
    scf = models.IntegerField(blank=True,null=True)  
    rempli=models.BooleanField(default=False,blank=True)  
    commentaire = models.CharField(max_length=100,null=True,blank=True)
    regler_par = models.CharField(max_length=100,null=True,blank=True)
    monnie = models.CharField(max_length=100,null=True,blank=True)
    cdd=models.BooleanField(default=False,blank=True) 
    

    def __str__(self):
     
        return '{} {} {}'.format(self.pv,self.type,self.rubrique)


class historique(models.Model):
    annee=models.IntegerField(blank=True,null=True)
    type = models.CharField(max_length=20,null=True,blank=True)
    type_1 =models.CharField(max_length=20,null=True,blank=True)
    user = models.CharField(max_length=100,null=True,blank=True)
    date_h = models.CharField(max_length=100,null=True,blank=True)

# # khaliha
# #class trafic(models.Model):
#     pv = models.ForeignKey(unite_1,on_delete=models.CASCADE,default=None)
#     mois = models.CharField(max_length=20,null=True,blank=True)
#     rubrique = models.CharField(max_length=20,null=True,blank=True)
#     montant = models.FloatField(null=True,blank=True)
#     annuel = models.FloatField(null=True,blank=True)

#     def __str__(self):
#         return str(self.pk)
# proposition (type : trafic / recette / ca / depenses  !!!! type 1 : fonctionnement ou exploitation )
class proposition(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    cloture = models.FloatField(null=True,blank=True)
    prevision = models.FloatField(null=True,blank=True)
    type1= models.CharField(max_length=20,null=True,blank=True)
    scf = models.IntegerField(blank=True,null=True)  
    rempli=models.BooleanField(default=False,blank=True)  
    commentaire = models.CharField(max_length=100,null=True,blank=True)
    regler_par = models.CharField(max_length=100,null=True,blank=True)
    monnie = models.CharField(max_length=100,null=True,blank=True)
   

    def __str__(self):
     
        return '{} {} {}'.format(self.pv,self.type,self.rubrique)



#table comptes
class Pos1(models.Model):
    scf = models.IntegerField(blank=True,unique=True)
    lib =  models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.scf)


class Pos2(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos1,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)

        
class Pos3(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos2,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)

class Pos6(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos3,on_delete=models.CASCADE,default=None)
    type = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return str(self.scf)
        
class unite_pos6(models.Model):
    unite = models.ForeignKey(unite_1,on_delete=models.CASCADE,default=None)
    pos6 =  models.ForeignKey(Pos6,on_delete=models.CASCADE,default=None)
    type = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
          return'{} {}'.format(self.unite,self.pos6)

class Pos7(models.Model):
    scf = models.IntegerField(blank=True,unique=True)    
    lib =  models.CharField(max_length=100,null=True,blank=True)
    ref = models.ForeignKey(Pos6,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return str(self.scf)


####




class controle_bud(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    ec = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    mois =  models.CharField(max_length=20,null=True,blank=True)
    montant = models.FloatField(null=True,blank=True)
    type1= models.CharField(max_length=20,null=True,blank=True)
    scf = models.IntegerField(blank=True,null=True)  
    rempli=models.BooleanField(default=False,blank=True) 

    def __str__(self):
     
        return '{} {} {}'.format(self.ec,self.type,self.rubrique)

class reunion_bud(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    proposition =  models.CharField(max_length=20,null=True,blank=True)
    realisation_1 = models.FloatField(null=True,blank=True)
    realisation_2 = models.FloatField(null=True,blank=True)
    controle_budgetaire = models.FloatField(null=True,blank=True)
    cloture = models.FloatField(null=True,blank=True)
    prevision = models.FloatField(null=True,blank=True)
    mois_controle = models.CharField(max_length=20,null=True,blank=True)
    annee = models.IntegerField(blank=True,null=True) 
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd1=models.BooleanField(default=False,blank=True) 
    sd1=models.BooleanField(default=False,blank=True) 
    is_valide=models.BooleanField(default=False,blank=True) 
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    date1=models.CharField(max_length=20,null=True,blank=True)
    date2=models.CharField(max_length=20,null=True,blank=True)
    date3=models.CharField(max_length=20,null=True,blank=True)
    cadre =  models.ForeignKey(profile,related_name="cadre",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd",on_delete=models.CASCADE,default=None,null=True)


    def __str__(self):
        return str(self.type)


class modification(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    type_modif = models.CharField(max_length=20,null=True,blank=True)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    notifie = models.FloatField(default=0,blank=True)
    modif = models.FloatField(default=0,blank=True)
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd1=models.BooleanField(default=False,blank=True) 
    sd1=models.BooleanField(default=False,blank=True) 
    monnaie=models.CharField(max_length=100,null=True,blank=True)
    is_valide=models.BooleanField(default=False,blank=True)
    date1=models.CharField(max_length=20,null=True,blank=True)
    date2=models.CharField(max_length=20,null=True,blank=True)
    date3=models.CharField(max_length=20,null=True,blank=True)
   
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    cadre =  models.ForeignKey(profile,related_name="cadre3",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd3",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd3",on_delete=models.CASCADE,default=None,null=True)

    def __str__(self):
        return str(self.type)

class historique_modification(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    type_modif = models.CharField(max_length=20,null=True,blank=True)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    notifie = models.FloatField(null=True,blank=True)
    modif = models.FloatField(default=0,blank=True)
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd1=models.BooleanField(default=False,blank=True) 
    sd1=models.BooleanField(default=False,blank=True) 
    monnaie=models.CharField(max_length=100,null=True,blank=True)
    is_valide=models.BooleanField(default=False,blank=True)
    date1=models.CharField(max_length=20,null=True,blank=True)
    date2=models.CharField(max_length=20,null=True,blank=True)
    date3=models.CharField(max_length=20,null=True,blank=True)
   
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    cadre =  models.ForeignKey(profile,related_name="cadre4",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd4",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd4",on_delete=models.CASCADE,default=None,null=True)

    def __str__(self):
        return str(self.type)



class notifie_bud(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    prevision = models.FloatField(null=True,blank=True)
    annee = models.IntegerField(blank=True,null=True) 
    monnaie=models.CharField(max_length=100,null=True,blank=True)
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd1=models.BooleanField(default=False,blank=True) 
    sd1=models.BooleanField(default=False,blank=True) 
    is_valide=models.BooleanField(default=False,blank=True)  
    date1=models.CharField(max_length=20,null=True,blank=True)
    date2=models.CharField(max_length=20,null=True,blank=True)
    date3=models.CharField(max_length=20,null=True,blank=True)
    modification =  models.ForeignKey(modification,related_name="modification",on_delete=models.CASCADE,default=None,null=True)
    cadre =  models.ForeignKey(profile,related_name="cadre1",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd1",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd1",on_delete=models.CASCADE,default=None,null=True)
    def __str__(self):
        return str(self.type)



class notifie_bud_m(models.Model):
    type = models.CharField(max_length=20,default=0,blank=True)
    rubrique =  models.CharField(max_length=20,null=True,blank=True)
    janvier = models.FloatField(default=0,blank=True)
    fevrier = models.FloatField(default=0,blank=True)
    mars = models.FloatField(default=0,blank=True)
    avril = models.FloatField(default=0,blank=True)
    mai = models.FloatField(default=0,blank=True)
    juin = models.FloatField(default=0,blank=True)
    juillet = models.FloatField(default=0,blank=True)
    aout = models.FloatField(default=0,blank=True)
    septembre = models.FloatField(default=0,blank=True)
    octobre = models.FloatField(default=0,blank=True)
    novembre = models.FloatField(default=0,blank=True)
    decembre = models.FloatField(default=0,blank=True)
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd1=models.BooleanField(default=False,blank=True) 
    sd1=models.BooleanField(default=False,blank=True) 
    monnaie=models.CharField(max_length=100,null=True,blank=True)
    pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
    cadre =  models.ForeignKey(profile,related_name="cadre2",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd2",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd2",on_delete=models.CASCADE,default=None,null=True)
    is_valide=models.BooleanField(default=False,blank=True)


    def __str__(self):
        return str(self.type)








# class modification_mm(models.Model):
#     type = models.CharField(max_length=20,default=0,blank=True)
#     type_modif = models.CharField(max_length=20,null=True,blank=True)
#     rubrique =  models.CharField(max_length=20,null=True,blank=True)
#     janvier = models.FloatField(default=0,blank=True)
#     fevrier = models.FloatField(default=0,blank=True)
#     mars = models.FloatField(default=0,blank=True)
#     avril = models.FloatField(default=0,blank=True)
#     mai = models.FloatField(default=0,blank=True)
#     juin = models.FloatField(default=0,blank=True)
#     juillet = models.FloatField(default=0,blank=True)
#     aout = models.FloatField(default=0,blank=True)
#     septembre = models.FloatField(default=0,blank=True)
#     octobre = models.FloatField(default=0,blank=True)
#     novembre = models.FloatField(default=0,blank=True)
#     decembre = models.FloatField(default=0,blank=True)
#     cadre1=models.BooleanField(default=False,blank=True) 
#     cdd1=models.BooleanField(default=False,blank=True) 
#     sd1=models.BooleanField(default=False,blank=True) 
#     pv = models.ForeignKey(entete_pv,on_delete=models.CASCADE,default=None)
#     cadre =  models.ForeignKey(profile,related_name="cadre222",on_delete=models.CASCADE,default=None,null=True)
#     cdd =  models.ForeignKey(profile,related_name="cdd222",on_delete=models.CASCADE,default=None,null=True)
#     sd =  models.ForeignKey(profile,related_name="sd222",on_delete=models.CASCADE,default=None,null=True)
#     is_valide=models.BooleanField(default=False,blank=True)


#     def __str__(self):
#         return str(self.type)






    
        

"""class actualisation(models.Model):
    type = models.CharField(max_length=20,null=True,blank=True)
    proposition = models.ForeignKey(proposition,on_delete=models.CASCADE,default=None)
    controle_budgetaire = models.FloatField(null=True,blank=True)
    cloture = models.FloatField(null=True,blank=True)
    prevision = models.FloatField(null=True,blank=True)
    mois_controle = models.CharField(max_length=20,null=True,blank=True)
    cadre1=models.BooleanField(default=False,blank=True) 
    cdd=models.BooleanField(default=False,blank=True) 
    sd=models.BooleanField(default=False,blank=True) 
    cadre =  models.ForeignKey(profile,related_name="cadre1",on_delete=models.CASCADE,default=None,null=True)
    cdd =  models.ForeignKey(profile,related_name="cdd1",on_delete=models.CASCADE,default=None,null=True)
    sd =  models.ForeignKey(profile,related_name="sd1",on_delete=models.CASCADE,default=None,null=True)


    def __str__(self):
        return str(self.type)

"""