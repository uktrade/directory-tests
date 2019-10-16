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


def extract_text_from_pdf(
    pdf_bytes: bytes = None,
    pdf_path: str = None,
    *,
    codec: str = "utf-8",
    password: str = "",
    maxpages: int = 0,
    caching: bool = True,
    remove_empty_lines: bool = True,
) -> str:
    error = f"Please provide PDF in-memory buffer stream or path to PDF file"
    assert pdf_bytes or pdf_path, error
    if pdf_bytes:
        pdf_file = io.BytesIO(pdf_bytes)
    else:
        pdf_file = open(pdf_path, "rb")
    resource_manager = PDFResourceManager()
    out_file = io.StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, out_file, codec=codec, laparams=laparams)
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
