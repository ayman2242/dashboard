from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


MOUGHATAA_CHOICES = [
    ('adel_bagrou', 'Adel Bagrou'),
    ('aïoun', 'Aïoun'),
    ('akjoujt', 'Akjoujt'),
    ('aleg', 'Aleg'),
    ('amourj', 'Amourj'),
    ('aoujeft', 'Aoujeft'),
    ('arafat', 'Arafat'),
    ('atar', 'Atar'),
    ('bababé', 'Bababé'),
    ('barkéol', 'Barkéol'),
    ('bassiknou', 'Bassiknou'),
    ('bénichab', 'Bénichab'),
    ('bir_moghreïn', 'Bir Moghreïn'),
    ('bogué', 'Bogué'),
    ('boumdeid', 'Boumdeid'),
    ('boutilimit', 'Boutilimit'),
    ('chami', 'Chami'),
    ('chinguetti', 'Chinguetti'),
    ('dar_naïm', 'Dar Naïm'),
    ('djigueni', 'Djigueni'),
    ('el_mina', 'El Mina'),
    ('f_deírick', "F'Déirick"),
    ('ghabou', 'Ghabou'),
    ('guérou', 'Guérou'),
    ('kaédi', 'Kaédi'),
    ('kankossa', 'Kankossa'),
    ('keur_macène', 'Keur Macène'),
    ('kiffa', 'Kiffa'),
    ('koubenni', 'Koubenni'),
    ('ksar', 'Ksar'),
    ('lexeiba', 'Lexeiba'),
    ('m_bagne', "M'Bagne"),
    ('m_bout', "M'Bout"),
    ('maghama', 'Maghama'),
    ('magta_lahjar', 'Magta Lahjar'),
    ('male', 'Male'),
    ('méderdra', 'Méderdra'),
    ('monguel', 'Monguel'),
    ('moudjéria', 'Moudjéria'),
    ('n_beiket_lehwach', "N'Beiket Lehwach"),
    ('néma', 'Néma'),
    ('nouadhibou', 'Nouadhibou'),
    ('ouad_naga', 'Ouad Naga'),
    ('ouadane', 'Ouadane'),
    ('oualata', 'Oualata'),
    ('ould_yengé', "Ould Yengé"),
    ('r_kiz', "R'Kiz"),
    ('riyad', 'Riyad'),
    ('rosso', 'Rosso'),
    ('sebkha', 'Sebkha'),
    ('sélibaby', 'Sélibaby'),
    ('tamchekett', 'Tamchekett'),
    ('tékane', 'Tékane'),
    ('tevragh_zeina', 'Tevragh Zeina'),
    ('teyarett', 'Teyarett'),
    ('tichitt', 'Tichitt'),
    ('tidjikja', 'Tidjikja'),
    ('timbédra', 'Timbédra'),
    ('tintane', 'Tintane'),
    ('touil', 'Touil'),
    ('toujounine', 'Toujounine'),
    ('wompou', 'Wompou'),
    ('zouérate', 'Zouérate'),
]

WILAYA_CHOICES = [
    ('adrar', 'Adrar'),
    ('assaba', 'Assaba'),
    ('brakna', 'Brakna'),
    ('dakhlet_nouadhibou', 'Dakhlet Nouadhibou'),
    ('gorgol', 'Gorgol'),
    ('guidimakha', 'Guidimakha'),
    ('hodh_charghi', 'Hodh Charghi'),
    ('hodh_gharb', 'Hodh Gharbi'),
    ('inchiri', 'Inchiri'),
    ('nouakchott_nord', 'Nouakchott Nord'),
    ('nouakchott_ouest', 'Nouakchott Ouest'),
    ('nouakchott_sud', 'Nouakchott Sud'),
    ('tagant', 'Tagant'),
    ('tiris_zemmour', 'Tiris Zemmour'),
    ('trarza', 'Trarza'),
]


class CustomUser(AbstractUser):
    nni = models.CharField(max_length=20, blank=True, null=True, verbose_name="National ID")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",    
        related_query_name="customuser",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",   
        related_query_name="customuser",
        blank=False,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    

