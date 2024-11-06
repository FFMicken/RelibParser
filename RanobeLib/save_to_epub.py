import os

from ebooklib import epub

def save_document_to_EPUB(self):
    epub_file_path = os.path.join(self.project_dir, f"{self.name_project}.epub")
    book = epub.EpubBook()
    book.set_title(self.name_project)
    book.set_language('ru')

    try:
        for chapter_index, (chapter_title, header_p) in enumerate(self.chapters_buffer):
            chapter = epub.EpubHtml(title=chapter_title, file_name=f'chapter_{chapter_index}.xhtml', lang='ru')
            all_text = '\n'.join([p.get_text(strip=True) for p in header_p if p.get_text(strip=True)])
            cleaned_text = '\n'.join([line.strip() for line in all_text.splitlines() if line.strip()])

            chapter.content = f"<h1>{chapter_title}</h1><p>{cleaned_text.replace('\n', '</p><p>')}</p>"

            book.add_item(chapter)
            book.spine.append(chapter)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        style = 'BODY {color: black;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        book.add_item(nav_css)

        epub.write_epub(epub_file_path, book)
        self.msg_manager.show_message('all_chapters_are_saved_to', epub_file_path)
    except Exception as e:
        self.msg_manager.show_message('all_chapters_are_saved_to', epub_file_path)
        print('error_saving_to_EPUB: ', {e})
