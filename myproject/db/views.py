import os
from django.conf import settings
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from io import BytesIO
import qrcode
from .forms import LoginForm ,DirectorAuthorizationForm,SchoolForm,TeacherAuthorizationForm
from fpdf import FPDF
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .models import DirectorAuthorization,School
from django.utils.timezone import now
from .utils.pdf_utils import fill_pdf
from datetime import date



# Create your views here.
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username , password= password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                form.add_error(None, "incalid username or password")
    else:
        form = LoginForm()

    return render(request,'login.html',{'form':form})


@login_required(login_url='/login/')
def school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            # 1️⃣ Create instance
            instance = form.save(commit=False)
            instance.user = request.user
            instance.dateAjout= date.today()
            # 2️⃣ Generate unique codeLR
            year = str(now().year)[-2:]
            last_school = School.objects.filter(codeLR__startswith=f'DEPLR{year}').order_by('id').last()
            number = int(last_school.codeLR[-6:]) + 1 if last_school else 1
            instance.codeLR = f'DEPLR{year}{number:06d}'
  
            # 3️⃣ Temporary save to get instance.id
            instance.lienQR = "temp"
            instance.save()

            # 4️⃣ Generate final QR link
            qr_link = f"http://127.0.0.1:8000/director/{instance.id}/"
            instance.lienQR = qr_link

            # 5️⃣ Generate QR code PNG
            qr_img = qrcode.make(qr_link)

            # 6️⃣ Save QR to a temporary file
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr")
            os.makedirs(temp_dir, exist_ok=True)
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeLR)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)



            # 8️⃣ Generate PDF with QR inserted
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeLR]": instance.codeLR,
                "[date]": instance.dateLettreWaly.strftime("%d/%m/%Y"),
                "[QR]": "[QR]"  # Placeholder in PDF template
            }

            pdf_path = fill_pdf(
                "template.pdf",
                f"{instance.codeLR}.pdf",
                pdf_replacements,
                qr_image_path=qr_path  # ✅ pass the actual QR PNG path
            )

            # 9️⃣ Save PDF to model
            with open(pdf_path, 'rb') as f:
                instance.pdf_file.save(f"{instance.codeLR}.pdf", File(f), save=False)

            #  🔟 Final save
            instance.save()

            return redirect("home")
        else:
            return render(request, 'lettre.html', {'form': form})

    else:
        form = SchoolForm()

    return render(request, 'lettre.html', {'form': form})


@login_required(login_url='/login/')    
def director_autor(request):
    if request.method == "POST":
        form = DirectorAuthorizationForm(request.POST)
        if form.is_valid():
            # ===== 1️⃣ حفظ مؤقت للسجل لتجنب IntegrityError =====
            instance = form.save(commit=False)
            instance.user = request.user
            instance.lienQR = "temp"  # قيمة مؤقتة
            instance.save()  # الآن لدينا instance.id

            # ===== 2️⃣ إنشاء الرابط النهائي للـ QR =====
            qr_link = f"http://127.0.0.1:8000/director/{instance.id}/"
            instance.lienQR = qr_link

            # ===== 3️⃣ إنشاء QR Code =====
            qr_img = qrcode.make(qr_link)

            # ===== 4️⃣ تجهيز المجلد المؤقت وحفظ QR =====
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr")
            os.makedirs(temp_dir, exist_ok=True)

            # تنظيف اسم الملف لتجنب الأحرف غير الصالحة
            safe_autorisationNum = re.sub(r'[^0-9a-zA-Z]+', '_', instance.autorisationNum)
            qr_filename = f"{safe_autorisationNum}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # ===== 5️⃣ إنشاء PDF وإدراج QR =====
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(200, 10, txt="Director Authorization", ln=True, align="C")
            pdf.ln(10)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Authorization Number: {instance.autorisationNum}", ln=True)
            pdf.cell(200, 10, txt=f"School: {instance.school}", ln=True)
            pdf.cell(200, 10, txt=f"Start Date: {instance.dateDebut}", ln=True)
            pdf.cell(200, 10, txt=f"End Date: {instance.dateFin}", ln=True)
            pdf.cell(200, 10, txt=f"User: {instance.user.username}", ln=True)

            # إدراج صورة QR داخل PDF
            pdf.image(qr_path, x=80, y=80, w=50, h=50)

            # حفظ PDF في FileField
            pdf_io = BytesIO()
            pdf_io.write(pdf.output(dest="S").encode("latin-1"))
            pdf_filename = f"{safe_autorisationNum}.pdf"
            instance.pdf_file.save(pdf_filename, ContentFile(pdf_io.getvalue()), save=False)

            # ===== 6️⃣ الحفظ النهائي =====
            instance.save()

            # ===== 7️⃣ (اختياري) حذف الملف المؤقت =====
            # os.remove(qr_path)

            return redirect("home")  # عدّل لصفحة النجاح

    else:   
        form = DirectorAuthorizationForm()
    return  render(request,"directeur.html", {'form':form})






def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,"home.html")
