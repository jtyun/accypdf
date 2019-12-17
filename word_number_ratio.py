import pdftotext
import sys

given_pdf = 'BRIDGEPORT CONN (CT)_FY2018.pdf'

# Returns a list of ratios of numbers to words. Each index of the list is a new page.
def numbers_to_words(working_pdf):
    # Load PDF
    with open(working_pdf, "rb") as f:
        pdf = pdftotext.PDF(f)

    ratios = []

    # Iterate over all the pages
    for page in pdf:

        strcount = 0
        numcount = 0
        for word in page:
            if word.isnumeric():
                numcount += 1
            else:
                strcount += 1

        ratios.append(numcount / strcount)
    
    print(ratios)
    return ratios


numbers_to_words(sys.argv[1])