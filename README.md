Project Description:

This Django application is a management system for private education institutions, allowing the administration to:

Register private schools (School Authorization Letter)

Register directors of schools

Register teachers of private institutions

Generate official authorization PDFs for each record

Automatically generate and embed QR Codes inside the PDFs

Allow verification of documents online by scanning the QR code

Restrict access based on user roles and groups

Manage system users and permissions

The system ensures digital tracking and verification of administrative authorizations.

How the System Works
Actor / Role	Permissions	What They Can Do
School Manager (Schools group)	Limited	Add & view school authorization letters
Director Manager (Director group)	Limited	Issue director authorization certificates
Teacher Manager (Teacher group)	Limited	Issue teaching authorization certificates
Administrator (Superuser)	Full Access	Create users and assign groups

Core Functionalities Explained
1) Authentication

The application uses Django’s built-in login system.
Only authenticated users can access the protected pages.

user = authenticate(request, username=username, password=password)
login(request, user)

2) Role-Based Access Control

Each page checks if the user belongs to the correct group:

if not request.user.groups.filter(name="Schools").exists():
    return redirect("home")


This ensures only authorized staff perform specific tasks.

3) Unique Authorization Code Generation

For each new record, a unique reference code is created:

Example for a school:

DEPLR + current_year_last_two_digits + sequential_number (6 digits)


Which produces codes like:

DEPLR25 000001
DEPLR25 000002

4) QR Code Generation

Each authorization gets a verification link:

https://yourdomain.com/lettre/<UUID>/


A QR code is generated from this link and later inserted into the PDF.

qr_link = f"{request.scheme}://{request.get_host()}/lettre/{instance.qr_uuid}/"
qr_img = qrcode.make(qr_link)

5) PDF Certificate Generation

The system fills a pre-designed PDF template with:

Person’s information

Authorization details

The QR Code

Using:

fill_pdf("template.pdf", "output.pdf", ...)


Arabic text is processed using:

arabic_reshaper + bidi.algorithm.get_display


To ensure proper right-to-left display.

6) Online Verification Pages

When someone scans the QR code, it opens:

/school/<uuid>/
/director/<uuid>/
/teacher/<uuid>/


Where the certificate data is displayed for verification.
