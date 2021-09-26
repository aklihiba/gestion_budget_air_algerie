from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.shortcuts import redirect, render

from .forms import *
from .models import *


def get_max_historique(annee,type,type1):

    h = historique.objects.filter(annee=annee,type=type,type_1=type1)
    return h[len(h)-1]

def get_min_historique(annee,type,type1):

    h = historique.objects.filter(annee=annee,type=type,type_1=type1)
    return h[0]

 
# cette fonction traite la page login
def user_login(request):
    form = form_login(request.POST)
    if form.is_valid():
        user = authenticate(request,username=form.cleaned_data["username"],password=form.cleaned_data["password"])
        if user is not None:
            p = profile.objects.get(user=user)
            if p.type_user=='administrateur':
                login(request,user)
                return redirect("../../administrateur/admin_user")
            else:
                login(request,user)
                return redirect("pre_pre_proposition_budgetaire")   
        
    context = {
        'form':form_login
    }
    return render(request,'login.html' , context)
    
#cette fonction traite la page logout
def logout_page(request):
    logout(request)
    return redirect('login')

#page principale de proposition
def pre_pre_proposition_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    if p.type_user == "cadre_bud":
        x=True
    else:
        x=False
    
    up = unite_profile.objects.filter(pro=p)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste":poste,
        'unite':up,
        "x":x

    }
    return render(request,'pre_pre_proposition_budgetaire.html',context)

# 2eme principale de proposition
def pre_proposition_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')  
    currentYear = datetime.now().year+1
    test=datetime.now()

    request.session['annee']=currentYear
    u = unite_1.objects.get(pk=request.session["unite"])
    pv = entete_pv.objects.filter(unite=u,annee=currentYear,type="proposition")

    
    if pv.exists():
            return redirect('proposition_budgetaire')

    else:
            pv = entete_pv(unite=u,annee=currentYear,type="proposition")
            pv.save()
            request.session["pv"]=pv.id
            return redirect('proposition_budgetaire')
    
    return render(request,'proposition_budgetaire.html')

### modifier d'un nouveau budget
def edit_trafic_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    p=proposition.objects.filter(pv=pv,type='trafic')
    
    context = {
        'pro': p,
        'unite':u,
    
    }
    return render(request,'edit_proposition_trafic.html',context)

#MODIFICATION TRAFIC PROPOSITION
def update_trafic_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    cloture=request.POST.getlist('cloture')
    prevision=request.POST.getlist('prevision')
    rubrique=request.POST.getlist('rubrique')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_modif=datetime.now()
    print('*********************')
    print(commentaire)
    
   

    for i in range(len(cloture)) :
       p=proposition.objects.get(type='trafic',pv=pv,rubrique=rubrique[i])
       degre = request.POST.getlist('degre'+rubrique[i])
       print(degre)
       print('*********************')
       p.cloture=cloture[i]
       p.prevision=prevision[i]
       p.commentaire=commentaire[i]
       if (len(degre)>0):
            p.commentaire_degre= degre[0]
       p.save()
      
    h = historique(annee=pv.annee,type="proposition",type_1="trafic",user=name,date_h=date_modif)
    h.save()
    

    return redirect('proposition_budgetaire')

### modifier d'un nouveau budget recette
def edit_recette_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    p=proposition.objects.filter(pv=pv,type='recette')
    context = {
        'pro': p,
        'unite':u
    }
    return render(request,'edit_proposition_recette.html',context)

#MODIFICATION RECETTE PROPOSITION
 
def update_recette_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    cloture=request.POST.getlist('cloture')
    prevision=request.POST.getlist('prevision')
    rubrique=request.POST.getlist('rubrique')
    commentaire = request.POST.getlist('commentaire')
    
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_modif=datetime.now()

 


    for i in range(len(cloture)) :
       p=proposition.objects.get(type='recette',pv=pv,rubrique=rubrique[i])
       p.cloture=cloture[i]
       p.prevision=prevision[i]
       p.commentaire=commentaire[i]
       p.save()
    
    
    h = historique(annee=pv.annee,type="proposition",type_1="recette",user=name,date_h=date_modif)
    h.save()

    return redirect('proposition_budgetaire')



### modifier d'un nouveau budget emission
def edit_emission_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    p=proposition.objects.filter(pv=pv, type='emission')
    context = {
        'pro': p,
        'unite':u
    }
    return render(request,'edit_proposition_emission.html',context)
#MODIFICATION emission PROPOSITION
 
def update_emission_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    cloture=request.POST.getlist('cloture')
    prevision=request.POST.getlist('prevision')
    rubrique=request.POST.getlist('rubrique')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_modif=datetime.now()



    for i in range(len(cloture)) :
       p=proposition.objects.get(type='emission',pv=pv,rubrique=rubrique[i])
       p.cloture=cloture[i]
       p.prevision=prevision[i]
       p.commentaire=commentaire[i]
       p.save()
    
    
    h = historique(annee=pv.annee,type="proposition",type_1="emission",user=name,date_h=date_modif)
    h.save()

    return redirect('proposition_budgetaire')

    ### modifier d'un nouveau budget fonctionnement
def edit_fonctionnement_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    p=proposition.objects.filter(pv=pv,type='depenses',type1="FONCTIONNEMENT")
    m = monnaie.objects.all()
    context = {
        'pro': p,
        'unite':u,
        'monnaie':m
    }
    return render(request,'edit_proposition_fonctionnement.html',context)

#MODIFICATION  fonctionnement 
 
def update_fonctionnement_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    cloture=request.POST.getlist('cloture')
    prevision=request.POST.getlist('prevision')
    rubrique=request.POST.getlist('rubrique')
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_modif=datetime.now()


    


    for i in range(len(cloture)) :
       p=proposition.objects.get(type='depenses',type1="FONCTIONNEMENT",pv=pv,rubrique=rubrique[i])
       p.cloture=cloture[i]
       p.prevision=prevision[i]
       p.regler_par=regler[i]
       p.commentaire=commentaire[i]
       p.monnie=monnaie[i]
       
       p.save()

    
    h = historique(annee=pv.annee,type="proposition",type_1="FONCTIONNEMENT",user=name,date_h=date_modif)
    h.save()

    return redirect('proposition_depense')

     ### modifier d'un nouveau budget exploitation
def edit_exploitation_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    p=proposition.objects.filter(pv=pv,type='depenses',type1="EXPLOITATION")
    m = monnaie.objects.all()
    context = {
        'pro': p,
        'unite':u,
        'monnaie':m
    }
    
    return render(request,'edit_proposition_exploitation.html',context)

#MODIFICATION emission fonctionnement 
 
