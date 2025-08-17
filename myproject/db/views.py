import os
from django.conf import settings
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from io import BytesIO
import qrcode
from .forms import LoginForm ,DirectorAuthorizationForm,SchoolForm,TeacherAuthorizationForm,UserForm
from fpdf import FPDF
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .models import DirectorAuthorization,School,TeacherAuthorization
from django.utils.timezone import now
from .utils.pdf_utils import fill_pdf
from datetime import date
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect





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
    if not request.user.groups.filter(name="Schools").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")  
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
            qr_link = f"http://127.0.0.1:8000/lettre/{instance.id}/"
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

            return redirect('success_school', school_id=instance.id)
        else:
            return render(request, 'lettre.html', {'form': form})

    else:
        form = SchoolForm()

    return render(request, 'lettre.html', {'form': form})


@login_required(login_url='/login/')    
def director_autor(request):
    if not request.user.groups.filter(name="Director").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")  
    if request.method == "POST":
        form = DirectorAuthorizationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.user = request.user
            instance.dateAjout= date.today()
            year = str(now().year)[-2:]
            last_director = DirectorAuthorization.objects.filter(
             codeAD__startswith=f'DEPAD{year}'
            ).order_by('id').last()
            number = int(last_director.codeAD[-6:]) + 1 if last_director else 1
            instance.codeAD = f'DEPAD{year}{number:06d}'

            instance.lienQR = "temp"
            instance.save()
            qr_link = f"http://127.0.0.1:8000/director/{instance.id}/"
            instance.lienQR = qr_link

            # 5️⃣ Generate QR code PNG
            qr_img = qrcode.make(qr_link)

            # 6️⃣ Save QR to a temporary file
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr1")
            os.makedirs(temp_dir, exist_ok=True)
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAD)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)



            # 8️⃣ Generate PDF with QR inserted
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeLR]": instance.codeAD,
                "[date]": instance.dateAutorisationNoter,
                "[QR]": "[QR]"  # Placeholder in PDF template
            }

            pdf_path = fill_pdf(
                "template.pdf",
                f"{instance.codeAD}.pdf",
                pdf_replacements,
                qr_image_path=qr_path  # ✅ pass the actual QR PNG path
            )

            # 9️⃣ Save PDF to model
            with open(pdf_path, 'rb') as f:
                instance.pdf_file.save(f"{instance.codeAD}.pdf", File(f), save=False)

            #  🔟 Final save
            instance.save()

            return redirect('success_director', director_id=instance.id)
        else:
            return render(request, 'succes.html', {'form': form})


    else:   
        form = DirectorAuthorizationForm()
    return  render(request,"directeur.html", {'form':form})

@login_required(login_url='/login/')    
def teacher_autor(request):
    if not request.user.groups.filter(name="Teacher").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    if request.method == "POST":
        form = TeacherAuthorizationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.user = request.user
            instance.dateAjout = date.today()

            # 1️⃣ Generate unique codeAE
            year = str(now().year)[-2:]
            last_teacher = TeacherAuthorization.objects.filter(
                codeAE__startswith=f'DEPAE{year}'
            ).order_by('id').last()
            number = int(last_teacher.codeAE[-6:]) + 1 if last_teacher else 1
            instance.codeAE = f'DEPAE{year}{number:06d}'

            # 2️⃣ Temporary save
            instance.lienQR = "temp"
            instance.save()

            # 3️⃣ Generate QR link
            qr_link = f"http://127.0.0.1:8000/teacher/{instance.id}/"
            instance.lienQR = qr_link

            # 4️⃣ Generate QR code PNG
            qr_img = qrcode.make(qr_link)

            # 5️⃣ Save QR to a temporary file
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr2")
            os.makedirs(temp_dir, exist_ok=True)
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAE)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # 6️⃣ Generate PDF with QR inserted
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeAE]": instance.codeAE,
                "[date]": instance.dateDebut.strftime("%d/%m/%Y") if instance.dateDebut else "",
                "[QR]": "[QR]"  # Placeholder in PDF template
            }

            pdf_path = fill_pdf(
                "template.pdf",
                f"{instance.codeAE}.pdf",
                pdf_replacements,
                qr_image_path=qr_path
            )

            # 7️⃣ Save PDF to model
            with open(pdf_path, 'rb') as f:
                instance.pdf_file.save(f"{instance.codeAE}.pdf", File(f), save=False)

            # 8️⃣ Final save
            instance.save()

            return redirect('success_teacher', teacher_id=instance.id)
        else:
            return render(request, 'succes.html', {'form': form})

    else:   
        form = TeacherAuthorizationForm()
    return render(request, "teacher.html", {'form': form})



@login_required(login_url='/login/')
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # password is already hashed by UserCreationForm
            user.save()

            # Assign selected group
            group = form.cleaned_data['group']
            user.groups.add(group)

            return redirect('success')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})


def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,"home.html")



@login_required
def success(request, school_id=None, director_id=None, teacher_id=None):
    context = {}

    if school_id:
        school = get_object_or_404(School, id=school_id)
        if school.user != request.user:  # redirect if not the owner
            return redirect('home')
        context['school'] = school

    elif director_id:
        director = get_object_or_404(DirectorAuthorization, id=director_id)
        if director.user != request.user:
            return redirect('home')
        context['director'] = director

    elif teacher_id:
        teacher = get_object_or_404(TeacherAuthorization, id=teacher_id)
        if teacher.user != request.user:
            return redirect('home')
        context['teacher'] = teacher

    else:
        # No valid ID provided
        return redirect('home')

    return render(request, 'succes.html', context)
