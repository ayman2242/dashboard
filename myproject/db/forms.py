from django import forms
from .models import School, TeacherAuthorization, DirectorAuthorization,CustomUser
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'nni', 'phone', 'groups']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserEditForm(UserChangeForm):
    password = None  # hide password field when editing

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'nni', 'phone', 'groups']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple(),  # multiple groups ✅
        }




class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        # Exclude auto-managed fields
        exclude = ['id','user','codeLR','lienQR','dateAjout','pdf_file','qr_file']

        widgets = {
            'diplome': forms.TextInput(attrs={'class': 'form-control'}),
            'dateLettreWaly': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'numLettreWaly': forms.TextInput(attrs={'class': 'form-control'}),
            'numTel': forms.TextInput(attrs={'class': 'form-control'}),
            'idMoughatta': forms.TextInput(attrs={'class': 'form-control'}),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # Fix date field for HTML5 input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and getattr(self.instance, 'dateLettreWaly'):
            self.fields['dateLettreWaly'].initial = getattr(self.instance, 'dateLettreWaly').strftime('%Y-%m-%d')

class TeacherAuthorizationForm(forms.ModelForm):

    class Meta:
        model = TeacherAuthorization
        # Exclude fields that are auto-managed
        exclude = ['id','user','qr_code','is_active','dateAjout','codeAE','pdf_file']

        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'matierEnseigner': forms.TextInput(attrs={'class': 'form-control'}),
            'sourceDiplome': forms.TextInput(attrs={'class': 'form-control'}),
            'numDiplome': forms.TextInput(attrs={'class': 'form-control'}),
            'specialiteDiplome': forms.TextInput(attrs={'class': 'form-control'}),
            'niveauDiplom': forms.TextInput(attrs={'class': 'form-control'}),
            'lieuNai': forms.TextInput(attrs={'class': 'form-control'}),
            'dateNais': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'nni': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'dateDebut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'dateFin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }

    # Fix date fields for HTML5 input
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['dateNais', 'dateDebut', 'dateFin']:
            if self.instance and getattr(self.instance, field):
                self.fields[field].initial = getattr(self.instance, field).strftime('%Y-%m-%d')



class DirectorAuthorizationForm(forms.ModelForm):

    class Meta:
        model = DirectorAuthorization
        exclude = ['id','user','lienQR','dateAjout','pdf_file','codeAD']

        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'noter' : forms.TextInput(attrs={'class':'form-control'}),
            'dateAutorisationNoter' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'numAutorisationNoter' : forms.TextInput(attrs={'class':'form-control'}),
            'numTel' : forms.TextInput(attrs={'class':'form-control'}),
            'idMoughatta' : forms.TextInput(attrs={'class':'form-control'}),
            'dateAutorisation' :forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'autorisationNum' : forms.TextInput(attrs={'class':'form-control'}),
            'sourceDiplome' : forms.TextInput(attrs={'class':'form-control'}),
            'numDiplome' : forms.TextInput(attrs={'class':'form-control'}),
            'specialiteDiplome' : forms.TextInput(attrs={'class':'form-control'}),
            'niveauDiplom' : forms.TextInput(attrs={'class':'form-control'}),
            'lieuNai' : forms.TextInput(attrs={'class':'form-control'}), 

            'dateNais' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'dateDebut' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'dateFin' : forms.DateInput(attrs={'class':'form-control', 'type':'date'}),

            'nni' : forms.TextInput(attrs={'class':'form-control'}),
            'nom' : forms.TextInput(attrs={'class':'form-control'}),
        }
    




