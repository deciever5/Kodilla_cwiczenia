import PyPDF2
import sys

# grabbing files for marking and watermark
for_marking = sys.argv[1]
watermark = sys.argv[2]
marked = sys.argv[3]

pdf_for_marking = PyPDF2.PdfReader(open(for_marking, "rb"))
pdf_with_watermark = PyPDF2.PdfReader(open(watermark, "rb"))
marked_file = PyPDF2.PdfFileWriter()

# scrolling through pages
# marking pages

for page in range(pdf_for_marking.getNumPages()):
    page_for_marking = pdf_for_marking.getPage(page)
    page_for_marking.mergePage(pdf_with_watermark.getPage(0))
    marked_file.addPage(page_for_marking)

# save pages
with open(marked, "wb") as finished_pdf:
    marked_file.write(finished_pdf)