def update_exploitation_proposition(request):
    current_year=request.session['annee']
    u=unite_1.objects.get(id=request.session['unite'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="proposition")
    cloture=request.POST.getlist('cloture')
    prevision=request.POST.getlist('prevision')
    rubrique=request.POST.getlist('rubrique')
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_modif=datetime.now()

    for i in range(len(cloture)) :
       p=proposition.objects.get(type='depenses',type1="EXPLOITATION",pv=pv,rubrique=rubrique[i])
       p.cloture=cloture[i]
       p.prevision=prevision[i]
       p.regler_par=regler[i]
       p.commentaire=commentaire[i]
       p.monnie=monnaie[i]
       
       p.save()
    
    
    h = historique(annee=pv.annee,type="proposition",type_1="EXPLOITATION",user=name,date_h=date_modif)
    h.save()
    

    return redirect('proposition_depense')


#3eme principale de proposition

def proposition_budgetaire(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
    
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
   
    u = unite_1.objects.get(pk=request.session["unite"])
   
    trafic = False
    recette = False
    emission = False
    depenses = False
    ep = entete_pv.objects.filter(unite=u,annee=request.session["annee"],type="proposition")
    if (not ep.exists()):
        ep = entete_pv.objects.get(unite=u,annee=request.session["annee"],type="proposition")
    

    ep = entete_pv.objects.get(unite=u,annee=request.session["annee"],type="proposition")
   
    p1 = proposition.objects.filter(pv=ep,type="trafic")
    p2 = proposition.objects.filter(pv=ep,type="recette")
    p3 = proposition.objects.filter(pv=ep,type="emission")
    p4 = proposition.objects.filter(pv=ep,type="depenses",type1='FONCTIONNEMENT')
    p5 = proposition.objects.filter(pv=ep,type="depenses",type1='EXPLOITATION')
    request.session["pv"]=ep.id


    if p1.exists():
        trafic = True
    if p2.exists():
       recette = True 
    if p3.exists():
        emission = True
    if(p4.exists() & p5.exists()):
        depenses= True
    if trafic == True and recette == True and emission == True and depenses == True :
        ep.rempli = True
        ep.save()

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

    context = {
        "user": name,

        "poste":poste,
        "unite":u,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "depense":depenses,

     }   

    return render(request,'proposition_budgetaire.html' , context)

###proposition_trafic
def proposition_trafic(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="trafic")

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

    context = {
        "user": name,
        "poste":poste,
        "unite":u,
       
        "compte":com,
       
        
     }   

    return render(request, "proposition_trafic.html", context   )
#cette fonction recupere les valeurs de formulaires TRAFIC
def test(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    commentaire = request.POST.getlist('commentaire')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_ajout=datetime.now()

    pv = entete_pv.objects.get(id=request.session["pv"])
    for c in range(len(compt)):
        p = proposition(type="trafic",pv=pv,rubrique=compt[c],cloture=compt2[c],prevision=compt3[c],rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        p.save()

    h = historique(annee=pv.annee,type="proposition",type_1="trafic",user=name,date_h=date_ajout)
    h.save()
    
    return redirect('proposition_budgetaire')

###proposition_recette

def proposition_recette(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="recette")
    
    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

    context = {
        "user": name,
        "poste": poste,
        "unite":u,
       
        "compte":com,
       
        
     }   

    return render(request, "proposition_recette.html", context   )

#cette fonction recupere les valeurs de formulaires RECETTE

def test1(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    commentaire = request.POST.getlist('commentaire')

    u = unite_1.objects.get(pk=request.session["unite"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_ajout=datetime.now()

    pv = entete_pv.objects.get(id=request.session["pv"])
    for c in range(len(compt)):
        p = proposition(type="recette",pv=pv,rubrique=compt[c],cloture=compt2[c],prevision=compt3[c],rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        p.save()

    
    h = historique(annee=pv.annee,type="proposition",type_1="recette",user=name,date_h=date_ajout)
    h.save()
    return redirect('proposition_budgetaire')

###proposition_emission

def proposition_emission(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="emission")


    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste": poste,
        "unite":u,
        "compte":com,
       
        
     }   

    return render(request, "proposition_emission.html", context   )

#cette fonction recupere les valeurs de formulaires EMISSION

def test2(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    commentaire = request.POST.getlist('commentaire')
    u = unite_1.objects.get(pk=request.session["unite"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_ajout=datetime.now()

    pv = entete_pv.objects.get(id=request.session["pv"])
    for c in range(len(compt)):
        p = proposition(type="emission",pv=pv,rubrique=compt[c],cloture=compt2[c],prevision=compt3[c],rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        p.save()
    
    h = historique(annee=pv.annee,type="proposition",type_1="emission",user=name,date_h=date_ajout)
    h.save()
    return redirect('proposition_budgetaire')



###proposition_depense

def proposition_depense(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    ep = entete_pv.objects.get(unite=u,annee=request.session["annee"],type="proposition")
    p = proposition.objects.filter(pv=ep,type="depenses",type1="FONCTIONNEMENT")
    print(p)
    print("iciiiiiiiiiiiiiiiiiiiiiiiiii")
    p2 = proposition.objects.filter(pv=ep,type1="EXPLOITATION")
    fonct = False
    expl = False
    if p.exists():
        fonct = True
    if p2.exists():
        expl = True
    context = {
       "unite":u,
       "fonct":fonct,
       "expl":expl
     }   

    return render(request, "proposition_depense.html", context   )
########################
def proposition_fonctionnement1(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite"])
    print(u)
    com = unite_pos6.objects.filter(unite=u,type="FONCTIONNEMENT")
    print(com)
    m = monnaie.objects.all()

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
#### hiba : add account form #####
    form= form_unite_pos_fonctionnement
    form1 = form_unite_pos_fonctionnement(request.POST)
    if form1.is_valid():
        u1 = unite_pos6()
        u1.unite=u  
        u1.pos6=Pos6.objects.get(scf=form1.cleaned_data["compte"].scf)  
        print(Pos6.objects.get(scf=form1.cleaned_data["compte"].scf))

        u1.type='FONCTIONNEMENT'   
        u1.added_by=p.type_user       
        u1.save()
        com = unite_pos6.objects.filter(unite=u,type="FONCTIONNEMENT")
        return redirect("proposition_fonctionnement1")
    

    context = {
        "user": name,
        "poste": poste,
        "unite":u,  
        "compte":com,
        'monnaie':m,
        'form': form
       
        
     }   

    return render(request, "proposition_fonctionnement.html", context   )

 ### hiba : delete unite_pos ####  
def delete_unite_pos_fct(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    
    id = request.POST.get("id")
    u = unite_pos6.objects.get(id=id)
    u.delete()    
    return redirect ('proposition_fonctionnement')


####1111
def proposition_exploitation1(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite"])
    print(u)
    print(request.session["unite"])
    com = unite_pos6.objects.filter(unite=request.session["unite"],type="EXEPLOITATION")
    print(com)
    print("mussssssssssss")
    m = monnaie.objects.all()


    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste": poste,
        "unite":u,  
        "compte":com,
        'monnaie':m
       
        
     }   

    return render(request, "proposition_exploitation.html", context   )

#cette fonction recupere les valeurs de formulaires DEPENSES

def test3(request):
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    type = request.POST.getlist('type')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    u = unite_1.objects.get(pk=request.session["unite"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + '' + str(p.prenom_user)
    date_ajout=datetime.now()


    pv = entete_pv.objects.get(unite=unite_1.objects.get(id=request.session["unite"]),annee=request.session["annee"],type="proposition")

    for c in range(len(scf)):
            p = proposition(scf=scf[c],type1=type[c],type="depenses",pv=pv,rubrique=rubrique[c],cloture=compt2[c],prevision=compt3[c],regler_par=regler[c],monnie=monnaie[c],commentaire=commentaire[c],rempli=True)
            p.save()
    
    h = historique(annee=pv.annee,type="proposition",type_1=type[0],user=name,date_h=date_ajout)
    h.save()
    return redirect('proposition_depense')




###consultation des propositions budget

def massivn(request):
    request.session["unite"]=request.POST.get("id")
    return redirect("consultation_proposition")


def massivn1(request):
    request.session["unite"]=request.POST.get("id")
    return redirect("pre_proposition_budgetaire")


def consultation_proposition(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
       
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite"])
    
    print(u)
    pro = entete_pv.objects.filter(type="proposition")

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste": poste,
        "pv":pro 
        
     }   

    return render(request, "consultation_proposition.html", context   )



###consultation des propositions budget - pv proposition
def intermed_pv_proposition(request):
    request.session["annee3"]=int(request.POST.get("annee"))
    return redirect("pv_proposition")


def pv_proposition(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(pk=request.session["unite"])
    pv = entete_pv.objects.get(annee=request.session["annee3"],unite=u,type="proposition")
    pro = proposition.objects.filter(type="trafic",pv=pv)
    usert_max=""
    usert_min=""
    dusert_max=""
    dusert_min=""

    userr_max=""
    userr_min=""
    duserr_max=""
    duserr_min=""

    usere_max=""
    usere_min=""
    dusere_max=""
    dusere_min=""

    userf_max=""
    userf_min=""
    duserf_max=""
    duserf_min=""

    userx_max=""
    userx_min=""
    duserx_max=""
    duserx_min=""
    trafic= False
    recette=False
    emission=False
    fonct=False
    expl=False

    if pro.exists():
        trafic=True
        print(get_max_historique(request.session["annee3"],'proposition','trafic'))
        usert_max=get_max_historique(request.session["annee3"],'proposition','trafic').user
        usert_min=get_min_historique(request.session["annee3"],'proposition','trafic').user
        dusert_max=get_max_historique(request.session["annee3"],'proposition','trafic').date_h
        dusert_min=get_min_historique(request.session["annee3"],'proposition','trafic').date_h
    


    pro1 = proposition.objects.filter(type="recette",pv=pv)
    if pro1.exists():
        recette=True

        userr_max=get_max_historique(request.session["annee3"],'proposition','recette').user
        userr_min=get_min_historique(request.session["annee3"],'proposition','recette').user
        duserr_max=get_max_historique(request.session["annee3"],'proposition','recette').date_h
        duserr_min=get_min_historique(request.session["annee3"],'proposition','recette').date_h

    
    pro2 = proposition.objects.filter(type="emission",pv=pv)
    if pro2.exists():
        emission= True
        usere_max=get_max_historique(request.session["annee3"],'proposition','emission').user
        usere_min=get_min_historique(request.session["annee3"],'proposition','emission').user
        dusere_max=get_max_historique(request.session["annee3"],'proposition','emission').date_h
        dusere_min=get_min_historique(request.session["annee3"],'proposition','emission').date_h

    


    pro3 = proposition.objects.filter(type1="FONCTIONNEMENT",pv=pv)
    if pro3.exists():
        fonct=True

        userf_max=get_max_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').user
        userf_min=get_min_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').user
        duserf_max=get_max_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').date_h
        duserf_min=get_min_historique(request.session["annee3"],'proposition','FONCTIONNEMENT').date_h

    pro4 = proposition.objects.filter(type1="EXPLOITATION",pv=pv)
    if pro4.exists():
        expl=True
        userx_max=get_max_historique(request.session["annee3"],'proposition','EXPLOITATION').user
        userx_min=get_min_historique(request.session["annee3"],'proposition','EXPLOITATION').user
        duserx_max=get_max_historique(request.session["annee3"],'proposition','EXPLOITATION').date_h
        duserx_min=get_min_historique(request.session["annee3"],'proposition','EXPLOITATION').date_h



    name = str(p.nom_user) + '     ' + str(p.prenom_user)
  
    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    
    context = {
        
       "user": name,
       "poste": poste,
       "pro":pro,
       "pro1":pro1,
       "pro2":pro2,
       "pro3":pro3,
       "pro4":pro4,

       "unite":u,
        "usert_max": usert_max,
        "usert_min": usert_min,
        "dusert_max": dusert_max,
        "dusert_min": dusert_min,
        
       "userr_max": userr_max,
        "userr_min": userr_min,
        "duserr_max": duserr_max,
        "duserr_min": duserr_min,
        

        "usere_max": usere_max,
        "usere_min": usere_min,
        "dusere_max": dusere_max,
        "dusere_min": dusere_min,
        
        
       "userf_max": userf_max,
        "userf_min": userf_min,
        "duserf_max": duserf_max,
        "duserf_min": duserf_min,

        "userx_max": userx_max,
        "userx_min": userx_min,
        "duserx_max": duserx_max,
        "duserx_min": duserx_min,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "fonct":fonct,
        "expl":expl
        


        

        
     }   

    return render(request, "pv_proposition.html", context   )

#############################################################################################################################################
    #page principale de reunion
def pre_pre_reunion_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)


    up = unite_profile.objects.filter(pro=p)
    date_reu=int(datetime.now().year)+1

    r = reunion_bud.objects.filter(annee=date_reu)
    # if (not r.exists()):
    #     r=reunion_bud

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste": poste,
        'unite':up,
        "r":r
    }
    return render(request,'pre_pre_reunion_budgetaire.html',context)

#2eme principale de reunion

def musvn(request):
    request.session['unite']=request.POST.get('id')
    return redirect("reunion_budgetaire")


def reunion_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    u= unite_1.objects.get(id=request.session['unite'])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_reu=int(datetime.now().year)
    e = entete_pv.objects.filter(annee=date_reu+1,unite=u,type="reunion")
    if not e.exists():
        e = entete_pv(annee=date_reu+1,unite=u,type="reunion")
        e.save()

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"


    context = {
        "user": name,
        "poste": poste,
       'unite':u
    }
    return render(request,'reunion_budgetaire.html',context)



# cette fonction retourne la somme des mois de controle budgetaire d une seul annee
def get_montant(query):
    montant = 0
    for c in query:
        montant = montant + c.montant
    return montant
# cette fonction retourne le dernier mois de l'annee de controle budgetaire
def get_mois(query):
    if len(query) == 0:
        return "rien"
    else:
        return query[len(query)-1].mois


#cette fonction return le montant du compte par rapport du scf annee type#

def get_realisaion(type,annee,rubrique,unite):
    pv = entete_pv.objects.filter(unite=unite_1.objects.get(pk=unite),annee=annee,type="realisation")
    if pv.exists():
        pv = entete_pv.objects.get(unite=unite_1.objects.get(pk=unite),annee=annee,type="realisation")

        r = realisation2.objects.filter(pv=pv,type=type,rubrique=rubrique)
        if r.exists():
            r = realisation2.objects.get(pv=pv,type=type,rubrique=rubrique)
            return r.realisation
        else:
            return 0
    else:
        return 0

#reunion_trafic
def reunion_trafic(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
    notifications = get_notifications(p)
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)

    date_reu= int(datetime.now().year)
    condition1=False
    condition2=False
    er = entete_pv.objects.get(type="reunion",unite=u,annee=date_act+1)

    if date_act == date_reu:
        pvv = entete_pv.objects.filter(unite=u,annee=date_act+1,type="proposition")

        if pvv.exists():
            pv = entete_pv.objects.get(unite=u,annee=date_act+1,type="proposition")
            pro = proposition.objects.filter(pv=pv,type="trafic")
            if pro.exists():
                condition1=True

        ecc = entete_pv.objects.filter(type="controle",unite=u,annee=date_act)
        if ecc.exists():
            ec = entete_pv.objects.get(type="controle",unite=u,annee=date_act)
            controle = controle_bud.objects.filter(ec=ec,type="trafic")
            if controle.exists():
                condition2=True
       
        if (condition1 == False) and (condition2 == False):

            # r = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act)
            r = Pos6.objects.filter(type="trafic") 
            r2 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)
        r2 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)
        if p.type_user == "cadre_bud":
            poste = 'Cadre Budgétaire'
        if p.type_user == "cdd":
            poste = "Chef de département"   
        if p.type_user == "sd":
            poste = "Sous-directeur"
            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p,
                "notifications":notifications
                         }
            else: 

                for re in r :
                    
                    r1 = reunion_bud(mois_controle="Rien",controle_budgetaire=0,pv=er,type="trafic",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("trafic",date_act-1,re.lib,u.id),realisation_2=get_realisaion("trafic",date_act-2,re.lib,u.id))
                    r1.save()
                

                r2 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)


                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p,
                    "notifications":notifications

                    
                }   
            return render(request,'reunion_trafic.html',context)
        
        elif (condition1 == False) and (condition2 == True) :

            r = Pos6.objects.filter(type="trafic") 
            r2 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)

            if r2.exists():
                 context = {
                "user": name,
                "poste":poste,
                "unite":u,
                "compte":r2,
                "profile":p,
                "notifications":notifications

                
                         }
            else: 
                for re in r :
                    
                     r1 = reunion_bud(controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),
                     mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),pv=er,
                     type="trafic",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("trafic",date_act-1,re.lib,u.id),realisation_2=get_realisaion("trafic",date_act-2,re.lib,u.id))
                     r1.save()
                
                r2 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)
                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p,
                    "notifications":notifications

                    
                }   
            return render(request,'reunion_trafic.html',context)
        
        else:
            
            r = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)        
            if r.exists():
                print("2")
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r,
                    "unite":u,
                    "profile":p,
                    "notifications":notifications

                }
            
                return render(request,'reunion_trafic.html',context)
            else:

                if ecc.exists():
                    for pros in pro:
                        res = reunion_bud(pv=er,type="trafic",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),realisation_1=get_realisaion("trafic",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("trafic",date_act-2,pros.rubrique,u.id))
                        res.save()
                else:    
                    for pros in pro:
                        res = reunion_bud(pv=er,type="trafic",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=0,cloture=pros.cloture,prevision=pros.prevision,mois_controle="rien",realisation_1=get_realisaion("trafic",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("trafic",date_act-2,pros.rubrique,u.id))
                        res.save()
                r1 = reunion_bud.objects.filter(pv=er,type="trafic",annee=date_act+1)
                print(r1)
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r1,
                    "etat":1,
                    "unite":u,
                    "profile":p,
                    "notifications":notifications

                    
                }
            
                return render(request,'reunion_trafic.html',context)
    
def verifier_trafic(request):
    p = profile.objects.get(user=request.user)
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True

    

    print(request.POST.get("compte2"))
    print(request.POST.get("compte3"))
    print("mussssssssssssssssss")
    r.cloture = request.POST.get("compte2")
    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()
    ## add notification 
    create_notif(r.pv,p)
    #### hna notifie
    date_act = int(datetime.now().year)+1
    u = unite_1.objects.get(pk=request.session["unite"])
    e1 = entete_pv.objects.filter(type="notifie",unite=u,annee=date_act)
    
    if e1.exists():
        e=entete_pv.objects.get(type="notifie",unite=u,annee=date_act)
        n1 = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="trafic",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    else:
        e = entete_pv(type="notifie",unite=u,annee=date_act)
        e.save()
        n1 = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="trafic",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    return redirect('reunion_trafic')

############### reunion
def add_trafic_reunion(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    for c in range(len(compt)):
        r = reunion_bud(type="trafic",cloture=compt2[c],prevision=compt3[c])
        r.save()
    return redirect('reunion_budgetaire')

############### reunion
def creer_trafic_reunion(request):
    p = profile.objects.get(user=request.user)
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    for c in range(len(compt)):
        r = reunion_bud(type="trafic",annee=r.annee+2,cloture=compt2[c],prevision=compt3[c])
        r.save()
    return redirect('reunion_budgetaire')


def islam(request):
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    r.is_valide = False
    p = profile.objects.get(user=request.user)

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False

   


    r.save()
    return redirect('reunion_trafic')

################################
#  condition1=False
#  condition2=False

#  if date_act == date_reu:

#         if pv.exists():
#               pro = proposition.objects.filter(pv=pv,type="recette")
#               if pro.exists():
#                    condition1=True
#         ec = entete_controle.objects.get(unite=u,annee=date_act)
#         if ec.exists():
#               controle = controle_bud.objects.filter(ec=ec,type="recette")
#               if controle.exists():
#                   condition2=True




#############solution################3

#reunion_recette
def reunion_recette(request):

    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)

    date_reu=int(datetime.now().year)
    condition1=False
    condition2=False
    er = entete_pv.objects.get(type="reunion",unite=u,annee=date_act+1)

    if date_act == date_reu:
        pvv = entete_pv.objects.filter(unite=u,annee=date_act+1,type="proposition")

        if pvv.exists():
            pv = entete_pv.objects.get(unite=u,annee=date_act+1,type="proposition")
            pro = proposition.objects.filter(pv=pv,type="recette")
            if pro.exists():
                condition1=True

        ecc = entete_pv.objects.filter(type="controle",unite=u,annee=date_act)
        if ecc.exists():
            ec = entete_pv.objects.get(type="controle",unite=u,annee=date_act)
            controle = controle_bud.objects.filter(ec=ec,type="recette")
            if controle.exists():
                condition2=True
       
        if (condition1 == False) and (condition2 == False):

            # r = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act)
            r = Pos6.objects.filter(type="recette") 
            r2 = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)

            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"
            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p
                
                         }
            else: 

                for re in r :
                    
                    r1 = reunion_bud(mois_controle="Rien",controle_budgetaire=0,pv=er,type="recette",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("recette",date_act-1,re.lib,u.id),realisation_2=get_realisaion("recette",date_act-2,re.lib,u.id))
                    r1.save()
                

                r2 = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)


                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_recette.html',context)
        
        elif (condition1 == False) and (condition2 == True) :

            r = Pos6.objects.filter(type="recette") 
            r2 = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)

            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"

            if r2.exists():
                 context = {
                "user": name,
                "poste":poste,
                "unite":u,
                "compte":r2,
                "profile":p

                
                         }
            else: 
                for re in r :
                    
                     r1 = reunion_bud(controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),
                     mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),pv=er,
                     type="recette",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("recette",date_act-1,re.lib,u.id),realisation_2=get_realisaion("recette",date_act-2,re.lib,u.id))
                     r1.save()
                
                r2 = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)

                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_recette.html',context)
        
        else:
            
            r = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)   
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"    
            if r.exists():
                print("2")
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r,
                    "unite":u,
                    "profile":p

                }
            
                return render(request,'reunion_recette.html',context)
            else:

                if not ecc.exists():
                    for pros in pro:
                        res = reunion_bud(pv=er,type="recette",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle="rien",realisation_1=get_realisaion("recette",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("recette",date_act-2,pros.rubrique,u.id))
                        res.save()

  
                else:    

                    for pros in pro:
                        res = reunion_bud(pv=er,type="recette",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),realisation_1=get_realisaion("recette",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("recette",date_act-2,pros.rubrique,u.id))
                        res.save()
                r1 = reunion_bud.objects.filter(pv=er,type="recette",annee=date_act+1)
                print(r1)
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r1,
                    "etat":1,
                    "unite":u,
                    "profile":p

                    
                }
            
                return render(request,'reunion_recette.html',context)
    

def verifier_recette(request):
    p = profile.objects.get(user=request.user)
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True

    


    r.cloture = request.POST.get("compte2")
    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()
    #### hna notifie
    date_act = int(datetime.now().year)+1
    u = unite_1.objects.get(pk=request.session["unite"])
    e1 = entete_pv.objects.filter(type="notifie",unite=u,annee=date_act)
    
    if e1.exists():
        e=entete_pv.objects.get(type="notifie",unite=u,annee=date_act)
        n1 = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="recette",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    else:
        e = entete_pv(type="notifie",unite=u,annee=date_act)
        e.save()
        n1 = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="recette",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    return redirect('reunion_recette')

def mus(request):
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    r.is_valide = False
    p = profile.objects.get(user=request.user)

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False

   


    r.save()
    return redirect('reunion_recette')


