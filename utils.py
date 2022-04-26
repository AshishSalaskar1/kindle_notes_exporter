import os
import dateutil.parser
import markdown
from xhtml2pdf import pisa 

quote_sytle="""
<style type="text/css">
    blockquote { font: 14px normal helvetica, sans-serif;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 50px;
        padding-left: 15px;
        padding-top: 20px;
        padding-bottom: 20px;
        border: 1px solid gray;
        border-left: 4px solid #0099cc
    }
</style>
"""

def read_file(file_name, sep):
    """Read My_Clippings file

    Args:
        file_name (str): file to read
        sep (str): separator for books

    Returns:
        List: List of book highlights
    """
    with open(file_name,"r",encoding="utf8") as f:
        content = f.read().split(sep)
        content = [s.strip() for s in content] # remove trailing spaces
        bookList = [list(filter(lambda x : len(x.strip()) != 0,book.split("\n"))) for book in content]
        return list(filter(lambda x:len(x)!=0, bookList))

def process_books(hiList):
    """Extract and preporcess book_data

    Returns:
        Dict: {book_name, date, authors}
    """
    bookList = {}
    for cur in hiList:
        bookName = cur[0]
        date = dateutil.parser.parse(cur[1].split("Added on ")[-1])
        note = " ".join(cur[2:])
        if bookName in bookList:
            bookList[bookName].add((note,date))
        else:
            bookList[bookName] = set([(note,date)])
        
    
    # sort according to time
    for key in bookList.keys():
        bookList[key] = sorted(list(bookList[key]), key=lambda x: x[1])

    return bookList

def export_notion_file(data, fileName):
    """Return markdown file in Notion Supported Format
    """
    bookNames = list(data.keys())
    content = ""

    for bookName in bookNames:
        notes = list(set([x[0] for x in data[bookName]]))
        # print(data[bookName])
        # print(*notes,"\n\n\n",sep="\n\n\n")
        content += ("--- \n\n## **"+bookName.replace("\ufeff","") +"**"+ "\n-" + "\n\n-".join(notes) +"\n\n\n\n<br><br>")

        # print("*-*-*-*-*-*-*"*5)
    with open(fileName,'w',encoding="utf8") as f:
        f.write(content)

def export_markdown_file(data, fileName, return_content_only=False):
    """Convert book_highlights into markdown supportable format
    
    """

    quote_sytle="""
    <style type="text/css">
        blockquote { font: 14px normal helvetica, sans-serif;
            margin-top: 10px;
            margin-bottom: 10px;
            margin-left: 50px;
            padding-left: 15px;
            border-left: 4px solid #0099cc
        }
    </style>
    """
    bookNames = list(data.keys())
    content = ""
    for book_name in bookNames:
        author_name = book_name[book_name.find("(")+1:book_name.find(")")]
        # STARTBOOK -> HR -> Book Title -> Notes as blockquotes -> ENDBOOK
        notes = list(set([x[0] for x in data[book_name]]))
        content += ("--- \n\n# "+book_name.replace("\ufeff","") +""+ "\n"+"*Author: "+author_name+"*"+"\n> " + "\n\n> ".join(notes) +"\n\n\n\n")
    
    if return_content_only:
        return content
    
    with open(fileName,'w',encoding="utf8") as f:
        f.write(content)


def markdown_to_pdf(md_file_name="output/output.md", pdf_name="output/output.pdf"):
    """Convert Markdown file to PDF

    Args:
        md_file_name (str, optional): _description_. Defaults to "output/output.md".
        pdf_name (str, optional): _description_. Defaults to "output/output.pdf".
    """
    # Markdown to HTML
    markdown.markdownFromFile(
        input=md_file_name,
        output='output/output.html',
        encoding='utf8',
    )
    
    # HTML to PDF
    result_file = open(pdf_name, "w+b")
    source_html = ""
    with open("output/output.html","r",encoding="utf-8") as f:
        source_html =quote_sytle+ f.read()
    pisa_status = pisa.CreatePDF(source_html, dest=result_file) 
    result_file.close()

    
def convert_to_pdf(content, pdf_file_name="output.pdf"):
    """Complete Pipeline : Data -> MD -> HTML -> PDF

    Args:
        content : Contents of preprocessed MyClippings.txt file
        pdf_file_name (str, optional): _description_. Defaults to "output.pdf".
    """
    export_markdown_file(content,"output/output.md")
    markdown_to_pdf()