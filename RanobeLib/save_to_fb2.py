import os
from lxml import etree

def save_document_to_fb2(self):
    try:
        fb2_file_path = os.path.join(self.project_dir, f"{self.name_project}.fb2")

        if os.path.exists(fb2_file_path):
            tree = etree.parse(fb2_file_path)
            root = tree.getroot()
            body = root.find("body")
        else:
            root = etree.Element("FictionBook")
            body = etree.SubElement(root, "body")
            tree = etree.ElementTree(root)

        section = etree.SubElement(body, "section")
        title = etree.SubElement(section, "title")
        p_title = etree.SubElement(title, "p")
        p_title.text = self.chapter_title

        for paragraph in self.header_p:
            p = etree.SubElement(section, "p")
            p.text = paragraph.get_text(strip=True)

        tree.write(fb2_file_path, pretty_print=True, xml_declaration=True, encoding='UTF-8')

        return fb2_file_path

    except Exception as e:
        self.msg_manager.show_message('error_saving_in_format', 'FB2', str(e))
