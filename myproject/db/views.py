import tempfile
import os
from django.conf import settings
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
import qrcode
from .forms import LoginForm ,DirectorAuthorizationForm,SchoolForm,TeacherAuthorizationForm,UserForm,UserEditForm
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from .models import DirectorAuthorization,School,TeacherAuthorization,CustomUser
from django.utils.timezone import now
from .utils.pdf_utils import fill_pdf
from datetime import date
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from datetime import timedelta
from django.utils import timezone

                    
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = timezone.timedelta(minutes=5)

def login_page(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        # Check if user is locked
        if user and user.is_locked:
            if user.lockout_time and timezone.now() < user.lockout_time + LOCKOUT_DURATION:
                remaining = (user.lockout_time + LOCKOUT_DURATION) - timezone.now()
                remaining_minutes = int(remaining.total_seconds() // 60) + 1
                messages.error(request, f"Votre compte est bloqué pour {remaining_minutes} minutes.")
                return render(request, 'login.html', {'form': form})
            else:
                # Unlock user automatically
                user.is_locked = False
                user.failed_login_attempts = 0
                user.lockout_time = None
                user.save()

        # Authenticate user
        user_auth = authenticate(request, username=username, password=password)
        if user_auth:
            # Reset failed attempts on successful login
            user.failed_login_attempts = 0
            user.is_locked = False
            user.lockout_time = None
            user.save()
            login(request, user_auth)
            return redirect('home')
        else:
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                    user.is_locked = True
                    user.lockout_time = timezone.now()
                    messages.error(request, "Trop de tentatives échouées. Votre compte est bloqué pour 5 minutes.")
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
                user.save()
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html', {'form': form})

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
            qr_link = f"{request.scheme}://{request.get_host()}/lettre/{instance.qr_uuid}/"
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
                "[codeAE]": instance.codeLR,
                "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
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
            try:
             # Remove temporary QR code
                if os.path.exists(qr_path):
                    os.remove(qr_path)
                # Remove temporary PDF
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                # Remove temp directory if empty
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as e:
                print(f"Error cleaning up files: {e}")

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
            try:
                instance = form.save(commit=False) 
                instance.user = request.user
                instance.dateAjout = date.today()
                
                # Generate codeAD
                year = str(now().year)[-2:]
                last_director = DirectorAuthorization.objects.filter(
                    codeAD__startswith=f'DEPAD{year}'
                ).order_by('id').last()
                number = int(last_director.codeAD[-6:]) + 1 if last_director else 1
                instance.codeAD = f'DEPAD{year}{number:06d}'

                # Temporary save to get ID
                instance.lienQR = "temp"
                instance.save()
                
                # Generate QR link
                # qr_link = f"http://127.0.0.1:8000/director/{instance.id}/"
                qr_link = f"{request.scheme}://{request.get_host()}/director/{instance.qr_uuid}/"
                instance.lienQR = qr_link

                # Generate QR code PNG
                qr_img = qrcode.make(qr_link)

                # Save QR to a temporary file
                temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr1")
                os.makedirs(temp_dir, exist_ok=True)
                safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAD)
                qr_filename = f"{safe_name}_qr.png"
                qr_path = os.path.join(temp_dir, qr_filename)
                qr_img.save(qr_path)

                # Generate PDF with QR inserted
                pdf_replacements = {
                    "[nom]": instance.nom,
                    "[codeAE]": instance.codeAD,
                    "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
                    "[QR]": "[QR]"
                }

                pdf_path = fill_pdf(
                    "template.pdf",
                    f"{instance.codeAD}.pdf",
                    pdf_replacements,
                    qr_image_path=qr_path
                )

                # Save PDF to model
                with open(pdf_path, 'rb') as f:
                    instance.pdf_file.save(f"{instance.codeAD}.pdf", File(f), save=False)

                # Final save
                instance.save()

                try:
                    # Clean up temporary files
                    if os.path.exists(qr_path):
                        os.remove(qr_path)
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as e:
                    print(f"Error cleaning up director files: {e}")
                
                return redirect('success_director', director_id=instance.id)
            
            except Exception as e:
                print(f"Error in director_autor view: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'directeur.html', {'form': form})
        else:
            return render(request, 'directeur.html', {'form': form})
    else:   
        form = DirectorAuthorizationForm()
    return render(request, "directeur.html", {'form': form})


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
            year = str(date.today().year)[-2:]
            last_teacher = TeacherAuthorization.objects.filter(
                codeAE__startswith=f'DEPAE{year}'
            ).order_by('id').last()
            
            if last_teacher and last_teacher.codeAE:
                try:
                    number = int(last_teacher.codeAE[-6:]) + 1
                except ValueError:
                    number = 1
            else:
                number = 1
                
            instance.codeAE = f'DEPAE{year}{number:06d}'

            # 2️⃣ Temporary save
            instance.lienQR = "temp"
            instance.save()

            # 3️⃣ Generate QR link
            qr_link = f"{request.scheme}://{request.get_host()}/teacher/{instance.qr_uuid}/"
            instance.lienQR = qr_link

            # 4️⃣ Generate QR code PNG
            qr_img = qrcode.make(qr_link)

            # 5️⃣ Save QR to a temporary file
            temp_dir = tempfile.mkdtemp()
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAE)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # 6️⃣ Generate PDF with QR inserted
            code = instance.codeAE
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeAE]": code,  # Just use the code directly
                "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
                "[QR]": "[QR]"
            }
            print("PDF replacements:", pdf_replacements)

            try:
                pdf_path = fill_pdf(
                    "template.pdf",
                    f"{instance.id}.pdf",
                    pdf_replacements,
                    qr_image_path=qr_path
                )
    
                # 7️⃣ Save PDF to model
                with open(pdf_path, 'rb') as f:
                    instance.pdf_file.save(f"{instance.id}.pdf", File(f), save=False)

                # 8️⃣ Final save
                instance.save()
                
                # Clean up temporary files
                try:
                    if os.path.exists(qr_path):
                        os.remove(qr_path)
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as e:
                    print(f"Error cleaning up teacher files: {e}")
                    
                return redirect('success_teacher', teacher_id=instance.id)
                
            except Exception as e:
                # Handle PDF generation errors
                messages.error(request, f"Error generating PDF: {str(e)}")
                # Clean up instance if PDF generation fails
                instance.delete()
                return render(request, 'teacher.html', {'form': form})
                
        else:
            # Form is not valid
            return render(request, 'teacher.html', {'form': form})

    else:   
        form = TeacherAuthorizationForm()
    
    return render(request, "teacher.html", {'form': form})



