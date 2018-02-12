"""  Assignment3 """
'''
--- beautiful soup ---
Expected duration: 90-120 minutes

For this assignment, we will use the two packages that you have used before and a new one.

Use the beautiful soup package to extract the scores from the html file of the mock results and put it in an excel sheet.

This screenshot contains the desired output: http://screencast.com/t/QCcNLhHh

- extract the columns names (skip the No column)
- extract the student data
- use click to write the command tool as shown below with 2 arguments
- use openpyxl to write to the excel file
- use beautifulsoup to parse and extract the html data.

dumptoexcel.py <mock_test.hml> <outputexcel.xlsx>

Input file for testing:mock_results.html
'''

from BeautifulSoup import *
from openpyxl import *
import click

@click.command()
@click.argument("html_file",nargs=1)
@click.argument("output_excel_file",nargs=1)

def dumptoexcel(html_file,output_excel_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "mock_test_results"
    with open("mock_results.html") as fp:
        soup = BeautifulSoup(fp)
        tr_tags = soup.findAll('tr')
        for tr in tr_tags:
            row = []
            for th_td_tag in tr:
                if isinstance(th_td_tag.contents[0],NavigableString):
                   row.append(int(th_td_tag.string) if th_td_tag.string.strip().isdigit() else th_td_tag.string)
                else:
                    row.append(th_td_tag.contents[0].string)

            ws.append(row[1:])

    wb.save(output_excel_file)


if __name__=='__main__':
    dumptoexcel()

