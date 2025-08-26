from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
import uuid


# -----------------------------
# CHOICES
# -----------------------------
MOUGHATAA_CHOICES = [
    ('عادل بغرو', 'عادل بغرو'),
    ('العيون', 'العيون'),
    ('أكجوجت', 'أكجوجت'),
    ('أليج', 'أليج'),
    ('أمُّرج', 'أمُّرج'),
    ('أوجفت', 'أوجفت'),
    ('عرفات', 'عرفات'),
    ('أتار', 'أتار'),
    ('بابابي', 'بابابي'),
    ('باركيول', 'باركيول'),
    ('باسيكنو', 'باسيكنو'),
    ('بنيشاب', 'بنيشاب'),
    ('بير مغرين', 'بير مغرين'),
    ('بوغي', 'بوغي'),
    ('بومديد', 'بومديد'),
    ('بوتيليمت', 'بوتيليمت'),
    ('شامي', 'شامي'),
    ('شنقيطي', 'شنقيطي'),
    ('دار النعيم', 'دار النعيم'),
    ('جيغني', 'جيغني'),
    ('الميناء', 'الميناء'),
    ("ف ديريك", "ف ديريك"),
    ('غابو', 'غابو'),
    ('غيرو', 'غيرو'),
    ('كيدي', 'كيدي'),
    ('كنكوصة', 'كنكوصة'),
    ('كير ماسين', 'كير ماسين'),
    ('كيفة', 'كيفة'),
    ('كوبني', 'كوبني'),
    ('قصر', 'قصر'),
    ('ليكسيبا', 'ليكسيبا'),
    ("م باني", "م باني"),
    ("م بوت", "م بوت"),
    ('ماقاما', 'ماقاما'),
    ('مقتى لحجار', 'مقتى لحجار'),
    ('مال', 'مال'),
    ('ميدردرا', 'ميدردرا'),
    ('مونغيل', 'مونغيل'),
    ('مجرية', 'مجرية'),
    ("ن بيكيت لهواش", "ن بيكيت لهواش"),
    ('نيما', 'نيما'),
    ('نواذيبو', 'نواذيبو'),
    ('واد ناغا', 'واد ناغا'),
    ('ودان', 'ودان'),
    ('والاتا', 'والاتا'),
    ("ولد ينجى", "ولد ينجى"),
    ("ر كيز", "ر كيز"),
    ('رياض', 'رياض'),
    ('روصو', 'روصو'),
    ('سبخة', 'سبخة'),
    ('سليبابي', 'سليبابي'),
    ('تامشكيت', 'تامشكيت'),
    ('تيكان', 'تيكان'),
    ('تفرغ زينة', 'تفرغ زينة'),
    ('تيارت', 'تيارت'),
    ('تيشيت', 'تيشيت'),
    ('تيدجيكجا', 'تيدجيكجا'),
    ('تيمبدرا', 'تيمبدرا'),
    ('تنطان', 'تنطان'),
    ('تويل', 'تويل'),
    ('توجونين', 'توجونين'),
    ('ومبو', 'ومبو'),
    ('زويرات', 'زويرات'),
]

WILAYA_CHOICES = [
    ('أدرار', 'أدرار'),
    ('عصابة', 'عصابة'),
    ('براكنة', 'براكنة'),
    ('داخل نواذيبو', 'داخل نواذيبو'),
    ('غورغول', 'غورغول'),
    ('كيدي ماغا', 'كيدي ماغا'),
    ('الحوض الشرقي', 'الحوض الشرقي'),
    ('الحوض الغربي', 'الحوض الغربي'),
    ('إنشيري', 'إنشيري'),
    ('نواكشوط الشمالية', 'نواكشوط الشمالية'),
    ('نواكشوط الغربية', 'نواكشوط الغربية'),
    ('نواكشوط الجنوبية', 'نواكشوط الجنوبية'),
    ('تكانت', 'تكانت'),
    ('تيرس زمور', 'تيرس زمور'),
    ('ترارزة', 'ترارزة'),
]



# -----------------------------
# USER
# -----------------------------
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    nni = models.CharField(
        max_length=20, blank=True, null=True, verbose_name=_("Numéro National d'Identité")
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Téléphone"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Adresse e-mail"))

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        help_text=_("Groupes auxquels appartient cet utilisateur."),
        verbose_name=_("Groupes"),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        related_query_name="customuser",
        blank=True,
        help_text=_("Permissions spécifiques de cet utilisateur."),
        verbose_name=_("Permissions utilisateur"),
    )

    # For login attempt tracking
    failed_login_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    lockout_time = models.DateTimeField(null=True, blank=True)  # New field


    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")


