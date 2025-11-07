import fitz
import os
import tempfile
import shutil
from django.conf import settings
import arabic_reshaper
from bidi.algorithm import get_display

def fill_pdf(template_filename, output_filename, replacements, qr_image_path=None, arabic_text=None):
    """
    Replace placeholders and insert Arabic text in the middle of the PDF.
    """

    template_path = os.path.join(settings.BASE_DIR, 'db', 'static', 'pdf', template_filename)
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated')
    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf = fitz.open(template_path) # type: ignore

        # مسار الخط العربي (Amiri أو غيره)
        
        arabic_font_path = os.path.join(settings.BASE_DIR, "db", "static", "fonts", "Amiri-Regular.ttf")

        for page in pdf:
            # --- استبدال placeholders ---
            for placeholder, replacement in replacements.items():
                if placeholder == "[QR]":
                    continue

                text_instances = page.search_for(placeholder)
                for inst in text_instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()

                    rect = fitz.Rect(inst.x0, inst.y0, inst.x0 + 300, inst.y1 + 20) # type: ignore
                    page.insert_textbox(
                        rect,
                        str(replacement),
                        fontsize=12,
                        fontname="helv",  # للإنجليزي
                        color=(0, 0, 0),
                        align=0
                    )

            # --- QR code ---
            if qr_image_path and "[QR]" in replacements:
                qr_instances = page.search_for("[QR]")
                for inst in qr_instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()
                    rect = fitz.Rect(inst.x0, inst.y0, inst.x0 + 65, inst.y0 + 65)
                    page.insert_image(rect, filename=qr_image_path, keep_proportion=True)

            # --- النص العربي في وسط الصفحة ---
            if arabic_text:
                # استبدال placeholders داخل النص
                final_text = arabic_text
                for placeholder, replacement in replacements.items():
                    final_text = final_text.replace(placeholder, str(replacement))

                page_width = page.rect.width
                page_height = page.rect.height
                rect = fitz.Rect(50, page_height/3, page_width-50, page_height/3 + 400)

                # تسجيل الخط العربي للصفحة
                page.insert_font(fontname="Amiri", fontfile=arabic_font_path)
                # 🔹 إعادة تشكيل + دعم RTL
                text = "\n".join([line.strip() for line in arabic_text.splitlines()])  # إزالة الفراغات
                # reshaped_text = arabic_reshaper.reshape(text)
                # bidi_text = get_display(reshaped_text)
                reshaped_text = arabic_reshaper.reshape(final_text)
                bidi_text = get_display(reshaped_text)

                page.insert_textbox(
                    rect,
                    bidi_text,  
                    fontsize=14,
                    fontname="Amiri",
                    align=1,  
        
                )


        temp_output = os.path.join(temp_dir, output_filename)
        pdf.save(temp_output)
        pdf.close()
        shutil.move(temp_output, output_path)

        return output_path