#reunion_emission
def reunion_emission(request):

  
    
    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)

    date_reu=int(datetime.now().year)
    condition1=False
    condition2=False
    er = entete_pv.objects.get(type="reunion",unite=u,annee=date_act+1)

    if date_act == date_reu:
        pvv = entete_pv.objects.filter(unite=u,annee=date_act+1,type="proposition")

        if pvv.exists():
            pv = entete_pv.objects.get(unite=u,annee=date_act+1,type="proposition")
            pro = proposition.objects.filter(pv=pv,type="emission")
            if pro.exists():
                condition1=True

        ecc = entete_pv.objects.filter(type="controle",unite=u,annee=date_act)
        if ecc.exists():
            ec = entete_pv.objects.get(type="controle",unite=u,annee=date_act)
            controle = controle_bud.objects.filter(ec=ec,type="emission")
            if controle.exists():
                condition2=True
       
        if (condition1 == False) and (condition2 == False):

            # r = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act)
            r = Pos6.objects.filter(type="emission") 
            r2 = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"
            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p
                
                         }
            else: 

                for re in r :
                    
                    r1 = reunion_bud(mois_controle="Rien",controle_budgetaire=0,pv=er,type="emission",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("emission",date_act-1,re.lib,u.id),realisation_2=get_realisaion("emission",date_act-2,re.lib,u.id))
                    r1.save()
                

                r2 = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)


                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_emission.html',context)
        
        elif (condition1 == False) and (condition2 == True) :

            r = Pos6.objects.filter(type="emission") 
            r2 = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"
            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p

                
                         }
            else: 
                for re in r :
                    
                     r1 = reunion_bud(controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),
                     mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=re.lib)),pv=er,
                     type="emission",annee=date_act+1,proposition=re.lib,cloture=0,prevision=0,realisation_1=get_realisaion("emission",date_act-1,re.lib,u.id),realisation_2=get_realisaion("emission",date_act-2,re.lib,u.id))
                     r1.save()
                
                r2 = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)
                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_emission.html',context)
        
        else:
            
            r = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)    
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"    
            if r.exists():
                print("2")
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r,
                    "unite":u,
                    "profile":p

                }
            
                return render(request,'reunion_emission.html',context)
            else:
                if not ecc.exists():
                    for pros in pro:
                        res = reunion_bud(pv=er,type="emission",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle="rien",realisation_1=get_realisaion("emission",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("emission",date_act-2,pros.rubrique,u.id))
                        res.save()
                else:    
                    for pros in pro:
                        res = reunion_bud(pv=er,type="emission",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),realisation_1=get_realisaion("emission",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("emission",date_act-2,pros.rubrique,u.id))
                        res.save()
                r1 = reunion_bud.objects.filter(pv=er,type="emission",annee=date_act+1)
                print(r1)
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r1,
                    "etat":1,
                    "unite":u,
                    "profile":p

                    
                }
            
                return render(request,'reunion_emission.html',context)
    

def verifier_emission(request):
    p = profile.objects.get(user=request.user)
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True

    


    r.cloture = request.POST.get("compte2")
    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()
    #### hna notifie
    date_act = int(datetime.now().year)+1
    u = unite_1.objects.get(pk=request.session["unite"])
    e1 = entete_pv.objects.filter(type="notifie",unite=u,annee=date_act)
    
    if e1.exists():
        e=entete_pv.objects.get(type="notifie",unite=u,annee=date_act)
        n1 = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="emission",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    else:
        e = entete_pv(type="notifie",unite=u,annee=date_act)
        e.save()
        n1 = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="emission",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    return redirect('reunion_emission')

def massi(request):
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    r.is_valide = False
    p = profile.objects.get(user=request.user)

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False

   


    r.save()
    return redirect('reunion_emission')











#reunion_depenses
def reunion_depenses1(request):
   
   
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)

    date_reu=int(datetime.now().year)
    condition1=False
    condition2=False
    er = entete_pv.objects.get(type="reunion",unite=u,annee=date_act+1)

    if date_act == date_reu:
        pvv = entete_pv.objects.filter(unite=u,annee=date_act+1,type="proposition")

        if pvv.exists():
            pv = entete_pv.objects.get(unite=u,annee=date_act+1,type="proposition")
            pro = proposition.objects.filter(pv=pv,type="depenses")
            if pro.exists():
                condition1=True

        ecc = entete_pv.objects.filter(type="controle",unite=u,annee=date_act)
        if ecc.exists():
            ec = entete_pv.objects.get(type="controle",unite=u,annee=date_act)
            controle = controle_bud.objects.filter(ec=ec,type="depenses")
            if controle.exists():
                condition2=True
       
        if (condition1 == False) and (condition2 == False):

            # r = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act)
            r = unite_pos6.objects.filter(unite=u) 
            for i in r:
                if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                    r = r.exclude(id=i.id)


            print(r)
            r2 = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"

            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p
                
                         }
            else: 

                for re in r :
                    
                    r1 = reunion_bud(mois_controle="Rien",controle_budgetaire=0,pv=er,type="depenses",annee=date_act+1,proposition=re.pos6.lib,cloture=0,prevision=0,realisation_1=get_realisaion("depenses",date_act-1,re.pos6.lib,u.id),realisation_2=get_realisaion("depenses",date_act-2,re.pos6.lib,u.id))
                    r1.save()
                

                r2 = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)


                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_depenses.html',context)
        
        elif (condition1 == False) and (condition2 == True) :

            r = unite_pos6.objects.filter(unite=u) 
            for i in r:
                if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                    r = r.exclude(id=i.id)

            r2 = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"
            if r2.exists():
                 context = {
                "user": name,
                "poste": poste,
                "unite":u,
                "compte":r2,
                "profile":p

                
                         }
            else: 
                for re in r :
                    
                     r1 = reunion_bud(controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=re.pos6.lib)),
                     mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=re.pos6.lib)),pv=er,
                     type="depenses",annee=date_act+1,proposition=re.pos6.lib,cloture=0,prevision=0,realisation_1=get_realisaion("depenses",date_act-1,re.pos6.lib,u.id),realisation_2=get_realisaion("depenses",date_act-2,re.pos6.lib,u.id))
                     r1.save()
                
                r2 = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)
                context = {
                    "user": name,
                    "poste": poste,
                    "unite":u,
                    "compte":r2,
                    "profile":p

                    
                }   
            return render(request,'reunion_depenses.html',context)
        
        else:
            
            r = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)       
            
            if p.type_user == "cadre_bud":
                poste = 'Cadre Budgétaire'
            if p.type_user == "cdd":
                poste = "Chef de département"   
            if p.type_user == "sd":
                poste = "Sous-directeur"
                 
            if r.exists():
                print("2")
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r,
                    "unite":u,
                    "profile":p

                }
            
                return render(request,'reunion_depenses.html',context)
            else:
                if not ecc.exists():
                    for pros in pro:
                        res = reunion_bud(pv=er,type="depenses",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle="rien",realisation_1=get_realisaion("depenses",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("depenses",date_act-2,pros.rubrique,u.id))
                        res.save()
                else:    
                    for pros in pro:
                        res = reunion_bud(pv=er,type="depenses",annee=date_act+1,proposition=pros.rubrique,controle_budgetaire=get_montant(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),cloture=pros.cloture,prevision=pros.prevision,mois_controle=get_mois(controle_bud.objects.filter(ec=ec,rubrique=pros.rubrique)),realisation_1=get_realisaion("depenses",date_act-1,pros.rubrique,u.id),realisation_2=get_realisaion("depenses",date_act-2,pros.rubrique,u.id))
                        res.save()
                r1 = reunion_bud.objects.filter(pv=er,type="depenses",annee=date_act+1)
                print(r1)
                context = {
                    "user": name,
                    "poste": poste,
                    "compte":r1,
                    "etat":1,
                    "unite":u,
                    "profile":p

                    
                }
            
                return render(request,'reunion_depenses.html',context)
    

def verifier_depenses(request):
    p = profile.objects.get(user=request.user)
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True

    


    r.cloture = request.POST.get("compte2")
    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()
    #### hna notifie
    date_act = int(datetime.now().year)+1
    u = unite_1.objects.get(pk=request.session["unite"])
    e1 = entete_pv.objects.filter(type="notifie",unite=u,annee=date_act)
    
    if e1.exists():
        e=entete_pv.objects.get(type="notifie",unite=u,annee=date_act)
        n1 = notifie_bud.objects.filter(pv=e,type="depenses",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="depenses",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="depenses",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    else:
        e = entete_pv(type="notifie",unite=u,annee=date_act)
        e.save()
        n1 = notifie_bud.objects.filter(pv=e,type="depenses",rubrique=r.proposition,annee=date_act)
        if n1.exists():
            n1 = notifie_bud.objects.get(pv=e,type="depenses",rubrique=r.proposition,annee=date_act)
            # n1.prevision = r.prevision 
            # n1.save()
        else:
            n=notifie_bud(pv=e,type="depenses",rubrique=r.proposition,prevision=r.prevision,annee=date_act)
            n.save()

    return redirect('reunion_depenses')

def ania(request):
    r = reunion_bud.objects.get(pk = request.POST.get("id"))
    r.is_valide = False
    p = profile.objects.get(user=request.user)

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False

   


    r.save()
    return redirect('reunion_depenses')




###########################################################################################################
    #page principale de controle budgetaire
def pre_pre_controle_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    # u = unite_1.objects.filter(pro=p)
    up = unite_profile.objects.filter(pro=p)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    context = {
        "user": name,
        "poste": poste,
        'unite':up
    }
    return render(request,'pre_pre_controle_budgetaire.html',context)




 #l'annee de controle budgetaire
def pre_controle_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    up = unite_profile.objects.filter(pro=p)
    # u = unite_1.objects.filter(pro=p)
    request.session['unite']=request.POST.get('id')
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
   
    context = {
        "user": name,
        "poste": poste,
        'unite':up,
        'form':form_controle

    }
    return render(request,'pre_controle_budgetaire.html',context)

###fonction qui garde l'annee de controle budgetaire
def add_control(request):
    
    form = form_budget(request.POST)
    if form.is_valid():
        u = unite_1.objects.get(pk=request.session["unite"])
        request.session["annee"]= form.cleaned_data["annee"]
        p =  entete_pv.objects.filter(type="controle",unite=u,annee=form.cleaned_data["annee"])
        if p.exists():
            ec = entete_pv.objects.get(type="controle",unite=u,annee=form.cleaned_data["annee"])
            request.session["ec"]=ec.id
            return redirect('controle_budgetaire')
        else:
            print(u.id)
            ec = entete_pv(type="controle",unite=u,annee=form.cleaned_data["annee"])
            ec.save()
            request.session["ec"]=ec.id
            return redirect('controle_budgetaire')
    return redirect('controle_budgetaire')

#principale de controle budgetaire

def controle_budgetaire(request):

    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
    
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    u = unite_1.objects.get(pk=request.session["unite"])
    trafic = False
    recette = False
    emission = False

    tjanvier =False
    tfevrier =False
    tmars=False
    tavril=False
    tmai =False
    tjuin=False
    tjuillet=False
    taout=False
    tseptembre=False
    toctobre=False
    tnovembre=False
    tdecembre=False
    #############
    rjanvier =False
    rfevrier =False
    rmars=False
    ravril=False
    rmai =False
    rjuin=False
    rjuillet=False
    raout=False
    rseptembre=False
    roctobre=False
    rnovembre=False
    rdecembre=False
    ############
    ejanvier =False
    efevrier =False
    emars=False
    eavril=False
    emai =False
    ejuin=False
    ejuillet=False
    eaout=False
    eseptembre=False
    eoctobre=False
    enovembre=False
    edecembre=False
    ##############
    fjanvier =False
    ffevrier =False
    fmars=False
    favril=False
    fmai =False
    fjuin=False
    fjuillet=False
    faout=False
    fseptembre=False
    foctobre=False
    fnovembre=False
    fdecembre=False
     ##############
    xjanvier =False
    xfevrier =False
    xmars=False
    xavril=False
    xmai =False
    xjuin=False
    xjuillet=False
    xaout=False
    xseptembre=False
    xoctobre=False
    xnovembre=False
    xdecembre=False


   
    ec = entete_pv.objects.get(type="controle",unite=u,annee=request.session["annee"])
    c1 = controle_bud.objects.filter(ec=ec,type="trafic")
    c2 = controle_bud.objects.filter(ec=ec,type="recette")
    c3 = controle_bud.objects.filter(ec=ec,type="emission")
    if c1.exists():
        trafic=True
    if c2.exists():
        recette=True
    if c3.exists():
        emission=True
    t1=controle_bud.objects.filter(ec=ec,type="trafic",mois="janvier")
    t2=controle_bud.objects.filter(ec=ec,type="trafic",mois="fevrier")
    t3=controle_bud.objects.filter(ec=ec,type="trafic",mois="mars")
    t4=controle_bud.objects.filter(ec=ec,type="trafic",mois="avril")
    t5=controle_bud.objects.filter(ec=ec,type="trafic",mois="mai")
    t6=controle_bud.objects.filter(ec=ec,type="trafic",mois="juin")
    t7=controle_bud.objects.filter(ec=ec,type="trafic",mois="juillet")
    t8=controle_bud.objects.filter(ec=ec,type="trafic",mois="aout")
    t9=controle_bud.objects.filter(ec=ec,type="trafic",mois="septembre")
    t10=controle_bud.objects.filter(ec=ec,type="trafic",mois="octobre")
    t11=controle_bud.objects.filter(ec=ec,type="trafic",mois="novembre")
    t12=controle_bud.objects.filter(ec=ec,type="trafic",mois="decembre")

    ############
    r1=controle_bud.objects.filter(ec=ec,type="recette",mois="janvier")
    r2=controle_bud.objects.filter(ec=ec,type="recette",mois="fevrier")
    r3=controle_bud.objects.filter(ec=ec,type="recette",mois="mars")
    r4=controle_bud.objects.filter(ec=ec,type="recette",mois="avril")
    r5=controle_bud.objects.filter(ec=ec,type="recette",mois="mai")
    r6=controle_bud.objects.filter(ec=ec,type="recette",mois="juin")
    r7=controle_bud.objects.filter(ec=ec,type="recette",mois="juillet")
    r8=controle_bud.objects.filter(ec=ec,type="recette",mois="aout")
    r9=controle_bud.objects.filter(ec=ec,type="recette",mois="septembre")
    r10=controle_bud.objects.filter(ec=ec,type="recette",mois="octobre")
    r11=controle_bud.objects.filter(ec=ec,type="recette",mois="novembre")
    r12=controle_bud.objects.filter(ec=ec,type="recette",mois="decembre")
    ############
    e1=controle_bud.objects.filter(ec=ec,type="emission",mois="janvier")
    e2=controle_bud.objects.filter(ec=ec,type="emission",mois="fevrier")
    e3=controle_bud.objects.filter(ec=ec,type="emission",mois="mars")
    e4=controle_bud.objects.filter(ec=ec,type="emission",mois="avril")
    e5=controle_bud.objects.filter(ec=ec,type="emission",mois="mai")
    e6=controle_bud.objects.filter(ec=ec,type="emission",mois="juin")
    e7=controle_bud.objects.filter(ec=ec,type="emission",mois="juillet")
    e8=controle_bud.objects.filter(ec=ec,type="emission",mois="aout")
    e9=controle_bud.objects.filter(ec=ec,type="emission",mois="septembre")
    e10=controle_bud.objects.filter(ec=ec,type="emission",mois="octobre")
    e11=controle_bud.objects.filter(ec=ec,type="emission",mois="novembre")
    e12=controle_bud.objects.filter(ec=ec,type="emission",mois="decembre")
     ############
    f1=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="janvier")
    f2=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="fevrier")
    f3=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="mars")
    f4=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="avril")
    f5=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="mai")
    f6=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="juin")
    f7=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="juillet")
    f8=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="aout")
    f9=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="septembre")
    f10=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="octobre")
    f11=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="novembre")
    f12=controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT",mois="decembre")

 ############
    x1=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="janvier")
    x2=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="fevrier")
    x3=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="mars")
    x4=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="avril")
    x5=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="mai")
    x6=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="juin")
    x7=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="juillet")
    x8=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="aout")
    x9=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="septembre")
    x10=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="octobre")
    x11=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="novembre")
    x12=controle_bud.objects.filter(ec=ec,type1="EXPLOITATION",mois="decembre")

    if t1.exists():
        tjanvier=True
    if t2.exists():
        tfevrier=True
    if t3.exists():
        tmars=True
    if t4.exists():
        tavril=True
    if t5.exists():
        tmai=True
    if t6.exists():
        tjuin=True
    if t7.exists():
        tjuillet=True
    if t8.exists():
        taout=True
    if t9.exists():
        tseptembre=True
    if t10.exists():
        toctobre=True
    if t11.exists():
        tnovembre=True
    if t12.exists():
        tdecembre=True

