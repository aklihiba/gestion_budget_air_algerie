from django import forms

from cadre_bud.models import Pos6, monnaie, profile, unite_1


class form_edit_user(forms.Form):
    types = [
        ("sd","sd"),
        ("cdd","cdd"),
        ("cadre_bud","cadre_bud"),

    ]
    
    type_u = forms.ChoiceField(choices=types,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

   
    nom = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    
    prenom = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    user_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    
    password = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'*****'
        })
        )
    
    password2 = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder':'*****'
        })
        )

class form_unite(forms.Form):

    code = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    
    reseau = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    pays = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "placeholder":"",
            "aria-label":"Name"
        })
    )

    
    monnaies = forms.ModelChoiceField(queryset=monnaie.objects.all(),widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

    c = [
        ("Y","Y"),
        ("N","N"),

    ]
    
    comercial = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))



    
    etranger = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

    tresorie = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

    trafic = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

    emission = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

    recette = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    exploitation = forms.ChoiceField(choices=c,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

class form_compte(forms.Form):
    scf = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class":"form-control",
            "aria-label":"Name"
        })
    )
 
    lib = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class":"form-control",
            "aria-label":"Name"
        })
    )


class form_unite_user(forms.Form):

    profile = forms.ModelChoiceField(queryset=profile.objects.all(),widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    unite = forms.ModelChoiceField(queryset=unite_1.objects.all(),widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

class form_unite_pos(forms.Form):
    r = Pos6.objects.all() 
    for i in r:
                if not (i.type =="FONCTIONNEMENT" or i.type =="EXPLOITATION"):
                    r = r.exclude(id=i.id)

    compte = forms.ModelChoiceField(queryset=r,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    unite = forms.ModelChoiceField(queryset=unite_1.objects.all(),widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))
    types = [
        ("FONCTIONNEMENT","FONCTIONNEMENT"),
        ("EXEPLOITATION","EXEPLOITATION"),

    ]
    type  = forms.ChoiceField(choices=types,widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ))

   
    
