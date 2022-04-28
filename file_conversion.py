# Version 0.2

from docx2pdf import convert
import fitz
import comtypes.client
import PyPDF2
import os

"""
Packages:
"""


# PPTX to PDF
def pptx2pdf(pptx_file, pdf_file, format_type=32):
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1

    if pdf_file[-3:] != 'pdf':
        pdf_file = pdf_file + ".pdf"
    deck = powerpoint.Presentations.Open(pptx_file)
    deck.SaveAs(pdf_file, format_type)  # formatType = 32 for ppt to pdf
    deck.Close()
    powerpoint.Quit()




# PDF to IMAGE
def pdf2img(pdf_file, img_folder, img_name):
    # get page count
    pdf = PyPDF2.PdfFileReader(pdf_file)
    page_count = pdf.numPages

    # Conversion
    doc = fitz.open(pdf_file)
    for i in range(page_count):
        page = doc.load_page(i)  # number of page
        pix = page.get_pixmap()
        output = os.path.join(img_folder, f'{img_name}_{i}.jpg')
        pix.save(output)


# DOCX to PDF
def docx2pdf(docx, pdf_file):
    convert(docx, pdf_file)


# pdf2img(r'D:\Dinesh\Project\Jackie Chan Info.pdf', r'D:\Dinesh\Project\Images', "Img")