##########
    if r1.exists():
        rjanvier=True
    if r2.exists():
        rfevrier=True
    if r3.exists():
        rmars=True
    if r4.exists():
        ravril=True
    if r5.exists():
        rmai=True
    if r6.exists():
        rjuin=True
    if r7.exists():
        rjuillet=True
    if r8.exists():
        raout=True
    if r9.exists():
        rseptembre=True
    if r10.exists():
        roctobre=True
    if r11.exists():
        rnovembre=True
    if r12.exists():
        rdecembre=True

    #######################

    if e1.exists():
        ejanvier=True
    if e2.exists():
        efevrier=True
    if e3.exists():
        emars=True
    if e4.exists():
        eavril=True
    if e5.exists():
        emai=True
    if e6.exists():
        ejuin=True
    if e7.exists():
        ejuillet=True
    if e8.exists():
        eaout=True
    if e9.exists():
        eseptembre=True
    if e10.exists():
        eoctobre=True
    if e11.exists():
        enovembre=True
    if e12.exists():
        edecembre=True


     #######################

    if f1.exists():
        fjanvier=True
    if f2.exists():
        ffevrier=True
    if f3.exists():
        fmars=True
    if f4.exists():
        favril=True
    if f5.exists():
        fmai=True
    if f6.exists():
        fjuin=True
    if f7.exists():
        fjuillet=True
    if f8.exists():
        faout=True
    if f9.exists():
        fseptembre=True
    if f10.exists():
        foctobre=True
    if f11.exists():
        fnovembre=True
    if f12.exists():
        fdecembre=True
   #######################

    if x1.exists():
        xjanvier=True
    if x2.exists():
        xfevrier=True
    if x3.exists():
        xmars=True
    if x4.exists():
        xavril=True
    if x5.exists():
        xmai=True
    if x6.exists():
        xjuin=True
    if x7.exists():
        xjuillet=True
    if x8.exists():
        xaout=True
    if x9.exists():
        xseptembre=True
    if x10.exists():
        xoctobre=True
    if x11.exists():
        xnovembre=True
    if x12.exists():
        xdecembre=True




    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"




    context = {
        "user": name,
        "poste": poste,
        "unite":u,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "tjanvier" :tjanvier,
        "tfevrier":tfevrier,
        "tmars":tmars,
        "tavril":tavril,
        "tmai" :tmai,
        "tjuin":tjuin,
        "tjuillet":tjuillet,
        "taout":taout,
        "tseptembre":tseptembre,
        "toctobre":toctobre,
        "tnovembre":tnovembre,
        "tdecembre":tdecembre,
        "rjanvier" :rjanvier,
        "rfevrier":rfevrier,
        "rmars":rmars,
        "ravril":ravril,
        "rmai" :rmai,
        "rjuin":rjuin,
        "rjuillet":rjuillet,
        "raout":raout,
        "rseptembre":rseptembre,
        "roctobre":roctobre,
        "rnovembre":rnovembre,
        "rdecembre":rdecembre,
        "ejanvier" :ejanvier,
        "efevrier":efevrier,
        "emars":emars,
        "eavril":eavril,
        "emai" :emai,
        "ejuin":ejuin,
        "ejuillet":ejuillet,
        "eaout":eaout,
        "eseptembre":eseptembre,
        "eoctobre":eoctobre,
        "enovembre":enovembre,
        "edecembre":edecembre,
        "fjanvier" :fjanvier,
        "ffevrier":ffevrier,
        "fmars":fmars,
        "favril":favril,
        "fmai" :fmai,
        "fjuin":fjuin,
        "fjuillet":fjuillet,
        "faout":faout,
        "fseptembre":fseptembre,
        "foctobre":foctobre,
        "fnovembre":fnovembre,
        "fdecembre":fdecembre,
        "xjanvier" :xjanvier,
        "xfevrier":xfevrier,
        "xmars":xmars,
        "xavril":xavril,
        "xmai" :xmai,
        "xjuin":xjuin,
        "xjuillet":xjuillet,
        "xaout":xaout,
        "xseptembre":xseptembre,
        "xoctobre":xoctobre,
        "xnovembre":xnovembre,
        "xdecembre":xdecembre,

     }   

    return render(request,'controle_budgetaire.html' , context)

#modfier le mois du controle
def edit_mounth_controle(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    mois=request.POST.get("mois")
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])

    com = controle_bud.objects.filter(ec=ec,type="trafic",mois=mois)
    poste = 'cadre'
    context = {
        "user": name,
        "poste": poste,
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
    return render(request,"edit_trafic_controle.html",context)

#erreur out of range 
def update_controle_trafic(request):
    mois=request.POST.getlist('mois')
    montant=request.POST.getlist('montant')
    rubrique=request.POST.getlist('rubrique')
    u = unite_1.objects.get(pk=request.session["unite"])
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])
   

    for i in range(len(montant)):

        c=controle_bud.objects.get(type="trafic",mois=mois[i],ec=ec,rubrique=rubrique[i])
        c.montant=montant[i]
        c.save()

    return redirect("controle_budgetaire")


###controle_trafic
def controle_trafic(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="trafic")

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

    context = {
        "user": name,
        "poste": poste,
        "unite":u,
       
        "compte":com,
        
        "form":form_controle1
     }   

    return render(request, "controle_trafic.html", context   )

#cette fonction recupere les valeurs de formulaires controle TRAFIC
def add_controle_trafic(request):
    compt = request.POST.getlist('compte')
    mois = request.POST.getlist('mois')
    montant = request.POST.getlist('montant')
    form=form_controle1(request.POST)
    ec = entete_pv.objects.get(type="controle",id=request.session["ec"])
        
    for c in range(len(compt)):  
          
            p = controle_bud(type="trafic",mois=mois[c],montant=montant[c],ec=ec,rubrique=compt[c],rempli=True)
            p.save()
    return redirect('controle_budgetaire')


###controle_recette
def controle_recette(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="recette")
    mois=request.POST.get("mois")


    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    context = {
        "user": name,
        "poste": poste,
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   

    return render(request, "controle_recette.html", context   )

#cette fonction recupere les valeurs de formulaires controle recette
def add_controle_recette(request):
    compt = request.POST.getlist('compte')
    mois = request.POST.getlist('mois')
    montant = request.POST.getlist('montant')
    form=form_controle1(request.POST)
    ec = entete_pv.objects.get(type="controle",id=request.session["ec"])
        
    for c in range(len(compt)):  
          
            p = controle_bud(type="recette",mois=mois[c],montant=montant[c],ec=ec,rubrique=compt[c],rempli=True)
            p.save()
    return redirect('controle_budgetaire')

###controle_emission
def controle_emission(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="emission")
    mois=request.POST.get("mois")


    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

        

    context = {
        "user": name,
        "poste": poste,
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
  
    return render(request, "controle_emission.html", context   )

#cette fonction recupere les valeurs de formulaires controle emission
def add_controle_emission(request):
    compt = request.POST.getlist('compte')
    mois = request.POST.getlist('mois')
    montant = request.POST.getlist('montant')
    form=form_controle1(request.POST)
    ec = entete_pv.objects.get(type="controle",id=request.session["ec"])
        
    for c in range(len(compt)):  
          
            p = controle_bud(type="emission",mois=mois[c],montant=montant[c],ec=ec,rubrique=compt[c],rempli=True)
            p.save()
    return redirect('controle_budgetaire')


############################################################praitraitement depense
def prt_depense(request):
    u = unite_1.objects.get(pk=request.session["unite"])
    ec = entete_pv.objects.get(type="controle",unite=u,annee=request.session["annee"])
    fonct = False
    expt = False
    c1 = controle_bud.objects.filter(ec=ec,type1="FONCTIONNEMENT")
    c2 = controle_bud.objects.filter(ec=ec,type1="EXPLOITATION")
    if c1.exists():
        fonct=True
    if c2.exists():
        expt=True
    
    
    context = {
        "unite":u,
        "expt":expt,
        "fonct":fonct
    }
    return render(request,'controle_depense2.html',context)


###controle_fonctionnement
def controle_depense(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    mois=request.POST.get("mois")

    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.all()
    for c in com:
        if not((c.type == "EXPLOITATION") | (c.type == "FONCTIONNEMENT")):
            com = com.exclude(pk=c.pk)
    u = unite_1.objects.get(pk=request.session["unite"])
    pro = unite_pos6.objects.filter(unite=u)
    for pros in pro:
        if not(pros.type=="FONCTIONNEMENT"):
            pro = pro.exclude(pk=pros.pk)
        
    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    context = {
        "user": name,
        "poste": poste,
        "unite":u,
        "mois":mois,
        "compte":pro,
        "form":form_controle1

        
     }   

    return render(request, "controle_fonctionnement.html", context   )




###controle_expoitation
def controle_depense2(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    mois=request.POST.get("mois")

    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.all()
    for c in com:
        if not((c.type == "EXPLOITATION") | (c.type == "FONCTIONNEMENT")):
            com = com.exclude(pk=c.pk)
    u = unite_1.objects.get(pk=request.session["unite"])
    pro = unite_pos6.objects.filter(unite=u)
    for pros in pro:
        if not(pros.type=="EXPLOITATION"):
            pro = pro.exclude(pk=pros.pk)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    
    context = {
        "user": name,
        "poste": poste,
        "unite":u,
        "mois":mois,
        "compte":pro,
        "form":form_controle1

        
     }   


    return render(request, "controle_exploitation.html", context   )






#cette fonction recupere les valeurs de formulaires controle depenses

def add_controle_depense(request):
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('compte')
    mois = request.POST.getlist('mois')
    montant = request.POST.getlist('montant')
    ec = entete_pv.objects.get(type="controle",id=request.session["ec"])
   
    for c in range(len(rubrique)):
        p = controle_bud(scf=scf[c],type1="FONCTIONNEMENT",type="depenses",ec=ec,rubrique=rubrique[c],mois=mois[c],montant=montant[c],rempli=True)
        p.save()
    return redirect('controle_budgetaire')

def add_controle_depense2(request):
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('compte')
    mois = request.POST.getlist('mois')
    montant = request.POST.getlist('montant')
    ec = entete_pv.objects.get(type="controle",id=request.session["ec"])
   
    for c in range(len(rubrique)):
        p = controle_bud(scf=scf[c],type1="EXPLOITATION",type="depenses",ec=ec,rubrique=rubrique[c],mois=mois[c],montant=montant[c],rempli=True)
        p.save()
    return redirect('controle_budgetaire')    

###################### Budget notifié #################
def unite_notifie(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_profile.objects.filter(pro=p)
    name = str(p.nom_user) + '     ' + str(p.prenom_user)


    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    context = {
        "user": name,
        "poste": poste,
        "unite": u,
    }
    return render(request,'unite_notifie.html',context)
def pre_consulter_notifier(request):

    request.session["unite_notif"]=request.POST.get("id")
    return redirect ('consulter_notifie')

def consulter_notifie(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u=unite_1.objects.get(id=request.session["unite_notif"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)+1
    print(u)
    print(date_act)
    en = entete_pv.objects.filter(type="notifie",annee=date_act,unite=u)
    print(en)
    print("iciiiiiiiiiiiiiiiiiiiii")
    if en.exists():
        en1=entete_pv.objects.filter(type="notifie",unite=u)
    else:
        en2=entete_pv(type="notifie",annee=date_act,unite=u)
        en2.save()
        en1=entete_pv.objects.filter(type="notifie",unite=u)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
    context = {
        "user": name,
        "poste": poste,
        "runion":en1,
    }
    return render(request,'consulter_notifie.html',context)

def pv_notifie(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    request.session['annee_notifie']=request.POST.get("annee")
   

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"

    context = {
        "poste": poste,
        "unite":u
        
    }
    return render(request,'pv_notifie.html',context)

def notifie_trafic(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])

    e =entete_pv.objects.get(type="notifie",unite=u,annee=request.session['annee_notifie'])
    r = notifie_bud.objects.filter(type="trafic",pv=e)
    if p.type_user == "cadre_bud":
            poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
            poste = "Chef de département"   
    if p.type_user == "sd":
            poste = "Sous-directeur"
    if r.exists():


        context = {
            "poste": poste,
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"notifie.html",context)
    else:
        pos = Pos6.objects.filter(type="trafic")
        for x in pos :
            n = notifie_bud(type="trafic",pv=e,annee=e.annee,rubrique=x.lib,prevision=0)
            n.save()

        r = notifie_bud.objects.filter(type="trafic",pv=e)

    if p.type_user == "cadre_bud":
        poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
        poste = "Chef de département"   
    if p.type_user == "sd":
        poste = "Sous-directeur"
        context = {
            "poste": poste,
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("notifie_trafic")

def verifier_n_trafic(request):
    p = profile.objects.get(user=request.user)
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()

# partie actualisation 
    u = unite_1.objects.get(id=request.session["unite_notif"])
    if p.type_user == "cdd" or p.type_user == "sd":
        a = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="modification")
        if not a.exists():
            a = entete_pv(unite=u,annee=request.session['annee_notifie'],type="modification")
            a.save()
        a = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="modification")

        a1 = modification.objects.filter(type="trafic",type_modif="actualisation",rubrique=r.rubrique,pv=a)
        if a1.exists():
            a1 = modification.objects.get(type="trafic",type_modif="actualisation",rubrique=r.rubrique,pv=a)

            a1.notifie=r.prevision
            a1.save()
        else:
            a1 = modification(type="trafic",type_modif="actualisation",rubrique=r.rubrique,pv=a,notifie=r.prevision,is_valide=True)
            
            a1.save()
        
        x = historique_modification(pv=a1.pv,type=a1.type,type_modif=a1.type_modif,rubrique=a1.rubrique,notifie=a1.notifie,modif=a1.modif,cadre1=a1.cadre1,cdd1=a1.cdd1,sd1=a1.sd1,monnaie=a1.monnaie,is_valide=a1.is_valide,cadre=a1.cadre,cdd=a1.cdd,sd=a1.sd)
        x.save()

# partie reajustement 
        a2 = modification.objects.filter(type="trafic",type_modif="reajustement",rubrique=r.rubrique,pv=a)
        if a2.exists():
            a2 = modification.objects.get(type="trafic",type_modif="reajustement",rubrique=r.rubrique,pv=a)

            a2.notifie=r.prevision
            a2.save()
        else:
            a2 = modification(type="trafic",type_modif="reajustement",is_valide=True,rubrique=r.rubrique,pv=a,notifie=r.prevision)
            a2.save()        
        x = historique_modification(pv=a2.pv,type=a2.type,type_modif=a2.type_modif,rubrique=a2.rubrique,notifie=a2.notifie,modif=a2.modif,cadre1=a2.cadre1,cdd1=a2.cdd1,sd1=a2.sd1,monnaie=a2.monnaie,is_valide=a2.is_valide,cadre=a2.cadre,cdd=a2.cdd,sd=a2.sd)
        x.save()



    return redirect('notifie_trafic')

def modifier_n_trafic(request):
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)

    r.is_valide = False

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

   

    r.save()
    return redirect('notifie_trafic')


def notifie_recette(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    e =entete_pv.objects.get(type="notifie",unite=u,annee=request.session['annee_notifie'])
    r = notifie_bud.objects.filter(type="recette",pv=e)

    if p.type_user == "cadre_bud":
            poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
            poste = "Chef de département"   
    if p.type_user == "sd":
            poste = "Sous-directeur"
    if r.exists():
        context = {
            "poste": poste,
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"notifie_recette.html",context)
    else:
        pos = Pos6.objects.filter(type="recette")
        for p in pos :
            n = notifie_bud(type="recette",pv=e,annee=e.annee,rubrique=p.lib,prevision=0)
            n.save()

        r = notifie_bud.objects.filter(type="recette",pv=e)
        if p.type_user == "cadre_bud":
            poste = 'Cadre Budgétaire'
        if p.type_user == "cdd":
            poste = "Chef de département"   
        if p.type_user == "sd":
            poste = "Sous-directeur"
        context = {
            "poste": poste,
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("notifie_recette")

def verifier_n_recette(request):
    p = profile.objects.get(user=request.user)
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()

# partie actualisation 
    u = unite_1.objects.get(id=request.session["unite_notif"])
    if p.type_user == "cdd" or p.type_user == "sd":
        a = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="modification")
        if not a.exists():
            a = entete_pv(unite=u,annee=request.session['annee_notifie'],type="modification")
            a.save()
        a = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="modification")

        a1 = modification.objects.filter(type="recette",type_modif="actualisation",rubrique=r.rubrique,pv=a)
        if a1.exists():
            a1 = modification.objects.get(type="recette",type_modif="actualisation",rubrique=r.rubrique,pv=a)

            a1.notifie=r.prevision
            a1.save()
        else:
            a1 = modification(type="recette",type_modif="actualisation",rubrique=r.rubrique,pv=a,notifie=r.prevision,is_valide=True)
            
            a1.save()
        
        x = historique_modification(pv=a1.pv,type=a1.type,type_modif=a1.type_modif,rubrique=a1.rubrique,notifie=a1.notifie,modif=a1.modif,cadre1=a1.cadre1,cdd1=a1.cdd1,sd1=a1.sd1,monnaie=a1.monnaie,is_valide=a1.is_valide,cadre=a1.cadre,cdd=a1.cdd,sd=a1.sd)
        x.save()

# partie reajustement 
        a2 = modification.objects.filter(type="recette",type_modif="reajustement",rubrique=r.rubrique,pv=a)
        if a2.exists():
            a2 = modification.objects.get(type="recette",type_modif="reajustement",rubrique=r.rubrique,pv=a)

            a2.notifie=r.prevision
            a2.save()
        else:
            a2 = modification(type="recette",type_modif="reajustement",is_valide=True,rubrique=r.rubrique,pv=a,notifie=r.prevision)
            a2.save()        
        x = historique_modification(pv=a2.pv,type=a2.type,type_modif=a2.type_modif,rubrique=a2.rubrique,notifie=a2.notifie,modif=a2.modif,cadre1=a2.cadre1,cdd1=a2.cdd1,sd1=a2.sd1,monnaie=a2.monnaie,is_valide=a2.is_valide,cadre=a2.cadre,cdd=a2.cdd,sd=a2.sd)
        x.save()



    return redirect('notifie_recette')

def modifier_n_recette(request):
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)

    r.is_valide = False

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

   

    r.save()
    return redirect('notifie_recette')



def notifie_emission(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    print(request.session['annee_notifie'])
    e =entete_pv.objects.get(type="notifie",unite=u,annee=request.session['annee_notifie'])
    r = notifie_bud.objects.filter(type="emission",pv=e)
    if p.type_user == "cadre_bud":
            poste = 'Cadre Budgétaire'
    if p.type_user == "cdd":
            poste = "Chef de département"   
    if p.type_user == "sd":
            poste = "Sous-directeur"
    if r.exists():
        context = {
            "poste": poste,
            "unite":u,
            "compte":r,      
            "profile":p          
    
                }
        return render(request,"notifie_emission.html",context)
    else:

        pos = Pos6.objects.filter(type="emission")
        for p in pos :
            n = notifie_bud(type="emission",pv=e,annee=e.annee,rubrique=p.lib,prevision=0)
            n.save()

        r = notifie_bud.objects.filter(type="emission",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p          

                 }
        return redirect("notifie_emission")

def verifier_n_emission(request):
    p = profile.objects.get(user=request.user)
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()

# partie actualisation 
    u = unite_1.objects.get(id=request.session["unite_notif"])
    if p.type_user == "cdd" or p.type_user == "sd":
        a = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="modification")
        if not a.exists():
            a = entete_pv(unite=u,annee=request.session['annee_notifie'],type="modification")
            a.save()
        a = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="modification")

        a1 = modification.objects.filter(type="emission",type_modif="actualisation",rubrique=r.rubrique,pv=a)
        if a1.exists():
            a1 = modification.objects.get(type="emission",type_modif="actualisation",rubrique=r.rubrique,pv=a)

            a1.notifie=r.prevision
            a1.save()
        else:
            a1 = modification(type="emission",type_modif="actualisation",rubrique=r.rubrique,pv=a,notifie=r.prevision,is_valide=True)
            
            a1.save()
        
        x = historique_modification(pv=a1.pv,type=a1.type,type_modif=a1.type_modif,rubrique=a1.rubrique,notifie=a1.notifie,modif=a1.modif,cadre1=a1.cadre1,cdd1=a1.cdd1,sd1=a1.sd1,monnaie=a1.monnaie,is_valide=a1.is_valide,cadre=a1.cadre,cdd=a1.cdd,sd=a1.sd)
        x.save()

# partie reajustement 
        a2 = modification.objects.filter(type="emission",type_modif="reajustement",rubrique=r.rubrique,pv=a)
        if a2.exists():
            a2 = modification.objects.get(type="emission",type_modif="reajustement",rubrique=r.rubrique,pv=a)

            a2.notifie=r.prevision
            a2.save()
        else:
            a2 = modification(type="emission",type_modif="reajustement",is_valide=True,rubrique=r.rubrique,pv=a,notifie=r.prevision)
            a2.save()        
        x = historique_modification(pv=a2.pv,type=a2.type,type_modif=a2.type_modif,rubrique=a2.rubrique,notifie=a2.notifie,modif=a2.modif,cadre1=a2.cadre1,cdd1=a2.cdd1,sd1=a2.sd1,monnaie=a2.monnaie,is_valide=a2.is_valide,cadre=a2.cadre,cdd=a2.cdd,sd=a2.sd)
        x.save()


    return redirect('notifie_emission')


def modifier_n_emission(request):
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)

    r.is_valide = False

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

   

    r.save()
    return redirect('notifie_emission')



def notifie_depenses(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    print(request.session['annee_notifie'])
    e =entete_pv.objects.get(type="notifie",unite=u,annee=request.session['annee_notifie'])
    r = notifie_bud.objects.filter(type="depenses",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,    
            "profile":p          
    
                }
        return render(request,"notifie_depenses.html",context)
    else:

        pos = unite_pos6.objects.filter(unite=u)     
        for i in pos :
            if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                pos = pos.exclude(id=i.id)
        for p in pos :
            n = notifie_bud(type="depenses",pv=e,annee=e.annee,rubrique=p.pos6.lib,prevision=0)
            n.save()

        r = notifie_bud.objects.filter(type="depenses",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p          

                 }
        return redirect("notifie_depenses")

def verifier_n_depenses(request):
    p = profile.objects.get(user=request.user)
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.prevision = request.POST.get("compte3")
    r.is_valide = True
    r.save()

# partie actualisation 
    u = unite_1.objects.get(id=request.session["unite_notif"])
    if p.type_user == "cdd" or p.type_user == "sd":
        a = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="modification")
        if not a.exists():
            a = entete_pv(unite=u,annee=request.session['annee_notifie'],type="modification")
            a.save()
        a = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="modification")

        a1 = modification.objects.filter(type="depenses",type_modif="actualisation",rubrique=r.rubrique,pv=a)
        if a1.exists():
            a1 = modification.objects.get(type="depenses",type_modif="actualisation",rubrique=r.rubrique,pv=a)

            a1.notifie=r.prevision
            a1.save()
        else:
            a1 = modification(type="depenses",type_modif="actualisation",rubrique=r.rubrique,pv=a,notifie=r.prevision,is_valide=True)
            
            a1.save()
        
        x = historique_modification(pv=a1.pv,type=a1.type,type_modif=a1.type_modif,rubrique=a1.rubrique,notifie=a1.notifie,modif=a1.modif,cadre1=a1.cadre1,cdd1=a1.cdd1,sd1=a1.sd1,monnaie=a1.monnaie,is_valide=a1.is_valide,cadre=a1.cadre,cdd=a1.cdd,sd=a1.sd)
        x.save()

# partie reajustement 
        a2 = modification.objects.filter(type="depenses",type_modif="reajustement",rubrique=r.rubrique,pv=a)
        if a2.exists():
            a2 = modification.objects.get(type="depenses",type_modif="reajustement",rubrique=r.rubrique,pv=a)

            a2.notifie=r.prevision
            a2.save()
        else:
            a2 = modification(type="depenses",type_modif="reajustement",is_valide=True,rubrique=r.rubrique,pv=a,notifie=r.prevision)
            a2.save()        
        x = historique_modification(pv=a2.pv,type=a2.type,type_modif=a2.type_modif,rubrique=a2.rubrique,notifie=a2.notifie,modif=a2.modif,cadre1=a2.cadre1,cdd1=a2.cdd1,sd1=a2.sd1,monnaie=a2.monnaie,is_valide=a2.is_valide,cadre=a2.cadre,cdd=a2.cdd,sd=a2.sd)
        x.save()



    return redirect('notifie_depenses')

def modifier_n_depenses(request):
    r = notifie_bud.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)

    r.is_valide = False

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

   

    r.save()
    return redirect('notifie_depenses')