@login_required(login_url='/login/')
def add_user(request):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Assign selected groups
            groups = form.cleaned_data['groups']  # ✅ key matches the form
            user.groups.set(groups)  # use set() to assign multiple groups

            return redirect('home')
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

    obj = None
    obj_type = None

    # Get the object based on which ID is provided
    if school_id:
        obj = get_object_or_404(School, id=school_id)
        obj_type = 'school'

    elif director_id:
        obj = get_object_or_404(DirectorAuthorization, id=director_id)
        obj_type = 'director'

    elif teacher_id:
        obj = get_object_or_404(TeacherAuthorization, id=teacher_id)
        obj_type = 'teacher'

    # Redirect if no object
    if not obj:
        return redirect('home')

    # Only check user ownership if the model has a user field
    if hasattr(obj, 'user') and obj.user != request.user:
        return redirect('home')

    # Add object to context
    context['object'] = obj
    context['object_type'] = obj_type

    # Add PDF URL if available
    if hasattr(obj, 'pdf_file') and obj.pdf_file:
        context['pdf_url'] = obj.pdf_file.url

    return render(request, 'succes.html', context)


#---------------------------------- detail -----------------------------------------#

def teacher_detail(request, qr_uuid):
    teacher = get_object_or_404(TeacherAuthorization, qr_uuid=qr_uuid)
    return render(request, 'teacher_detail.html', {'teacher': teacher})

def school_detail(request, qr_uuid):
    school = get_object_or_404(School, qr_uuid=qr_uuid)
    return render(request, 'school_detail.html', {'school': school})

def director_detail(request, qr_uuid):
    director = get_object_or_404(DirectorAuthorization, qr_uuid=qr_uuid)
    return render(request, 'director_detail.html', {'director': director})



#---------------------------------- list /table-----------------------------------------#


# 1) director
def directors_list(request):
    school_count = School.objects.count()
    total_directors = DirectorAuthorization.objects.count()
    total_teachers = TeacherAuthorization.objects.count()

    if not request.user.groups.filter(name="Director").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    directors = DirectorAuthorization.objects.all()
    return render(request, 'directors_list.html', {'directors': directors,"school_count": school_count,'total_directors':total_directors,'total_teachers':total_teachers})

# 2) teacher
def teacher_list(request):
    school_count = School.objects.count()
    total_directors = DirectorAuthorization.objects.count()
    total_teachers = TeacherAuthorization.objects.count()

    if not request.user.groups.filter(name="Teacher").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    teachers = TeacherAuthorization.objects.all()
    return render(request, 'teachers_list.html', {'teachers': teachers,"school_count": school_count,'total_directors':total_directors,'total_teachers':total_teachers})

