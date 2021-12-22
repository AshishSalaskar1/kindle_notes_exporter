import os
import dateutil.parser

def read_file(file_name, sep):
    with open(file_name,"r",encoding="utf8") as f:
        content = f.read().split(sep)
        content = [s.strip() for s in content]
        bookList = [list(filter(lambda x : len(x.strip()) != 0,book.split("\n"))) for book in content]
        return list(filter(lambda x:len(x)!=0, bookList))

def process_books(hiList):
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
    bookNames = list(data.keys())
    content = ""

    for bookName in bookNames:
        notes = list(set([x[0] for x in data[bookName]]))
        # print(data[bookName])
        # print(*notes,"\n\n\n",sep="\n\n\n")
        content += ("--- \n\n## **"+bookName.replace("\ufeff","") +"**"+ "\n-" + "\n\n-".join(notes) +"\n\n\n\n")

        # print("*-*-*-*-*-*-*"*5)
    with open(fileName,'w',encoding="utf8") as f:
        f.write(content)

