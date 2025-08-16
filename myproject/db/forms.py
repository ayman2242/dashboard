from django import forms
from .models import School, TeacherAuthorization, DirectorAuthorization,CustomUser
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserForm(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'nni', 'phone', 'group']
        help_texts = {  # remove all default help_text
            'username': None,
            'password1': None,
            'password2': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ['id','codeLR','lienQR' ,'dateAjout','code','pdf_file','qr_file']
    widgets = {
        'diplome' : forms.TextInput(attrs={'class':'form-control'}),    
        'dateLettreWaly': forms.TextInput(attrs={'class':'form-control'}),
        'numLettreWaly': forms.TextInput(attrs={'class':'form-control'}),
        'numTel': forms.TextInput(attrs={'class':'form-control'}),
        'nomMoughatta': forms.TextInput(attrs={'class':'form-control'}),
        'idMoughatta': forms.TextInput(attrs={'class':'form-control'}),
        'wilaya': forms.TextInput(attrs={'class':'form-control'}),
        'nni': forms.TextInput(attrs={'class':'form-control'}),
        'nom': forms.TextInput(attrs={'class':'form-control'}),
        'nationalite': forms.TextInput(attrs={'class':'form-control'}),
        'niveau': forms.TextInput(attrs={'class':'form-control'}),
    }


class TeacherAuthorizationForm(forms.ModelForm):
    
    class Meta:
        model = TeacherAuthorization
        exclude = ['id','user','qr_code','is_active','dateAjout','codeAE','pdf_file']

    widgets = {
        'school' : forms.TextInput(attrs={'class':'form-control'}),
        'degree' : forms.TextInput(attrs={'class':'form-control'}),
        'matierEnseigner' : forms.TextInput(attrs={'class':'form-control'}),
        'sourceDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'numDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'specialiteDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'niveauDiplom' : forms.TextInput(attrs={'class':'form-control'}),
        'lieuNai' : forms.TextInput(attrs={'class':'form-control'}),
        'dateNais' : forms.TextInput(attrs={'class':'form-control'}),
        'nni' : forms.TextInput(attrs={'class':'form-control'}),
        'nom' : forms.TextInput(attrs={'class':'form-control'}),
        'code' : forms.TextInput(attrs={'class':'form-control'}),
        'dateDebut' : forms.TextInput(attrs={'class':'form-control'}),
        'dateFin' : forms.TextInput(attrs={'class':'form-control'}),

    }

class DirectorAuthorizationForm(forms.ModelForm):

    class Meta:
        model = DirectorAuthorization
        exclude = ['id','user','lienQR','dateAjout','pdf_file','codeAD']

    widgets = {
        'school' : forms.TextInput(attrs={'class':'form-control'}),
        'noter' : forms.TextInput(attrs={'class':'form-control'}),
        'dateAutorisationNoter' : forms.TextInput(attrs={'class':'form-control'}),
        'numAutorisationNoter' : forms.TextInput(attrs={'class':'form-control'}),
        'numTel' : forms.TextInput(attrs={'class':'form-control'}),
        'nomMoughatta' : forms.TextInput(attrs={'class':'form-control'}),
        'idMoughatta' : forms.TextInput(attrs={'class':'form-control'}),
        'wilaya' : forms.TextInput(attrs={'class':'form-control'}),
        'dateAutorisation' : forms.TextInput(attrs={'class':'form-control'}),
        'autorisationNum' : forms.TextInput(attrs={'class':'form-control'}),
        'nomEcole' : forms.TextInput(attrs={'class':'form-control'}),
        'sourceDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'numDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'specialiteDiplome' : forms.TextInput(attrs={'class':'form-control'}),
        'niveauDiplom' : forms.TextInput(attrs={'class':'form-control'}),
        'lieuNai' : forms.TextInput(attrs={'class':'form-control'}),
        'dateNais' : forms.TextInput(attrs={'class':'form-control'}),
        'nni' : forms.TextInput(attrs={'class':'form-control'}),
        'nom' : forms.TextInput(attrs={'class':'form-control'}),
        'dateDebut' : forms.TextInput(attrs={'class':'form-control'}),
        'dateFin' : forms.TextInput(attrs={'class':'form-control'}),
        
    }

