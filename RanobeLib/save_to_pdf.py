import os

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def save_document_to_PDF(self):
    pdf_file_path = os.path.join(self.project_dir, f"{self.name_project}.pdf")
    
    try:
        c = canvas.Canvas(pdf_file_path, pagesize=A4)
        width, height = A4
        margin = 2 * cm
        text_height = height - margin

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        c.setFont("DejaVuSans", 12)

        if not self.chapters_buffer:
            print("Ошибка: chapters_buffer пуст. Проверьте, были ли главы загружены.")
            return
        
        for chapter_title, header_p in self.chapters_buffer:
            text = c.beginText(margin, text_height)
            text.setFont("DejaVuSans", 12)

            text.textLine(chapter_title)

            all_text = '\n'.join([p.get_text(strip=True) for p in header_p if p.get_text(strip=True)])
            if not all_text.strip():
                print(f"Глава '{chapter_title}' не содержит текста.")
                continue
            
            cleaned_text = '\n'.join([line.strip() for line in all_text.splitlines() if line.strip()])

            for line in cleaned_text.splitlines():
                text.textLine(line)

            c.drawText(text)
            c.showPage()

        c.save()
        self.msg_manager.show_message('all_chapters_are_saved_to', pdf_file_path)
    except Exception as e:
            self.msg_manager.show_message('pdf_creation_error', str(e))