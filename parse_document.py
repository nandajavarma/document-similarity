#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cStringIO import StringIO
from pprint import pprint

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert(pdf_file, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    codec = 'utf8'
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(pdf_file, 'rb')

    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()

    output.close

    return text


def extract_from_pdf(pdf_file):
    drows = tuple()
    body = convert(pdf_file)

    body = body.strip()
    if body != "":
        lines = body.split('\n')
        body_str = ""
        c = 0
        title = ""
        for l in lines:
            '''Don't consider more than 200 lines (for long pdfs!)'''
            if c < 200:
                if title == "":
                    title = l
                if l != "":
                    body_str += l + " "
            c += 1

        title = unicode(title, "utf-8")
        body_str = unicode(body_str, "utf-8")
        drows = (title.encode('utf-8'), body_str.encode('utf-8'))


    return drows