def get_mounth_controle(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="trafic")
    mois=request.POST.get("mois")

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   

    return render (request,"controle_trafic.html",context)





    #modfier le mois du controle
def edit_controle_recette(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    mois=request.POST.get("mois")
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])

    com = controle_bud.objects.filter(ec=ec,type="recette",mois=mois)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
    return render(request,"edit_recette_controle.html",context)

#erreur out of range 
def update_controle_recette(request):
    mois=request.POST.getlist('mois')
    montant=request.POST.getlist('montant')
    rubrique=request.POST.getlist('rubrique')
    u = unite_1.objects.get(pk=request.session["unite"])
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])
   

    for i in range(len(montant)):

        c=controle_bud.objects.get(type="recette",mois=mois[i],ec=ec,rubrique=rubrique[i])
        c.montant=montant[i]
        c.save()

    return redirect("controle_budgetaire")


    #modfier le mois du controle[emission]
def edit_controle_emission(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    mois=request.POST.get("mois")
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])

    com = controle_bud.objects.filter(ec=ec,type="emission",mois=mois)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
    return render(request,"edit_emission_controle.html",context)

#erreur out of range [controle emission]
def update_controle_emission(request):
    mois=request.POST.getlist('mois')
    montant=request.POST.getlist('montant')
    rubrique=request.POST.getlist('rubrique')
    u = unite_1.objects.get(pk=request.session["unite"])
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])
   

    for i in range(len(montant)):

        c=controle_bud.objects.get(type="emission",mois=mois[i],ec=ec,rubrique=rubrique[i])
        c.montant=montant[i]
        c.save()

    return redirect("controle_budgetaire")

 #modfier le mois du controle[fonctionnement]
def edit_controle_fonctionnement(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    mois=request.POST.get("mois")
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])

    com = controle_bud.objects.filter(ec=ec,type="depenses",type1="FONCTIONNEMENT",mois=mois)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
  
    return render(request,"edit_fonctionnement_controle.html",context)

#erreur out of range [controle emission]
def update_controle_fonctionnement(request):
    mois=request.POST.getlist('mois')
    montant=request.POST.getlist('montant')
    rubrique=request.POST.getlist('rubrique')
    type1=request.POST.getlist('type1')
    u = unite_1.objects.get(pk=request.session["unite"])
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])
   

    for i in range(len(montant)):

        c=controle_bud.objects.get(type="depenses",type1=type1[i],mois=mois[i],ec=ec,rubrique=rubrique[i])
        c.montant=montant[i]
        c.save()

    return redirect("controle_budgetaire")

#modfier le mois du controle[exploitation]
def edit_controle_exploitation(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    mois=request.POST.get("mois")
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])

    com = controle_bud.objects.filter(ec=ec,type="depenses",type1="EXPLOITATION",mois=mois)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "form":form_controle1,
        'mois' : mois

     }   
  
    return render(request,"edit_exploitation_controle.html",context)

#erreur out of range [controle emission]
def update_controle_exploitation(request):
    mois=request.POST.getlist('mois')
    montant=request.POST.getlist('montant')
    rubrique=request.POST.getlist('rubrique')
    type1=request.POST.getlist('type1')
    u = unite_1.objects.get(pk=request.session["unite"])
    ec=entete_pv.objects.get(type="controle",unite=u,annee=request.session['annee'])
   

    for i in range(len(montant)):

        c=controle_bud.objects.get(type="depenses",type1=type1[i],mois=mois[i],ec=ec,rubrique=rubrique[i])
        c.montant=montant[i]
        c.save()

    return redirect("controle_budgetaire")