class School(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True)
    diplome = models.CharField(max_length=50,null=True)
    dateLettreWaly = models.DateField()
    numLettreWaly = models.CharField(max_length=50,null= True)
    numTel =models.CharField(max_length=50,null=True)
    nomMoughatta = models.CharField(max_length=50,choices=MOUGHATAA_CHOICES,default="N/A")
    idMoughatta = models.IntegerField(null= True)
    wilaya =  models.CharField(max_length=50,choices=WILAYA_CHOICES,null=True)
    nomEcole =models.CharField(max_length=50,null=True)
    code = models.CharField(max_length=20,null=True)
    nni = models.CharField(max_length=50,null=True)
    nom =  models.CharField(max_length=50,null=True)
    codeLR =   models.CharField(max_length=50,null=True)
    lienQR =   models.CharField(max_length=200,null=True)
    nationalite =   models.CharField(max_length=50,null=True)
    niveau = models.CharField(max_length=50,default="N/A")
    pdf_file = models.FileField(upload_to='generated_pdfs/', null=True, blank=True)
    dateAjout = models.DateField()



    def __str__(self):
        return self.nom

class DirectorAuthorization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    school = models.ForeignKey(
    School,
    on_delete=models.CASCADE,
    related_name='director_authorizations')   
    id = models.AutoField(primary_key=True)
    noter = models.CharField(max_length=50,default="N/A")
    dateAutorisationNoter = models.DateField()
    numAutorisationNoter = models.CharField(max_length=50,default="N/A")
    numTel = models.CharField(max_length=50,default="N/A")  
    nomMoughatta = models.CharField(max_length=50,choices=MOUGHATAA_CHOICES,default="N/A")
    idMoughatta = models.IntegerField(null= True)
    wilaya =models.CharField(max_length=50,choices=WILAYA_CHOICES,default="N/A")
    dateAutorisation=models.DateField()
    autorisationNum = models.CharField(max_length=50,default="N/A")
    sourceDiplome =  models.CharField(max_length=50,default="N/A")
    numDiplome =  models.CharField(max_length=50,default="N/A")
    specialiteDiplome =  models.CharField(max_length=50,default="N/A")
    niveauDiplom =  models.CharField(max_length=50,default="N/A")
    lieuNai =  models.CharField(max_length=50,default="N/A")
    dateNais=models.DateField()
    nni =  models.CharField(max_length=50,default="N/A")
    nom =  models.CharField(max_length=50,default="N/A")
    codeAD = models.CharField(max_length=50,default="N/A")
    lienQR = models.URLField(blank=True, null=True)
    pdf_file = models.ImageField(upload_to='pdfs/', blank=True, null=True)  
    typeAutorisationDirige = models.CharField(max_length=200,default="N/A", null=False)
    dateAjout = models.DateField()
    dateDebut = models.DateField()
    dateFin = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.nomEcole}"

class TeacherAuthorization(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_authorizations')
    degree = models.CharField(max_length=50,blank=True,null=True)
    matierEnseigner = models.CharField(max_length=50,blank=True,null=True)
    sourceDiplome = models.CharField(max_length=50,blank=True,null=True)
    numDiplome = models.CharField(max_length=50,blank=True,null=True)
    specialiteDiplome =models.CharField(max_length=50,blank=True,null=True)
    niveauDiplom = models.CharField(max_length=50,blank=True,null=True)
    lieuNai =models.CharField(max_length=50,blank=True,null=True)
    dateNais =models.CharField(max_length=50,blank=True,null=True)
    nni=models.CharField(max_length=50,blank=True,null=True)
    nom=models.CharField(max_length=50,blank=True,null=True)
    code=models.CharField(max_length=50,blank=True,null=True)
    codeAE =models.CharField(max_length=50,blank=True,null=True)
    qr_code = models.CharField(max_length=50, blank=True, null=True) 
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True)  
    dateAjout = models.DateField()
    dateDebut = models.DateField()
    dateFin = models.DateField()
    is_active = models.BooleanField(default=True) #and this also

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialiteDiplome}"
    

