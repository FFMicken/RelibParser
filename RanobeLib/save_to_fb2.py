import os

from lxml import etree

def save_document_to_FB2(self):
    fb2_file_path = os.path.join(self.project_dir, f"{self.name_project}.fb2")
    root = etree.Element("FictionBook")
    body = etree.SubElement(root, "body")

    for chapter_title, header_p in self.chapters_buffer:
        section = etree.SubElement(body, "section")
        title = etree.SubElement(section, "title")
        p_title = etree.SubElement(title, "p")
        p_title.text = chapter_title

        for paragraph in header_p:
            p = etree.SubElement(section, "p")
            p.text = paragraph.get_text(strip=True)

    tree = etree.ElementTree(root)
    tree.write(fb2_file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    self.msg_manager.show_message('all_chapters_are_saved_to', fb2_file_path)