import fitz  # PyMuPDF
import os
from django.conf import settings
import tempfile
import shutil

def fill_pdf(template_filename, output_filename, replacements, qr_image_path=None):
    """
    Replace placeholders like [nom], [codeAE], [date], [QR] directly in the PDF.
    Keeps placeholders replaced with actual text and inserts QR code.
    """

    template_path = os.path.join(settings.BASE_DIR, 'db', 'static', 'pdf', template_filename)
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated')
    output_path = os.path.join(output_dir, output_filename)
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf = fitz.open(template_path)

        for page in pdf:
            for placeholder, replacement in replacements.items():
                if placeholder == "[QR]":
                    continue  # handled separately

                text_instances = page.search_for(placeholder)
                for inst in text_instances:
                    # **Erase old placeholder** (optional, white fill)
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()  # apply immediately before inserting text

                    # Insert replacement text
                    rect = fitz.Rect(inst.x0, inst.y0, inst.x0 + 300, inst.y1 + 15)  # width 300
                    font_size = 12

                    while True:
                        text_width = fitz.get_text_length(str(replacement), fontname="helvetica", fontsize=font_size)
                        if text_width <= rect.width or font_size <= 6:
                            break
                        font_size -= 1  # reduce font until it fits

                    page.insert_textbox(
                        rect,
                        str(replacement),
                        fontsize=font_size,
                        fontname="helvetica",
                        color=(0, 0, 0),
                        align=0
                    )

            # Insert QR code
            if qr_image_path and "[QR]" in replacements:
                qr_instances = page.search_for("[QR]")
                for inst in qr_instances:
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()
                    rect = fitz.Rect(inst.x0, inst.y0, inst.x0 + 100, inst.y0 + 100)
                    page.insert_image(rect, filename=qr_image_path, keep_proportion=True)

        temp_output = os.path.join(temp_dir, output_filename)
        pdf.save(temp_output)
        pdf.close()
        shutil.move(temp_output, output_path)

        return output_path
