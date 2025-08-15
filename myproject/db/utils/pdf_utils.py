import fitz
import os
from django.conf import settings

def fill_pdf(template_filename, output_filename, replacements, qr_image_path=None):
    template_path = os.path.join(settings.BASE_DIR, 'db', 'static', 'pdf', template_filename)
    output_path = os.path.join(settings.MEDIA_ROOT, 'generated', output_filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    pdf = fitz.open(template_path)

    for page in pdf:
        # 1️⃣ Redact and replace text placeholders (skip QR)
        for old, new in replacements.items():
            if old == "[QR]":
                continue  # QR will be handled separately
            areas = page.search_for(old)
            for area in areas:
                page.add_redact_annot(area, fill=(1, 1, 1))
        page.apply_redactions()

        # 2️⃣ Insert replacement text
        for old, new in replacements.items():
            if old == "[QR]":
                continue
            areas = page.search_for(old)
            for area in areas:
                page.insert_text((area.x0, area.y0), str(new), fontsize=12, fontname="helv")

        # 3️⃣ Insert QR image if provided
        if qr_image_path:
            qr_areas = page.search_for("[QR]")  # placeholder in PDF
            for qr_area in qr_areas:
                # Double the size of the placeholder
                rect = fitz.Rect(
                    qr_area.x0,
                    qr_area.y0,
                    qr_area.x0 + (qr_area.x1 - qr_area.x0) * 5,  # width ×2
                    qr_area.y0 + (qr_area.y1 - qr_area.y0) * 6    # height ×2
                )
                page.insert_image(rect, filename=qr_image_path)

    pdf.save(output_path)
    return output_path
    