# -*- coding: utf-8 -*-
import io
import logging

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


class NoPDFMinerLogEntriesFilter(logging.Filter):
    def filter(self, record):
        skip = [
            "nextline",
            "nexttoken",
            "seek",
            "start_type",
            "exec",
            "nextobject",
            "do_keyword",
            "add_results",
            "end_type",
            "get_unichr",
            "Stream",
            "register",
            "getobj",
            "xref",
            "Resource",
            "Processing ",
            "trailer",
            "get_font",
            "Page",
            "find_xref",
            "render_contents",
            "read_xref_from",
        ]
        return all(not record.getMessage().startswith(word) for word in skip)


def extract_text_from_pdf_bytes(
    pdf_bytes: bytes,
    *,
    codec: str = "utf-8",
    password: str = "",
    maxpages: int = 0,
    caching: bool = True,
    remove_empty_lines: bool = True,
) -> str:
    resource_manager = PDFResourceManager()
    out_file = io.StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, out_file, codec=codec, laparams=laparams)
    pdf_file = io.BytesIO(pdf_bytes)
    interpreter = PDFPageInterpreter(resource_manager, device)
    page_numbers = set()
    pdf_pages = PDFPage.get_pages(
        pdf_file,
        page_numbers,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
    )
    for page in pdf_pages:
        interpreter.process_page(page)

    text = out_file.getvalue()

    pdf_file.close()
    device.close()
    out_file.close()
    if remove_empty_lines:
        text = "\n".join([line for line in text.splitlines() if line.strip()])
    return text