# -----------------------------
# ECOLE 13
# -----------------------------
class School(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name="Utilisateur")
    
    nomEcole = models.CharField(max_length=50, null=True, verbose_name="Nom de l'école")
    code = models.CharField(max_length=20, null=True, verbose_name="Code école")
    niveau = models.CharField(max_length=50, default="N/A", verbose_name="Niveau scolaire")
    nomMoughatta = models.CharField(max_length=50, choices=MOUGHATAA_CHOICES, default="N/A", verbose_name="Moughataa")
    idMoughatta = models.IntegerField(null=True, verbose_name="ID Moughataa")
    wilaya = models.CharField(max_length=50, choices=WILAYA_CHOICES, null=True, verbose_name="Wilaya")
    numTel = models.CharField(max_length=50, null=True, verbose_name="Téléphone")
    nni = models.CharField(max_length=50, null=True, verbose_name="NNI")
    nom = models.CharField(max_length=50, null=True, verbose_name="Nom")
    nationalite = models.CharField(max_length=50, null=True, verbose_name="Nationalité")
    diplome = models.CharField(max_length=50, null=True, verbose_name="Diplôme")
    dateLettreWaly = models.DateField(verbose_name="Date de la lettre Waly")
    numLettreWaly = models.CharField(max_length=50, null=True, verbose_name="Numéro de la lettre Waly")
    qr_uuid = models.UUIDField(default=uuid.uuid4,editable=False, unique=True)

    codeLR = models.CharField(max_length=50, null=True, verbose_name="Code LR")
    lienQR = models.CharField(max_length=200, null=True, verbose_name="Lien QR")
    pdf_file = models.FileField(upload_to='generated_pdfs/', null=True, blank=True, verbose_name="Fichier PDF")
    dateAjout = models.DateField(verbose_name="Date d'ajout")

    def __str__(self):
        return self.nom or "École"


# -----------------------------
# DIRECTEUR 21
# -----------------------------
class DirectorAuthorization(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur")
    nom = models.CharField(max_length=50, default="N/A", verbose_name="Nom complet")
    nni = models.CharField(max_length=50, default="N/A", verbose_name="NNI")
    lieuNai = models.CharField(max_length=50, default="N/A", verbose_name="Lieu de naissance")
    dateNais = models.DateField(verbose_name="Date de naissance")
    sourceDiplome = models.CharField(max_length=50, default="N/A", verbose_name="Source du diplôme")
    numDiplome = models.CharField(max_length=50, default="N/A", verbose_name="Numéro du diplôme")
    specialiteDiplome = models.CharField(max_length=50, default="N/A", verbose_name="Spécialité du diplôme")
    niveauDiplom = models.CharField(max_length=50, default="N/A", verbose_name="Niveau du diplôme")
    typeAutorisationDirige = models.CharField(max_length=200, default="N/A", verbose_name="Type d'autorisation")
    dateAutorisation = models.DateField(verbose_name="Date d'autorisation")
    autorisationNum = models.CharField(max_length=50, default="N/A", verbose_name="Numéro d'autorisation")
    dateDebut = models.DateField(verbose_name="Date de début")
    dateFin = models.DateField(verbose_name="Date de fin")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='director_authorizations', verbose_name="École")

    numTel = models.CharField(max_length=50, default="N/A", verbose_name="Téléphone")
    nomMoughatta = models.CharField(max_length=50, choices=MOUGHATAA_CHOICES, default="N/A", verbose_name="Moughataa")
    wilaya = models.CharField(max_length=50, choices=WILAYA_CHOICES, default="N/A", verbose_name="Wilaya")
    idMoughatta = models.IntegerField(null=True, verbose_name="ID Moughataa")


    noter = models.CharField(max_length=50, default="N/A", verbose_name="Notaire")
    dateAutorisationNoter = models.DateField(verbose_name="Date de l'autorisation notaire")
    numAutorisationNoter = models.CharField(max_length=50, default="N/A", verbose_name="Numéro d'autorisation notaire")

    codeAD = models.CharField(max_length=50, default="N/A", verbose_name="Code AD")
    lienQR = models.URLField(blank=True, null=True, verbose_name="Lien QR")
    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Fichier PDF")
    dateAjout = models.DateField(verbose_name="Date d'ajout")
    qr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)


    def __str__(self):
        return f"{self.user.get_full_name()} - {self.school.nomEcole}"


# -----------------------------
# ENSEIGNANT 14
# -----------------------------
class TeacherAuthorization(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Utilisateur")
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teacher_authorizations', verbose_name="École")

    degree = models.CharField(max_length=50, blank=True, null=True, verbose_name="Diplôme")
    matierEnseigner = models.CharField(max_length=50, blank=True, null=True, verbose_name="Matière enseignée")
    sourceDiplome = models.CharField(max_length=50, blank=True, null=True, verbose_name="Source du diplôme")
    numDiplome = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro du diplôme")
    specialiteDiplome = models.CharField(max_length=50, blank=True, null=True, verbose_name="Spécialité du diplôme")
    niveauDiplom = models.CharField(max_length=50, blank=True, null=True, verbose_name="Niveau du diplôme")

    lieuNai = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lieu de naissance")
    dateNais = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    nni = models.CharField(max_length=50, blank=True, null=True, verbose_name="NNI")
    nom = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom complet")

    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code")
    codeAE = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code AE")
    qr_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code QR")

    pdf_file = models.FileField(upload_to='pdfs/', blank=True, null=True, verbose_name="Fichier PDF")

    dateAjout = models.DateField(verbose_name="Date d'ajout")
    dateDebut = models.DateField(verbose_name="Date de début")
    dateFin = models.DateField(verbose_name="Date de fin")

    is_active = models.BooleanField(default=True, verbose_name="Actif")
    qr_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialiteDiplome or 'N/A'}"