def consulter_controle(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

   
    context = {
      
      "user": name,
       "poste": "Cadre Budgetaire",


     }   
  

    return render(request,"consulter_controle.html",context)



def pre_consulter_controle(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    context = {
      
        "user": name,
        "poste": "Cadre Budgetaire",

     }   
  

    return render(request,"pre_consulter_controle.html",context)



######################## partie Realisation####################################

def islamvn1(request):
    request.session["unite1"]=request.POST.get("id")
    return redirect ("realisation_consulter")


def realisation_consulter(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
       
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite1"])
    
    print(u)
    pro = entete_pv.objects.filter(type="realisation")
   
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "pv":pro 
        
     }   

    return render(request, "consultation_realisation.html", context   )



################# choix annee realisation #################


def realisation_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    remplir = False
    user= p.type_user
    if user == "cadre_bud" or user == "cdd":
      remplir = True



    u = unite_profile.objects.filter(pro=p)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        'unite':u,
        "remplir":remplir
    }

    return render(request,"realisation_unite.html",context)


def islamvn(request):
    request.session['unite1']=request.POST.get('id')
    return redirect("pre_realisation")


def pre_realisation(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')  
    u = unite_1.objects.get(id=request.session['unite1'])
   
    context = {
        "form":form_budget,
    }
    return render(request,"pre_realisation.html",context)

def pre_traitement_realisation(request):
        u = unite_1.objects.get(id=request.session['unite1'])
        form = form_budget(request.POST)
        if form.is_valid():
            annee = form.cleaned_data['annee']
            request.session['annee1']=annee
            print(annee)
            print("soulef")

            pv = entete_pv.objects.filter(unite=u,type="realisation",annee=annee)
            if pv.exists():
                pv = entete_pv.objects.get(unite=u,type="realisation",annee=annee)

                request.session["pv1"]=pv.pk
                return redirect("realisation_budgetaire")
            else:
             print("test")
             pv = entete_pv(unite=u,annee=annee,type="realisation")
             pv.save()
             request.session["pv1"]=pv.id
             print(pv.annee)
            return redirect('realisation_budgetaire')
        
        context = {
        "form":form_budget,
                    }
        return render(request,"pre_realisation.html",context)    
        
    

def realisation_budgetaire(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    u = unite_1.objects.get(pk=request.session["unite1"])
    rtrafic = False
    rrecette = False
    remission = False
    rdepenses = False
    cdd = False
    cddr = False
    cdde = False
    cddd = False





    
    ep = entete_pv.objects.get(unite=u,annee=request.session["annee1"],type="realisation")
    p1 = realisation2.objects.filter(pv=ep,type="trafic")
    p2 = realisation2.objects.filter(pv=ep,type="recette")
    p3 = realisation2.objects.filter(pv=ep,type="emission")
    p4 = realisation2.objects.filter(pv=ep,type="depenses",type1='FONCTIONNEMENT')
    p5 = realisation2.objects.filter(pv=ep,type="depenses",type1='EXPLOITATION')



    

    if p1.exists():
        rtrafic = True
        if p1[0].cdd == True:
            cdd = True

    if p2.exists():
       rrecette = True 
       if p2[0].cdd == True:
            cddr = True

    if p3.exists():
        remission = True
        if p3[0].cdd == True:
            cdde = True

    if(p4.exists() & p5.exists()):
        rdepenses= True
        if (p4[0].cdd == True & p5[0].cdd == True):
            cddd = True

    usert_max=""
    usert_min=""
    dusert_max=""
    dusert_min=""

    userr_max=""
    userr_min=""
    duserr_max=""
    duserr_min=""

    usere_max=""
    usere_min=""
    dusere_max=""
    dusere_min=""

    userf_max=""
    userf_min=""
    duserf_max=""
    duserf_min=""

    userx_max=""
    userx_min=""
    duserx_max=""
    duserx_min=""
    trafic= False
    recette=False
    emission=False
    fonct=False
    expl=False

    if p1.exists():
        trafic=True
        usert_max=get_max_historique(request.session["annee1"],'realisation','trafic').user
        usert_min=get_min_historique(request.session["annee1"],'realisation','trafic').user
        dusert_max=get_max_historique(request.session["annee1"],'realisation','trafic').date_h
        dusert_min=get_min_historique(request.session["annee1"],'realisation','trafic').date_h
    


    if p2.exists():
        recette=True

        userr_max=get_max_historique(request.session["annee1"],'realisation','recette').user
        userr_min=get_min_historique(request.session["annee1"],'realisation','recette').user
        duserr_max=get_max_historique(request.session["annee1"],'realisation','recette').date_h
        duserr_min=get_min_historique(request.session["annee1"],'realisation','recette').date_h

    
    if p3.exists():
        emission= True
        usere_max=get_max_historique(request.session["annee1"],'realisation','emission').user
        usere_min=get_min_historique(request.session["annee1"],'realisation','emission').user
        dusere_max=get_max_historique(request.session["annee1"],'realisation','emission').date_h
        dusere_min=get_min_historique(request.session["annee1"],'realisation','emission').date_h

    


    if p4.exists():
        fonct=True

        userf_max=get_max_historique(request.session["annee1"],'realisation','FONCTIONNEMENT').user
        userf_min=get_min_historique(request.session["annee1"],'realisation','FONCTIONNEMENT').user
        duserf_max=get_max_historique(request.session["annee1"],'realisation','FONCTIONNEMENT').date_h
        duserf_min=get_min_historique(request.session["annee1"],'realisation','FONCTIONNEMENT').date_h

    if p5.exists():
        expl=True
        userx_max=get_max_historique(request.session["annee1"],'realisation','EXPLOITATION').user
        userx_min=get_min_historique(request.session["annee1"],'realisation','EXPLOITATION').user
        duserx_max=get_max_historique(request.session["annee1"],'realisation','EXPLOITATION').date_h
        duserx_min=get_min_historique(request.session["annee1"],'realisation','EXPLOITATION').date_h



    name = str(p.nom_user) + '     ' + str(p.prenom_user)
  

    
    print(p.type_user)
    print(cdd)
    print("je suis laaa")

    context = {
        "cdd": cdd,
        "cddr": cddr,
        "cdde": cdde,
        "cddd": cddd,


        "profile":p,
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
        "trafic":rtrafic,
        "recette":rrecette,
        "emission":remission,
        "depense":rdepenses,
        "usert_max": usert_max,
        "usert_min": usert_min,
        "dusert_max": dusert_max,
        "dusert_min": dusert_min,
        
       "userr_max": userr_max,
        "userr_min": userr_min,
        "duserr_max": duserr_max,
        "duserr_min": duserr_min,
        

        "usere_max": usere_max,
        "usere_min": usere_min,
        "dusere_max": dusere_max,
        "dusere_min": dusere_min,
        
        
       "userf_max": userf_max,
        "userf_min": userf_min,
        "duserf_max": duserf_max,
        "duserf_min": duserf_min,

        "userx_max": userx_max,
        "userx_min": userx_min,
        "duserx_max": duserx_max,
        "duserx_min": duserx_min,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "fonct":fonct,
        "expl":expl
        


     }   
    return render(request,"realisation_budgetaire.html",context)

def realisation_trafic(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite1"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="trafic")
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
       
        "compte":com,
       
        
     }   


    return render(request,"realisation_trafic.html",context)

#cette fonction recupere les valeurs de formulaires TRAFIC
def add_realisation_trafic(request):
    compt = request.POST.getlist('compte')
    # compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    u = unite_1.objects.get(pk=request.session["unite1"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_ajout=datetime.now()
    commentaire = request.POST.getlist('commentaire')


    pv = entete_pv.objects.get(id=request.session["pv1"])
    # print(compt2)
    print(compt3)
    for c in range(len(compt)):
        r =realisation2(type="trafic",pv=pv,rubrique=compt[c],realisation=compt3[c],scf=0,rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        if p.type_user=="cdd":
         r.cdd=True
        r.save()
    h = historique(annee=pv.annee,type="realisation",type_1="trafic",user=name,date_h=date_ajout)
    h.save()
    
    return redirect('realisation_budgetaire')

def edit_trafic_realisation(request):
    annee=request.session['annee1']

    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=annee,type="realisation")
    p=realisation2.objects.filter(pv=pv,type='trafic')
    user = profile.objects.get(user=request.user)

    context = {
        'pro': p,
        'unite':u,
        "profile":user
    }
    return render(request,'edit_trafic_realisation.html',context)

#MODIFICATION TRAFIC realisation
 
def update_trafic_realisation(request):
    current_year=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])
    
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="realisation")
    scf=request.POST.getlist('scf')
    realisation=request.POST.getlist('realisation')
    rubrique=request.POST.getlist('compte')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_ajout=datetime.now()
    for i in range(len(rubrique)) :
       r = realisation2.objects.get(type='trafic',pv=pv,rubrique=rubrique[i],scf=scf[i])
       r.commentaire=commentaire[i]
       r.realisation=realisation[i]
       if p.type_user=="cdd":
         r.cdd=True
       r.save()
    h = historique(annee=pv.annee,type="realisation",type_1="trafic",user=name,date_h=date_ajout)
    h.save()
    return redirect('realisation_budgetaire')


    
##################realisation recette###################
def realisation_recette(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite1"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="recette")
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
       
        "compte":com,
       
        
     }   


    return render(request,"realisation_recette.html",context)

#cette fonction recupere les valeurs de formulaires TRAFIC
def add_realisation_recette(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    u = unite_1.objects.get(pk=request.session["unite1"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    commentaire = request.POST.getlist('commentaire')
    date_ajout=datetime.now()

    pv = entete_pv.objects.get(id=request.session["pv1"])
    for c in range(len(compt)):
        r =realisation2(type="recette",pv=pv,rubrique=compt[c],realisation=compt3[c],scf=compt2[c],rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        if p.type_user=="cdd":
         r.cdd=True
        r.save()
    h = historique(annee=pv.annee,type="realisation",type_1="recette",user=name,date_h=date_ajout)
    h.save()
    
    return redirect('realisation_budgetaire')

def edit_recette_realisation(request):
    annee=request.session['annee1']

    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=annee,type="realisation")
    p=realisation2.objects.filter(pv=pv,type='recette')
    user = profile.objects.get(user=request.user)
    context = {
        'pro': p,
        'unite':u,
        'profile':user
    }
    return render(request,'edit_recette_realisation.html',context)

#MODIFICATION recette realisation
 
def update_recette_realisation(request):
    current_year=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])
    
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="realisation")
    scf=request.POST.getlist('scf')
    realisation=request.POST.getlist('realisation')
    rubrique=request.POST.getlist('compte')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()

    for i in range(len(rubrique)) :
       r = realisation2.objects.get(type='recette',pv=pv,rubrique=rubrique[i],scf=scf[i])
       r.realisation=realisation[i]
       r.commentaire=commentaire[i]
       if p.type_user=="cdd":
         r.cdd=True
       r.save()
    h = historique(annee=pv.annee,type="realisation",type_1="recette",user=name,date_h=date_modif)
    h.save()
    
    return redirect('realisation_budgetaire')


    
##################realisation emission ###################
def realisation_emission(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite1"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="emission")
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
       
        "compte":com,
       
        
     }   


    return render(request,"realisation_emission.html",context)

#cette fonction recupere les valeurs de formulaires TRAFIC
def add_realisation_emission(request):
    compt = request.POST.getlist('compte')
    compt2 = request.POST.getlist('compte2')
    compt3 = request.POST.getlist('compte3')
    u = unite_1.objects.get(pk=request.session["unite1"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    commentaire = request.POST.getlist('commentaire')
    date_ajout=datetime.now()
    pv = entete_pv.objects.get(id=request.session["pv1"])
    for c in range(len(compt)):
        r =realisation2(type="emission",pv=pv,rubrique=compt[c],realisation=compt3[c],scf=compt2[c],rempli=True,commentaire=commentaire[c],monnie=u.lib_monnaie,regler_par="unite")
        if p.type_user=="cdd":
         r.cdd=True
        
        r.save()

    h = historique(annee=pv.annee,type="realisation",type_1="emission",user=name,date_h=date_ajout)
    h.save()
    return redirect('realisation_budgetaire')

def edit_emission_realisation(request):
    annee=request.session['annee1']

    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=annee,type="realisation")
    p=realisation2.objects.filter(pv=pv,type='emission')
    user = profile.objects.get(user=request.user)
    context = {
        'pro': p,
        'unite':u,
        "profile":user
    }
    return render(request,'edit_emission_realisation.html',context)

#MODIFICATION emission realisation
 
def update_emission_realisation(request):
    current_year=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])
    
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="realisation")
    scf=request.POST.getlist('scf')
    realisation=request.POST.getlist('realisation')
    rubrique=request.POST.getlist('compte')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()

    for i in range(len(rubrique)) :
       r = realisation2.objects.get(type='emission',pv=pv,rubrique=rubrique[i],scf=scf[i])
       r.realisation=realisation[i]
       r.commentaire=commentaire[i]
       if p.type_user=="cdd":
         r.cdd=True
       r.save()
    
    h = historique(annee=pv.annee,type="realisation",type_1="emission",user=name,date_h=date_modif)
    h.save()
    return redirect('realisation_budgetaire')

############################# depense realisation ######################################
def realisation_depense(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite1"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    ep = entete_pv.objects.get(unite=u,annee=request.session["annee1"],type="realisation")
    p = realisation2.objects.filter(pv=ep,type="depenses",type1="FONCTIONNEMENT")
    p2 = realisation2.objects.filter(pv=ep,type1="EXPLOITATION")
    fonct = False
    expl = False
    if p.exists():
        fonct = True
    if p2.exists():
        expl = True
    context = {
       "unite":u,
       "fonct":fonct,
       "expl":expl
     }   

    return render(request,"realisation_depense.html",context)


def realisation_fonctionnement(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite1"])
    com = unite_pos6.objects.filter(unite=u,type="FONCTIONNEMENT")
    m = monnaie.objects.all()
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "monnaie":m
     }   

    return render(request, "realisation_fonctionnement.html", context   )
# add realisation fonctionnement ## 
def add_realisation_fonctionnement(request):
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    type = request.POST.getlist('type')
    compt3 = request.POST.getlist('compte3')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    u = unite_1.objects.get(pk=request.session["unite1"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()


    pv = entete_pv.objects.get(id=request.session["pv1"])
    for c in range(len(scf)):
        r =realisation2(type="depenses",type1='FONCTIONNEMENT',pv=pv,rubrique=rubrique[c],realisation=compt3[c],scf=scf[c],rempli=True,commentaire=commentaire[c],monnie=monnaie[c],regler_par=regler[c])
        if p.type_user=="cdd":
         r.cdd=True
        r.save()
    
    h = historique(annee=pv.annee,type="realisation",type_1="FONCTIONNEMENT",user=name,date_h=date_modif)
    h.save()
    return redirect('realisation_depense')

def edit_fonctionnement_realisation(request):
    annee=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])

    pv=entete_pv.objects.get(unite=u,annee=annee,type="realisation")
    p=realisation2.objects.filter(pv=pv,type1='FONCTIONNEMENT')
    m = monnaie.objects.all()
    user = profile.objects.get(user=request.user)

    context = {
        'pro': p,
        'unite':u,
        "monnaie":m,
        "profile":user
    }
    return render(request,'edit_fonctionnement_realisation.html',context)

#MODIFICATION emission realisation
 
def update_fonctionnement_realisation(request):
    current_year=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="realisation")
    
    scf=request.POST.getlist('scf')
    realisation=request.POST.getlist('realisation')
    rubrique=request.POST.getlist('rubrique')
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()


    for i in range(len(rubrique)) :
       r = realisation2.objects.get(type='depenses',type1='FONCTIONNEMENT',pv=pv,rubrique=rubrique[i],scf=scf[i])
       r.realisation=realisation[i]
       r.regler_par=regler[i]
       r.commentaire=commentaire[i]
       r.monnie=monnaie[i]
       if p.type_user=="cdd":
         r.cdd=True
       r.save()
    
    h = historique(annee=pv.annee,type="realisation",type_1="FONCTIONNEMENT",user=name,date_h=date_modif)
    h.save()
    return redirect('realisation_depense')




########################### depense realisation exploitation###############

def realisation_exploitation(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
   
   
    name = str(p.nom_user) + '     ' + str(p.prenom_user)

    u = unite_1.objects.get(pk=request.session["unite1"])
    com = unite_pos6.objects.filter(unite=u,type="EXPLOITATION")
    m = monnaie.objects.all()
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,  
        "compte":com,
        "monnaie":m
    
     }   

    return render(request, "realisation_exploitation.html", context   )
# add realisation fonctionnement ## 
def add_realisation_exploitation(request):
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    type = request.POST.getlist('type')
    compt3 = request.POST.getlist('compte3')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    u = unite_1.objects.get(pk=request.session["unite1"])
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()


    pv = entete_pv.objects.get(id=request.session["pv1"])
    for c in range(len(scf)):
        r =realisation2(type="depenses",type1='EXPLOITATION',pv=pv,rubrique=rubrique[c],realisation=compt3[c],scf=scf[c],rempli=True,commentaire=commentaire[c],monnie=monnaie[c],regler_par=regler[c])
        if p.type_user=="cdd":
         r.cdd=True
        r.save()
    
    h = historique(annee=pv.annee,type="realisation",type_1="EXPLOITATION",user=name,date_h=date_modif)
    h.save()
    return redirect('realisation_depense')

def edit_exploitation_realisation(request):
    annee=request.session['annee1']

    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=annee,type="realisation")
    p=realisation2.objects.filter(pv=pv,type1='EXPLOITATION')
    m = monnaie.objects.all()
    user = profile.objects.get(user=request.user)


    context = {
        'pro': p,
        'unite':u,
        "monnaie":m,
        "profile":user
    }
    return render(request,'edit_exploitation_realisation.html',context)

#MODIFICATION emission realisation
 
def update_exploitation_realisation(request):
    current_year=request.session['annee1']
    u=unite_1.objects.get(id=request.session['unite1'])
    pv=entete_pv.objects.get(unite=u,annee=current_year,type="realisation")
    
    scf=request.POST.getlist('scf')
    realisation=request.POST.getlist('realisation')
    rubrique=request.POST.getlist('rubrique')
    scf = request.POST.getlist('scf')
    rubrique = request.POST.getlist('rubrique')
    regler = request.POST.getlist('regler')
    monnaie = request.POST.getlist('monnaie')
    commentaire = request.POST.getlist('commentaire')
    p = profile.objects.get(user=request.user)
    name = str(p.nom_user) + ' ' + str(p.prenom_user)
    date_modif=datetime.now()


    for i in range(len(rubrique)) :
       r = realisation2.objects.get(type='depenses',type1='EXPLOITATION',pv=pv,rubrique=rubrique[i],scf=scf[i])
       r.realisation=realisation[i]
       r.regler_par=regler[i]
       r.commentaire=commentaire[i]
       r.monnie=monnaie[i]
       if p.type_user=="cdd":
         r.cdd=True
       r.save()
    
    h = historique(annee=pv.annee,type="realisation",type_1="EXPLOITATION",user=name,date_h=date_modif)
    h.save()
    return redirect('realisation_depense')

##################################consulter_realisation####################################################

def intermed_pv_realisation(request):
    request.session["annee3"]=int(request.POST.get("annee"))
    return redirect("pv_realisation")


