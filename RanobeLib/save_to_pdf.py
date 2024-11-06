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
        line_height = 14
        max_text_height = height - margin * 2
        max_text_width = width - margin * 2

        pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
        c.setFont("DejaVuSans", 12)

        if not self.chapters_buffer:
            return
        
        for chapter_title, header_p in self.chapters_buffer:
            text = c.beginText(margin, height - margin)
            text.setFont("DejaVuSans", 12)
            text.setLeading(line_height)

            text.textLine(chapter_title)

            all_text = '\n'.join([p.get_text(strip=True) for p in header_p if p.get_text(strip=True)])
            if not all_text.strip():
                self.msg_manager.show_message('chapter_does_not_text', chapter_title)
                continue
            
            cleaned_text = '\n'.join([line.strip() for line in all_text.splitlines() if line.strip()])

            current_height = 0
            for line in cleaned_text.splitlines():
                words = line.split(' ')
                split_line = ""
                for word in words:
                    if c.stringWidth(split_line + word, "DejaVuSans", 12) > max_text_width:
                        text.textLine(split_line)
                        current_height += line_height
                        split_line = word + " "
                        
                        if current_height + line_height > max_text_height:
                            c.drawText(text)
                            c.showPage()
                            text = c.beginText(margin, height - margin)
                            text.setFont("DejaVuSans", 12)
                            current_height = 0
                    else:
                        split_line += word + " "

                if split_line.strip():
                    text.textLine(split_line)
                    current_height += line_height

            c.drawText(text)
            c.showPage()

        c.save()
        self.msg_manager.show_message('all_chapters_are_saved_to', pdf_file_path)
    except Exception as e:
        self.msg_manager.show_message('pdf_creation_error', str(e))
