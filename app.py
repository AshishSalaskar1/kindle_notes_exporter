import os
from flask.helpers import send_file, send_from_directory
from utils import export_notion_file, read_file, process_books
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS, cross_origin

file_name = "My Clippings.txt"
sep = "=========="
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
cors = CORS(app)

# hiList = read_file(file_name, sep)
# noteList = process_books(hiList)
# export_notion_file(noteList, "output.txt")

@app.route('/')
def hello():
    print("Hello")
    return render_template('index.html', url=request.base_url)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    print("CALLED")
    if request.method == 'POST':
        f = request.files['file']
        f.save("output/My_Clippings.txt")

        content = process_books(read_file("output/My_Clippings.txt",sep))
        export_notion_file(content, "output/output.txt")
        # return send_from_directory(directory="output", filename="output.txt")
        return send_file("output/output.txt", as_attachment=True)

if __name__ == '__main__':
    print("App started Succesfully")
    app.run()