def pv_realisation(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user=="administrateur"):
        return render(request, '404.html')
    
    u = unite_1.objects.get(pk=request.session["unite1"])
    pv = entete_pv.objects.get(annee=request.session["annee3"],unite=u,type="realisation")
    print(pv)
    pro = realisation2.objects.filter(type="trafic",pv=pv)
    print(pro)
    usert_max=""
    usert_min=""
    dusert_max=""
    dusert_min=""

    userr_max=""
    userr_min=""
    duserr_max=""
    duserr_min=""

    usere_max=""
    usere_min=""
    dusere_max=""
    dusere_min=""

    userf_max=""
    userf_min=""
    duserf_max=""
    duserf_min=""

    userx_max=""
    userx_min=""
    duserx_max=""
    duserx_min=""
    trafic= False
    recette=False
    emission=False
    fonct=False
    expl=False

    if pro.exists():
        trafic=True
        usert_max=get_max_historique(request.session["annee3"],'realisation','trafic').user
        usert_min=get_min_historique(request.session["annee3"],'realisation','trafic').user
        dusert_max=get_max_historique(request.session["annee3"],'realisation','trafic').date_h
        dusert_min=get_min_historique(request.session["annee3"],'realisation','trafic').date_h
    


    pro1 = realisation2.objects.filter(type="recette",pv=pv)
    if pro1.exists():
        recette=True

        userr_max=get_max_historique(request.session["annee3"],'realisation','recette').user
        userr_min=get_min_historique(request.session["annee3"],'realisation','recette').user
        duserr_max=get_max_historique(request.session["annee3"],'realisation','recette').date_h
        duserr_min=get_min_historique(request.session["annee3"],'realisation','recette').date_h

    
    pro2 = realisation2.objects.filter(type="emission",pv=pv)
    if pro2.exists():
        emission= True
        usere_max=get_max_historique(request.session["annee3"],'realisation','emission').user
        usere_min=get_min_historique(request.session["annee3"],'realisation','emission').user
        dusere_max=get_max_historique(request.session["annee3"],'realisation','emission').date_h
        dusere_min=get_min_historique(request.session["annee3"],'realisation','emission').date_h

    


    pro3 = realisation2.objects.filter(type1="FONCTIONNEMENT",pv=pv)
    if pro3.exists():
        fonct=True

        userf_max=get_max_historique(request.session["annee3"],'realisation','FONCTIONNEMENT').user
        userf_min=get_min_historique(request.session["annee3"],'realisation','FONCTIONNEMENT').user
        duserf_max=get_max_historique(request.session["annee3"],'realisation','FONCTIONNEMENT').date_h
        duserf_min=get_min_historique(request.session["annee3"],'realisation','FONCTIONNEMENT').date_h

    pro4 = realisation2.objects.filter(type1="EXPLOITATION",pv=pv)
    if pro4.exists():
        expl=True
        userx_max=get_max_historique(request.session["annee3"],'realisation','EXPLOITATION').user
        userx_min=get_min_historique(request.session["annee3"],'realisation','EXPLOITATION').user
        duserx_max=get_max_historique(request.session["annee3"],'realisation','EXPLOITATION').date_h
        duserx_min=get_min_historique(request.session["annee3"],'realisation','EXPLOITATION').date_h



    name = str(p.nom_user) + '     ' + str(p.prenom_user)
  

    
    context = {
        
       "user": name,
       "poste": "Cadre Budgetaire",
       "pro":pro,
       "pro1":pro1,
       "pro2":pro2,
       "pro3":pro3,
       "pro4":pro4,

       "unite":u,
        "usert_max": usert_max,
        "usert_min": usert_min,
        "dusert_max": dusert_max,
        "dusert_min": dusert_min,
        
       "userr_max": userr_max,
        "userr_min": userr_min,
        "duserr_max": duserr_max,
        "duserr_min": duserr_min,
        

        "usere_max": usere_max,
        "usere_min": usere_min,
        "dusere_max": dusere_max,
        "dusere_min": dusere_min,
        
        
       "userf_max": userf_max,
        "userf_min": userf_min,
        "duserf_max": duserf_max,
        "duserf_min": duserf_min,

        "userx_max": userx_max,
        "userx_min": userx_min,
        "duserx_max": duserx_max,
        "duserx_min": duserx_min,
        "trafic":trafic,
        "recette":recette,
        "emission":emission,
        "fonct":fonct,
        "expl":expl
        


        

        
     }   

    return render(request, "pv_realisation.html", context   )







#############################################################################################################################################

###################### mensuel notifie######################


def pv_notifie_m(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    print("alllo")
    print(u)
    request.session['annee_notifie']=request.POST.get("annee")
    pv = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="notifie_m")
    if not pv.exists():
        pv = entete_pv(unite=u,annee=request.session['annee_notifie'],type="notifie_m")
        pv.save()
    pv = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="notifie_m")
    request.session["pv_notifie"]=pv.id
    context = {
        "poste": "Cadre Budgetaire",
        "unite":u
        
    }
    return render(request,'pv_notifie_m.html',context)



def notifie_trafic_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite_notif"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="trafic")
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    n=notifie_bud_m.objects.filter(type='trafic',pv=e)
    if not n.exists() :
        for c in com :
            n=notifie_bud_m(type='trafic',pv=e,rubrique=c.lib)
            n.save()
    
    
    n=notifie_bud_m.objects.filter(type='trafic',pv=e)
    

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
        "profile":p,
        "compte":n
       
     }   

    return render(request, "notifie_trafic_m.html", context   )


# cette fonction recupere les valeurs de formulaires TRAFIC
def add_notifie_m(request):


    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    rubrique=request.POST.get("compte")
    janvier=request.POST.get("janvier")
    fevrier=request.POST.get("fevrier")
    mars=request.POST.get("mars")
    avril=request.POST.get("avril")
    mai=request.POST.get("mai")
    juin=request.POST.get("juin")
    juillet=request.POST.get("juillet")
    aout=request.POST.get("aout")
    septembre=request.POST.get("septembre")
    octobre=request.POST.get("octobre")
    novembre=request.POST.get("novembre")
    decembre=request.POST.get("decembre")

    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=True
    n.janvier=janvier
    n.fevrier=fevrier
    n.mars=mars
    n.avril=avril
    n.mai=mai
    n.juin=juin
    n.juillet=juillet
    n.aout=aout
    n.septembre=septembre
    n.octobre=octobre
    n.novembre=novembre
    n.decembre=decembre
    p = profile.objects.get(user=request.user)
    ##### modification de la valeur de annuel
    somme = float(janvier)+ float(fevrier)+float(mars)+float(avril)+float(mai)+float(juin)+float(juillet)+float(aout)+float(septembre)+float(octobre)+float(novembre)+float(decembre)
    pv = entete_pv.objects.get(type="notifie",annee=n.pv.annee,unite=n.pv.unite) 
    ne = notifie_bud.objects.filter(pv=pv,type=n.type,rubrique=n.rubrique)
    if not ne.exists():
        ne = notifie_bud(pv=pv,type=n.type,rubrique=n.rubrique)
        ne.save()
    ne = notifie_bud.objects.get(pv=pv,type=n.type,rubrique=n.rubrique)
    ne.prevision=somme
    ne.is_valide=True
    if p.type_user == "cadre_bud" :
        n.cadre=p
        n.cadre1=True
        n.save()
        ne.cadre=p
        ne.cadre1=True
        ne.cdd=None
        ne.cdd1=False
        ne.sd=None
        ne.sd1=False
    elif p.type_user == "cdd" :
        n.cdd=p
        n.cdd1=True
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=p
        ne.cdd1=True
        ne.sd=None
        ne.sd1=False
    else :
        n.sd1=True
        n.sd=p
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=None
        ne.cdd1=False
        ne.sd=p
        ne.sd1=True
    ne.save()
    return redirect('notifie_trafic_m')

def modifier_trafic_m(request):
    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=False
    p = profile.objects.get(user=request.user)
    if p.type_user == "cadre_bud" :
        n.cadre=None
        n.cadre1=False
        n.save()
    elif p.type_user == "cdd" :
        n.cdd=None
        n.cdd1=False
        n.save()
    else :
        n.sd1=None
        n.sd=False
        n.save()

    return redirect('notifie_trafic_m')

# ************************************************************actualisation  ************************************************************************************************************

def actualisation_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user == "administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)


    u = unite_profile.objects.filter(pro=p)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        'unite':u
    }

    return render(request,"actualisation_unite.html",context)

def pre_consulter_actualisation(request):

    request.session["unite_act"]=request.POST.get("id")
    return redirect ('actualisation_consulter')

