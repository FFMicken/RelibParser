import os
from docx import Document, shared

def save_document_to_docx(self):
    docx_file_path = os.path.join(self.project_dir, f"{self.name_project}.docx")
    doc = Document()

    for chapter_title, header_p in self.chapters_buffer:
        title_paragraph = doc.add_paragraph()
        title_run = title_paragraph.add_run(chapter_title)
        title_run.bold = True
        title_run.font.size = shared.Pt(14)

        all_text = '\n'.join([p.get_text(strip=True) for p in header_p if p.get_text(strip=True)])
        cleaned_text = '\n'.join([line.strip() for line in all_text.splitlines() if line.strip()])

        for line in cleaned_text.splitlines():
            doc.add_paragraph(line)

        doc.add_page_break()

    doc.save(docx_file_path)
    self.msg_manager.show_message('all_chapters_are_saved_to', docx_file_path)