# 3) school/lettre
def school_list(request):
    school_count = School.objects.count()
    total_directors = DirectorAuthorization.objects.count()
    total_teachers = TeacherAuthorization.objects.count()

    if not request.user.groups.filter(name="Schools").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    schools = School.objects.all()
    return render(request, 'schools_list.html', {'schools': schools,"school_count": school_count,'total_directors':total_directors,'total_teachers':total_teachers})

# 4)user 
def user_list(request):
    school_count = School.objects.count()
    total_directors = DirectorAuthorization.objects.count()
    total_teachers = TeacherAuthorization.objects.count()
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")
    users = CustomUser.objects.all()
    return render(request, 'user_list.html', {'users': users,"school_count": school_count,'total_directors':total_directors,'total_teachers':total_teachers})

#---------------------------------- views -----------------------------------------#


# 1) director
def director_views(request, director_id):
    if not request.user.groups.filter(name="Director").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    director = get_object_or_404(DirectorAuthorization, id=director_id)
    return render(request, 'director_views.html', {'director': director})
# 2) teacher
def teacher_views(request, teacher_id):
    if not request.user.groups.filter(name="Teacher").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    teacher = get_object_or_404(TeacherAuthorization, id=teacher_id)
    return render(request, 'teacher_views.html', {'teacher': teacher})
# 3) school/lettre
def school_views(request, school_id):
    if not request.user.groups.filter(name="Schools").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    school= get_object_or_404(School, id=school_id)
    return render(request, 'school_views.html', {'school':school })
# 4)user 
def user_views(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")
    user= get_object_or_404(CustomUser, id=user_id)
    return render(request, 'user_views.html', {'user': user})

#---------------------------------- EDIT -----------------------------------------#

# 1) director
@login_required(login_url='/login/')
def edit_director(request, director_id):
    if not request.user.groups.filter(name="Director").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 

    director = get_object_or_404(DirectorAuthorization, id=director_id)

    if request.method == "POST":
        form = DirectorAuthorizationForm(request.POST, request.FILES, instance=director)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.dateAjout = date.today()  # optional: track edit date

            # Ensure codeAD exists (for older directors)
            if not instance.codeAD:
                year = str(now().year)[-2:]
                last_director = DirectorAuthorization.objects.filter(codeAD__startswith=f'DEPAD{year}').order_by('id').last()
                number = int(last_director.codeAD[-6:]) + 1 if last_director else 1
                instance.codeAD = f'DEPAD{year}{number:06d}'

            # Generate QR link
            qr_link = f"{request.scheme}://{request.get_host()}/director/{instance.id}/"
            instance.lienQR = qr_link

            # Generate QR code PNG
            qr_img = qrcode.make(qr_link)
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr1")
            os.makedirs(temp_dir, exist_ok=True)
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAD)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # Generate PDF with QR inserted
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeAE]": instance.codeAD,
                "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
                "[QR]": "[QR]"
            }

            try:
                pdf_path = fill_pdf(
                    "template.pdf",
                    f"{instance.codeAD}.pdf",
                    pdf_replacements,
                    qr_image_path=qr_path
                )

                # Save PDF to model
                with open(pdf_path, 'rb') as f:
                    instance.pdf_file.save(f"{instance.codeAD}.pdf", File(f), save=False)

                # Final save
                instance.save()

                # Cleanup temp files
                for path in [qr_path, pdf_path]:
                    if os.path.exists(path):
                        os.remove(path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)

                return redirect('director_detail', qr_uuid=instance.qr_uuid)

            except Exception as e:
                messages.error(request, f"Error generating PDF: {str(e)}")
                return render(request, 'edit_director.html', {'form': form, 'director': director})

        else:
            print(form.errors)
    else:
        form = DirectorAuthorizationForm(instance=director)

    return render(request, "edit_director.html", {'form': form, 'director': director})