def actualisation_consulter(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u=unite_1.objects.get(id=request.session["unite_act"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)+1

    en = entete_pv.objects.filter(type="modification",annee=date_act,unite=u)
    if en.exists():
        en1=entete_pv.objects.filter(type="modification",unite=u)
    else:
        en2=entete_pv(type="modification",annee=date_act,unite=u)
        en2.save()
        en1=entete_pv.objects.filter(type="modification",unite=u)

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "runion":en1,
    }
    return render(request,"actualisation_consulter.html",context)



def pv_actualisation(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    request.session['annee_act']=request.POST.get("annee")
   

    context = {
        "poste": "Cadre Budgetaire",
        "unite":u
        
    }
    return render(request,'pv_actualisation.html',context)
   
    


def actualisation_trafic(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_notifie'])
    r = modification.objects.filter(type="trafic",type_modif="actualisation",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"actualisation_trafic.html",context)
    else:
        pos = Pos6.objects.filter(type="trafic")
        for p in pos :
            n = modification(type="trafic",type_modif="actualisation",pv=e,rubrique=p.lib,modif=0,is_valide=True)
            n.save()

        r = modification.objects.filter(type="trafic",type_modif="actualisation",pv=e)
        print(r)
        print("alllooooooooooooooo")
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("actualisation_trafic")


def verifier_a_trafic(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  

    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()

       


    return redirect('actualisation_trafic')

def modifier_a_trafic(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('actualisation_trafic')

def actualisation_recette(request):
    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_notifie'])
    r = modification.objects.filter(type="recette",type_modif="actualisation",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"actualisation_recette.html",context)
    else:
        pos = Pos6.objects.filter(type="recette")
        for p in pos :
            n = modification(type="recette",type_modif="actualisation",pv=e,rubrique=p.lib,modif=0,is_valide=True)
            n.save()

        r = modification.objects.filter(type="recette",type_modif="actualisation",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("actualisation_recette")




def verifier_a_recette(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.rubrique)
        # nn = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.rubrique)
# false a regler :
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()

       

    return redirect('actualisation_recette')

def modifier_a_recette(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('actualisation_recette')


def actualisation_emission(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_notifie'])
    r = modification.objects.filter(type="emission",type_modif="actualisation",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"actualisation_emission.html",context)
    else:
        pos = Pos6.objects.filter(type="emission")
        for p in pos :
            n = modification(type="emission",type_modif="actualisation",pv=e,rubrique=p.lib,modif=0,is_valide=True)
            n.save()

        r = modification.objects.filter(type="emission",type_modif="actualisation",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("actualisation_emission")



def verifier_a_emission(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()

       

    return redirect('actualisation_emission')

def modifier_a_emission(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('actualisation_emission')




def actualisation_depense(request):
    
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_notifie'])
    r = modification.objects.filter(type="depenses",type_modif="actualisation",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"actualisation_depense.html",context)
    else:
        pos = unite_pos6.objects.filter(unite=u)     
        for i in pos :
            if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                    pos = pos.exclude(id=i.id)

           
        for re in pos :
                   
            n = modification(type="depenses",pv=e,type_modif="actualisation",rubrique=re.pos6.lib,modif=0,is_valide=True)
            n.save()

        r = modification.objects.filter(type="depenses",type_modif="actualisation",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }

        return redirect("actualisation_depense")


def verifier_a_depense(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  
    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="depenses",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="depenses",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="depenses",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="depenses",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="depenses",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="depenses",rubrique=r.rubrique)
          n.modification = r
          n.save()

       

    return redirect('actualisation_depense')

def modifier_a_depense(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('actualisation_depense')






# partie reajustement *************************************************************************



def reajustement_unite(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user == "administrateur"):
        return render(request, '404.html')  
    name = str(p.nom_user) + '     ' + str(p.prenom_user)


    u = unite_profile.objects.filter(pro=p)
    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        'unite':u
    }

    return render(request,"reajustement_unite.html",context)

def pre_consulter_reajustement(request):

    request.session["unite_act"]=request.POST.get("id")
    return redirect ('reajustement_consulter')

def reajustement_consulter(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u=unite_1.objects.get(id=request.session["unite_act"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    date_act = int(datetime.now().year)+1

    en = entete_pv.objects.filter(type="modification",annee=date_act,unite=u)
    if en.exists():
        en1=entete_pv.objects.filter(type="modification",unite=u)
    else:
        en2=entete_pv(type="modification",annee=date_act,unite=u)
        en2.save()
        en1=entete_pv.objects.filter(type="modification",unite=u)

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "runion":en1,
    }
    return render(request,"reajustement_consulter.html",context)



def pv_reajustement(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    request.session['annee_act']=request.POST.get("annee")
   

    context = {
        "poste": "Cadre Budgetaire",
        "unite":u
        
    }
    return render(request,'pv_reajustement.html',context)
   
    

 # trafic reajustement

def reajustement_trafic(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_act'])
    r = modification.objects.filter(type="trafic",type_modif="reajustement",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"reajustement_trafic.html",context)
    else:
        pos = Pos6.objects.filter(type="trafic")
        for p in pos :
            n = modification(type="trafic",pv=e,rubrique=p.lib,modif=0,is_valide=True,type_modif="reajustement")
            n.save()

        r = modification.objects.filter(type="trafic",type_modif="reajustement",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("reajustement_trafic")


def verifier_r_trafic(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  

    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="trafic",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="trafic",rubrique=r.rubrique)
          n.modification = r
          n.save()

       


    return redirect('reajustement_trafic')

def modifier_r_trafic(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('reajustement_trafic')


 # recette reajustement
  

def reajustement_recette(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_act'])
    r = modification.objects.filter(type="recette",type_modif="reajustement",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"reajustement_recette.html",context)
    else:
        pos = Pos6.objects.filter(type="recette")
        for p in pos :
            n = modification(type="recette",pv=e,rubrique=p.lib,modif=0,is_valide=True,type_modif="reajustement")
            n.save()

        r = modification.objects.filter(type="recette",type_modif="reajustement",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("reajustement_recette")


def verifier_r_recette(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  

    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="recette",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="recette",rubrique=r.rubrique)
          n.modification = r
          n.save()

       


    return redirect('reajustement_recette')

def modifier_r_recette(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('reajustement_recette')

# emission reajustement


def reajustement_emission(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_act'])
    r = modification.objects.filter(type="emission",type_modif="reajustement",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"reajustement_emission.html",context)
    else:
        pos = Pos6.objects.filter(type="emission")
        for p in pos :
            n = modification(type="emission",pv=e,rubrique=p.lib,modif=0,is_valide=True,type_modif="reajustement")
            n.save()

        r = modification.objects.filter(type="emission",type_modif="reajustement",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }
        return redirect("reajustement_emission")


def verifier_r_emission(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  

    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()
    
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="emission",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="emission",rubrique=r.rubrique)
          n.modification = r
          n.save()

       


    return redirect('reajustement_emission')

def modifier_r_emission(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('reajustement_emission')

# depense reajustement 


def reajustement_depense(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user =="administrateur"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_act"])
    e =entete_pv.objects.get(type="modification",unite=u,annee=request.session['annee_act'])
    r = modification.objects.filter(type="depenses",type_modif="reajustement",pv=e)
    if r.exists():
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,            
            "profile":p            
    
    
                }
        return render(request,"reajustement_depense.html",context)
    else:
        pos = unite_pos6.objects.filter(unite=u)     
        for i in pos :
            if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                    pos = pos.exclude(id=i.id)

           
        for re in pos :
                   
            n = modification(type="depenses",pv=e,type_modif="reajustement",rubrique=re.pos6.lib,modif=0,is_valide=True)
            n.save()

        r = modification.objects.filter(type="depenses",type_modif="reajustement",pv=e)
        context = {
            "poste": "Cadre Budgetaire",
            "unite":u,
            "compte":r,
            "profile":p            
                 }

        return redirect("reajustement_depense")


def verifier_r_depense(request):
    p = profile.objects.get(user=request.user)
    r = modification.objects.get(pk = request.POST.get("id"))
  

    if p.type_user=="cadre_bud":
        r.cadre = p
        r.date1=datetime.now()
        r.cadre1 = True
    if p.type_user=="cdd":
        r.cdd = p
        r.date2=datetime.now()
        r.cdd1=True
    if p.type_user=="sd":
        r.sd = p
        r.date3=datetime.now()
        r.sd1=True

    r.modif = request.POST.get("modif")
    r.is_valide = False
    r.save()

    x = historique_modification(pv=r.pv,type=r.type,type_modif=r.type_modif,rubrique=r.rubrique,notifie=r.notifie,modif=r.modif,cadre1=r.cadre1,cdd1=r.cdd1,sd1=r.sd1,monnaie=r.monnaie,is_valide=r.is_valide,cadre=r.cadre,cdd=r.cdd,sd=r.sd)
    x.save()

    
    e = entete_pv.objects.filter(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
    if e.exists():
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="depense",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="depense",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="depense",rubrique=r.rubrique)
          n.modification = r
          n.save()

       
    else:
        e = entete_pv(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        e = entete_pv.objects.get(unite=r.pv.unite,annee=r.pv.annee,type="notifie")
        n = notifie_bud.objects.filter(pv=e,type="depense",rubrique=r.rubrique)
        if n.exists():
          n = notifie_bud.objects.get(pv=e,type="depense",rubrique=r.rubrique)
          n.modification = r
          n.save()
        else:
          n = notifie_bud(pv=e,type="depense",rubrique=r.rubrique)
          n.modification = r
          n.save()

       


    return redirect('reajustement_depense')

def modifier_r_depense(request):
    r = modification.objects.get(pk = request.POST.get("id"))
    p = profile.objects.get(user=request.user)
    
    r.is_valide = True

    if p.type_user=="cadre_bud":
        r.cadre = None
        r.date1=""
        r.cadre1 = False
    if p.type_user=="cdd":
        r.cdd = None
        r.date2=""
        r.cdd1 = False
    if p.type_user=="sd":
        r.sd = None
        r.date3=""
        r.sd1 = False

    r.save()
    return redirect('reajustement_depense')


def pv_actualisation_m(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    print("alllo")
    print(u)
    request.session['annee_notifie']=request.POST.get("annee")
    pv = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="notifie")
    if not pv.exists():
        pv = entete_pv(unite="u",annee=request.session['annee_notifie'],type="notifie")
        pv.save()
    pv = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="notifie")
    request.session["pv_notifie"]=pv.id
    context = {
        "poste": "Cadre Budgetaire",
        "unite":u
        
    }
    return render(request,'pv_actualisation_m.html',context)


def actualisation_trafic_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   

    return render(request, "actualisation_trafic_m.html", context   )


def actualisation_recette_m(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   

    return render(request, "actualisation_recette_m.html", context   )


def actualisation_emission_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   


    return render(request, "actualisation_emission_m.html", context   )


def actualisation_depenses_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   


    return render(request, "actualisation_depenses_m.html", context   )



def notifie_depenses_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
    u = unite_1.objects.get(pk=request.session["unite_notif"])
    pos = unite_pos6.objects.filter(unite=u)     
    for i in pos :
        if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
            pos = pos.exclude(id=i.id)
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    n=notifie_bud_m.objects.filter(type='depenses',pv=e)
    if not n.exists() :
        for c in pos :
            n=notifie_bud_m(type='depenses',pv=e,rubrique=c.pos6.lib)
            n.save()
    
    
    n=notifie_bud_m.objects.filter(type='depenses',pv=e)
    context = {
        "poste": "Cadre Budgetaire",
        "unite":u,
        "profile":p,
        "compte":n
       
     }   


    return render(request, "notifie_depenses_m.html", context   )

def add_depenses_m(request):
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    rubrique=request.POST.get("compte")
    janvier=request.POST["janvier"]
    fevrier=request.POST["fevrier"]
    mars=request.POST["mars"]
    avril=request.POST["avril"]
    mai=request.POST["mai"]
    juin=request.POST["juin"]
    juillet=request.POST["juillet"]
    aout=request.POST["aout"]
    septembre=request.POST["septembre"]
    octobre=request.POST["octobre"]
    novembre=request.POST["novembre"]
    decembre=request.POST["decembre"]
    
    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=True
    n.janvier=janvier
    n.fevrier=fevrier
    n.mars=mars
    n.avril=avril
    n.mai=mai
    n.juin=juin
    n.juillet=juillet
    n.aout=aout
    n.septembre=septembre
    n.octobre=octobre
    n.novembre=novembre
    n.decembre=decembre
    p = profile.objects.get(user=request.user)
    ##### modification de la valeur de annuel
    somme = float(janvier)+ float(fevrier)+float(mars)+float(avril)+float(mai)+float(juin)+float(juillet)+float(aout)+float(septembre)+float(octobre)+float(novembre)+float(decembre)
    pv = entete_pv.objects.get(type="notifie",annee=n.pv.annee,unite=n.pv.unite) 
    ne = notifie_bud.objects.filter(pv=pv,type=n.type,rubrique=n.rubrique)
    if not ne.exists():
        ne = notifie_bud(pv=pv,type=n.type,rubrique=n.rubrique)
        ne.save()
    ne = notifie_bud.objects.get(pv=pv,type=n.type,rubrique=n.rubrique)
    ne.prevision=somme
    ne.is_valide=True
    if p.type_user == "cadre_bud" :
        n.cadre=p
        n.cadre1=True
        n.save()
        ne.cadre=p
        ne.cadre1=True
        ne.cdd=None
        ne.cdd1=False
        ne.sd=None
        ne.sd1=False
    elif p.type_user == "cdd" :
        n.cdd=p
        n.cdd1=True
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=p
        ne.cdd1=True
        ne.sd=None
        ne.sd1=False
    else :
        n.sd1=True
        n.sd=p
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=None
        ne.cdd1=False
        ne.sd=p
        ne.sd1=True
    ne.save()
    return redirect('notifie_depenses_m')

def modifier_depenses_m(request):
    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=False
    p = profile.objects.get(user=request.user)
    if p.type_user == "cadre_bud" :
        n.cadre=None
        n.cadre1=False
        n.save()
    elif p.type_user == "cdd" :
        n.cdd=None
        n.cdd1=False
        n.save()
    else :
        n.sd1=None
        n.sd=False
        n.save()

    return redirect('notifie_depenses_m')



##############################################################
def notifie_emission_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite_notif"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="emission")
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    n=notifie_bud_m.objects.filter(type='emission',pv=e)
    if not n.exists() :
        for c in com :
            n=notifie_bud_m(type='emission',pv=e,rubrique=c.lib)
            n.save()
    
    
    n=notifie_bud_m.objects.filter(type='emission',pv=e)
    

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
        "profile":p,
        "compte":n
       
     }   


    return render(request, "notifie_emission_m.html", context   )

def add_emission_m(request):
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    rubrique=request.POST.get("compte")
    janvier=request.POST.get("janvier")
    fevrier=request.POST.get("fevrier")
    mars=request.POST.get("mars")
    avril=request.POST.get("avril")
    mai=request.POST.get("mai")
    juin=request.POST.get("juin")
    juillet=request.POST.get("juillet")
    aout=request.POST.get("aout")
    septembre=request.POST.get("septembre")
    octobre=request.POST.get("octobre")
    novembre=request.POST.get("novembre")
    decembre=request.POST.get("decembre")

    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=True
    n.janvier=janvier
    n.fevrier=fevrier
    n.mars=mars
    n.avril=avril
    n.mai=mai
    n.juin=juin
    n.juillet=juillet
    n.aout=aout
    n.septembre=septembre
    n.octobre=octobre
    n.novembre=novembre
    n.decembre=decembre
    p = profile.objects.get(user=request.user)
    ##### modification de la valeur de annuel
    somme = float(janvier)+ float(fevrier)+float(mars)+float(avril)+float(mai)+float(juin)+float(juillet)+float(aout)+float(septembre)+float(octobre)+float(novembre)+float(decembre)
    pv = entete_pv.objects.get(type="notifie",annee=n.pv.annee,unite=n.pv.unite) 
    ne = notifie_bud.objects.filter(pv=pv,type=n.type,rubrique=n.rubrique)
    if not ne.exists():
        ne = notifie_bud(pv=pv,type=n.type,rubrique=n.rubrique)
        ne.save()
    ne = notifie_bud.objects.get(pv=pv,type=n.type,rubrique=n.rubrique)
    ne.prevision=somme
    ne.is_valide=True
    if p.type_user == "cadre_bud" :
        n.cadre=p
        n.cadre1=True
        n.save()
        ne.cadre=p
        ne.cadre1=True
        ne.cdd=None
        ne.cdd1=False
        ne.sd=None
        ne.sd1=False
    elif p.type_user == "cdd" :
        n.cdd=p
        n.cdd1=True
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=p
        ne.cdd1=True
        ne.sd=None
        ne.sd1=False
    else :
        n.sd1=True
        n.sd=p
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=None
        ne.cdd1=False
        ne.sd=p
        ne.sd1=True
    ne.save()

    return redirect('notifie_emission_m')

def modifier_emission_m(request):
    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=False
    p = profile.objects.get(user=request.user)
    if p.type_user == "cadre_bud" :
        n.cadre=None
        n.cadre1=False
        n.save()
    elif p.type_user == "cdd" :
        n.cdd=None
        n.cdd1=False
        n.save()
    else :
        n.sd1=None
        n.sd=False
        n.save()

    return redirect('notifie_emission_m')



################################################################

def notifie_recette_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
   
    u = unite_1.objects.get(pk=request.session["unite_notif"])
    name = str(p.nom_user) + '     ' + str(p.prenom_user)
    com = Pos6.objects.filter(type="recette")
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    n=notifie_bud_m.objects.filter(type='recette',pv=e)
    if not n.exists() :
        for c in com :
            n=notifie_bud_m(type='recette',pv=e,rubrique=c.lib)
            n.save()
    
    
    n=notifie_bud_m.objects.filter(type='recette',pv=e)
    

    context = {
        "user": name,
        "poste": "Cadre Budgetaire",
        "unite":u,
        "profile":p,
        "compte":n
       
     }   


    return render(request, "notifie_recette_m.html", context   )

def add_recette_m(request):
    e=entete_pv.objects.get(id=request.session["pv_notifie"])
    rubrique=request.POST.get("compte")
    janvier=request.POST.get("janvier")
    fevrier=request.POST.get("fevrier")
    mars=request.POST.get("mars")
    avril=request.POST.get("avril")
    mai=request.POST.get("mai")
    juin=request.POST.get("juin")
    juillet=request.POST.get("juillet")
    aout=request.POST.get("aout")
    septembre=request.POST.get("septembre")
    octobre=request.POST.get("octobre")
    novembre=request.POST.get("novembre")
    decembre=request.POST.get("decembre")

    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=True
    n.janvier=janvier
    n.fevrier=fevrier
    n.mars=mars
    n.avril=avril
    n.mai=mai
    n.juin=juin
    n.juillet=juillet
    n.aout=aout
    n.septembre=septembre
    n.octobre=octobre
    n.novembre=novembre
    n.decembre=decembre
    p = profile.objects.get(user=request.user)
    ##### modification de la valeur de annuel
    somme = float(janvier)+ float(fevrier)+float(mars)+float(avril)+float(mai)+float(juin)+float(juillet)+float(aout)+float(septembre)+float(octobre)+float(novembre)+float(decembre)
    pv = entete_pv.objects.get(type="notifie",annee=n.pv.annee,unite=n.pv.unite) 
    ne = notifie_bud.objects.filter(pv=pv,type=n.type,rubrique=n.rubrique)
    if not ne.exists():
        ne = notifie_bud(pv=pv,type=n.type,rubrique=n.rubrique)
        ne.save()
    ne = notifie_bud.objects.get(pv=pv,type=n.type,rubrique=n.rubrique)
    ne.prevision=somme
    ne.is_valide=True
    if p.type_user == "cadre_bud" :
        n.cadre=p
        n.cadre1=True
        n.save()
        ne.cadre=p
        ne.cadre1=True
        ne.cdd=None
        ne.cdd1=False
        ne.sd=None
        ne.sd1=False
    elif p.type_user == "cdd" :
        n.cdd=p
        n.cdd1=True
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=p
        ne.cdd1=True
        ne.sd=None
        ne.sd1=False
    else :
        n.sd1=True
        n.sd=p
        n.save()
        ne.cadre=None
        ne.cadre1=False
        ne.cdd=None
        ne.cdd1=False
        ne.sd=p
        ne.sd1=True
    ne.save()
    return redirect('notifie_recette_m')

def modifier_recette_m(request):
    n = notifie_bud_m.objects.get(id=request.POST.get("id"))
    n.is_valide=False
    p = profile.objects.get(user=request.user)
    if p.type_user == "cadre_bud" :
        n.cadre=None
        n.cadre1=False
        n.save()
    elif p.type_user == "cdd" :
        n.cdd=None
        n.cdd1=False
        n.save()
    else :
        n.sd1=None
        n.sd=False
        n.save()

    return redirect('notifie_recette_m')

def pv_reajustement_m(request):
    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
    u = unite_1.objects.get(id=request.session["unite_notif"])
    print("alllo")
    print(u)
    request.session['annee_notifie']=request.POST.get("annee")
    pv = entete_pv.objects.filter(unite=u,annee=request.session['annee_notifie'],type="notifie")
    if not pv.exists():
        pv = entete_pv(unite="u",annee=request.session['annee_notifie'],type="notifie")
        pv.save()
    pv = entete_pv.objects.get(unite=u,annee=request.session['annee_notifie'],type="notifie")
    request.session["pv_notifie"]=pv.id
    context = {
        "poste": "Cadre Budgetaire",
        "unite":u
        
    }
    return render(request,'pv_reajustement_m.html',context)


def reajustement_trafic_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   

    return render(request, "reajustement_trafic_m.html", context   )


def reajustement_recette_m(request):

    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   

    return render(request, "reajustement_recette_m.html", context   )


def reajustement_emission_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   


    return render(request, "reajustement_emission_m.html", context   )


def reajustement_depenses_m(request):


    if (not request.user.is_authenticated):
        return render(request, '404.html')
    p = profile.objects.get(user=request.user)
    if ( p.type_user!="cadre_bud"):
        return render(request, '404.html')
 
    context = {
  
       
     }   


    return render(request, "reajustement_depenses_m.html", context   )

##### hiba: notification's fct ######
def create_notif(pv, user):

    up = unite_profile.objects.filter(unite= pv.unite)
    if up.exists :
        ## unite_pro = unite_profile.objects.get(unite=pv.unite)
        for unpr in up :
            pro = unpr.pro
            if (pro.type_user=='sd' and not user.type_user=='sd'):
                if not pv.type in {'controle','proposition'}:
                    notif = notification(pv=pv, notified_user=pro, modifier_user=user , date=datetime.now())
                    notif.save()       
            if (pro.type_user== 'cdd' and user.type_user=='cadre_bud'):
                notif = notification(pv=pv, notified_user=pro, modifier_user=user , date=datetime.now())
                notif.save()
    
def get_notifications(user):
    n = notification.objects.filter(notified_user=user)
    if n.exists:
        return n