from PyPDF2 import PdfFileReader, PdfFileWriter
import sys

'''
Purpose: to split a PDF into multiple PDFs by page numbers

Last edited: 10/27
'''

print("Purpose: to split PDFs into multiple PDFs by page numbers \n")

input_file_location = input("Enter input file location and name: ")

try:
    infile = open(input_file_location, 'rb')
except:
    print("\nfatal error: file not found")
    sys.exit()

reader = PdfFileReader(infile)

output_file_location = input("Enter output file location and name (without .pdf extension): ")
individ_pages = input("Pages can be saved as individual PDFs or one PDF. Should pages be saved as one PDF? (y/n): ")

input_page_nums = input("Enter page numbers or ranges of pages (with a single dash between numbers). Make sure they are separated by 1 space each: ")
page_number_list = input_page_nums.split(' ')

pages = set([])

for num in page_number_list:
    if('-' in str(num)):
        range = str(num).split('-')

        current_page = int(range[0])
        while(current_page <= int(range[1])):
            pages.add(current_page - 1)
            current_page += 1

    else:
        pages.add(int(num) - 1)

pages = sorted(pages)

if(individ_pages == 'y'):
    writer = PdfFileWriter()

    for page in pages:
        writer.addPage(reader.getPage(page))

    with open(output_file_location + ".pdf", 'wb') as outfile:
        writer.write(outfile)

else:
    for page in pages:
        writer = PdfFileWriter()
        writer.addPage(reader.getPage(page))

        with open(output_file_location + "-" + str(page + 1) + ".pdf", 'wb') as outfile:
            writer.write(outfile)

print("Finished!")