# 2) teacher
@login_required(login_url='/login/')
def edit_teacher(request, teacher_id):
    if not request.user.groups.filter(name="Teacher").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 

    teacher = get_object_or_404(TeacherAuthorization, id=teacher_id)

    if request.method == "POST":
        form = TeacherAuthorizationForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.dateAjout = date.today()  # optional: update last edit date

            # Ensure codeAE exists (for older teachers)
            if not instance.codeAE:
                year = str(date.today().year)[-2:]
                last_teacher = TeacherAuthorization.objects.filter(codeAE__startswith=f'DEPAE{year}').order_by('id').last()
                number = int(last_teacher.codeAE[-6:]) + 1 if last_teacher and last_teacher.codeAE else 1
                instance.codeAE = f'DEPAE{year}{number:06d}'

            # Generate QR link
            qr_link = f"{request.scheme}://{request.get_host()}/teacher/{instance.id}/"
            instance.lienQR = qr_link

            # Generate QR code image
            qr_img = qrcode.make(qr_link)
            temp_dir = tempfile.mkdtemp()
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeAE)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # Generate PDF with QR inserted
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeAE]": instance.codeAE,
                "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
                "[QR]": "[QR]"
            }

            try:
                pdf_path = fill_pdf(
                    "template.pdf",
                    f"{instance.id}.pdf",
                    pdf_replacements,
                    qr_image_path=qr_path
                )

                # Save PDF to model
                with open(pdf_path, 'rb') as f:
                    instance.pdf_file.save(f"{instance.id}.pdf", File(f), save=False)

                instance.save()

                # Cleanup temporary files
                for path in [qr_path, pdf_path]:
                    if os.path.exists(path):
                        os.remove(path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)

                return redirect('teacher_detail', qr_uuid=instance.qr_uuid)

            except Exception as e:
                messages.error(request, f"Error generating PDF: {str(e)}")
                return render(request, 'edit_teacher.html', {'form': form, 'teacher': teacher})

        else:
            print(form.errors)

    else:
        form = TeacherAuthorizationForm(instance=teacher)

    return render(request, "edit_teacher.html", {'form': form, 'teacher': teacher})

# 3) school/lettre
@login_required(login_url='/login/')
def edit_school(request, school_id):
    if not request.user.groups.filter(name="Schools").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 

    school = get_object_or_404(School, id=school_id)

    if request.method == "POST":
        form = SchoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            instance = form.save(commit=False)

            # Update user and date if needed
            instance.user = request.user
            instance.dateAjout = date.today()

            # Regenerate codeLR only if needed
            if not instance.codeLR:
                year = str(now().year)[-2:]
                last_school = School.objects.filter(codeLR__startswith=f'DEPLR{year}').order_by('id').last()
                number = int(last_school.codeLR[-6:]) + 1 if last_school else 1
                instance.codeLR = f'DEPLR{year}{number:06d}'

            # Generate QR link and image
            qr_link = f"{request.scheme}://{request.get_host()}/lettre/{instance.id}/"
            instance.lienQR = qr_link

            qr_img = qrcode.make(qr_link)
            temp_dir = os.path.join(settings.MEDIA_ROOT, "temp_qr")
            os.makedirs(temp_dir, exist_ok=True)
            safe_name = re.sub(r'[^0-9a-zA-Z]+', '_', instance.codeLR)
            qr_filename = f"{safe_name}_qr.png"
            qr_path = os.path.join(temp_dir, qr_filename)
            qr_img.save(qr_path)

            # Regenerate PDF only if user wants (or always regenerate)
            pdf_replacements = {
                "[nom]": instance.nom,
                "[codeAE]": instance.codeLR,
                "[date]": instance.dateAjout.strftime("%d/%m/%Y"),
                "[QR]": "[QR]"  # placeholder in PDF template
            }

            pdf_path = fill_pdf(
                "template.pdf",
                f"{instance.codeLR}.pdf",
                pdf_replacements,
                qr_image_path=qr_path
            )

            # Save PDF to model
            with open(pdf_path, 'rb') as f:
                instance.pdf_file.save(f"{instance.codeLR}.pdf", File(f), save=False)

            # Save instance
            instance.save()

            # Cleanup temporary files
            try:
                if os.path.exists(qr_path):
                    os.remove(qr_path)
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                if os.path.exists(temp_dir) and not os.listdir(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as e:
                print(f"Error cleaning up files: {e}")

            return redirect('school_detail', qr_uuid=instance.qr_uuid)
        else:
            print(form.errors)
    else:
        form = SchoolForm(instance=school)

    return render(request, "edit_school.html", {
        "form": form,
        "school": school,
    })

# 4)user 
def edit_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")  # 🔄 redirect where you want
    else:
        form = UserEditForm(instance=user)

    return render(request, "edit_user.html", {"form": form, "user": user})


#---------------------------------- delete -----------------------------------------#

# 1) director
def delete_director(request, director_id):
    if not request.user.groups.filter(name="Director").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    director = get_object_or_404(DirectorAuthorization, id=director_id)
    director.delete()
    return redirect('directors_list')


# 2) teacher
def delete_teacher(request, teacher_id):
    if not request.user.groups.filter(name="Teacher").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    teacher = get_object_or_404(TeacherAuthorization, id=teacher_id)
    teacher.delete()
    return redirect('teacher_list')

# 3) school/lettre
def delete_school(request, school_id):
    if not request.user.groups.filter(name="Schools").exists():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home") 
    school = get_object_or_404(School, id=school_id)
    school.delete()
    return redirect('school_list')
# 4)user 
def delete_user(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")
    school = get_object_or_404(CustomUser, id=user_id)
    school.delete()
    return redirect('user_list')

