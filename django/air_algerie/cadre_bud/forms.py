from django import forms
from django.contrib.auth.models import User
from django.forms.fields import CharField, ChoiceField
from django.forms.widgets import RadioSelect


class form_login(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder':'Username',
            'class':'form-control'
        })
    )
    password= forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'placeholder':'*****',
            'class':'form-control'

        })
    )

class form_budget(forms.Form):
    annee = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class":"form-control",
            "placeholder":"2019",
            "aria-label":"Name"
        })
    )


class form_controle(forms.Form):
    annee = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class":"form-control",
            "placeholder":"2019",
            "aria-label":"Name"
        })
    )

    

class form_controle1(forms.Form):
    mois_choix = [
        ("janvier","janvier"),
        ("fevrier","fevrier"),
        ("mars","mars"),
        ("avril","avril"),
        ("mai","mai"),
        ("juin","juin"),
        ("juillet","juillet"),
        ("aout","aout"),
        ("septembre","septembre"),
        ("octobre","octobre"),
        ("novembre","novembre"),
        ("decembre","decembre"),

    ]
    
    mois = forms.ChoiceField(choices=mois_choix,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

   
    montant = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )
DEGRES = [('0','négligeable'),('1','utile'),('2','important')]
class form_comment(forms.Form):
    commentaire = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder':'Commentaire',
            'class':'form-control'
        })
    )
    degré = ChoiceField(widget=RadioSelect, choices=DEGRES, required= True)
