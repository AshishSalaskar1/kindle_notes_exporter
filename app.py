import os
from flask.helpers import send_file, send_from_directory
from utils import export_notion_file, read_file, process_books, convert_to_pdf
from flask import Flask, flash, request, redirect, url_for, render_template
from flask_cors import CORS, cross_origin

file_name = "My Clippings.txt"
sep = "=========="
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello():
    return render_template('index.html', url=request.base_url)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    """Reads uploaded file and returns PDF via Markdown Conversion

    Returns:
        File: PDF file which contains the converted Kindle Highlights File 
    """
    if request.method == 'POST':
        f = request.files['file']
        f.save("output/My_Clippings.txt")

        content = process_books(read_file("output/My_Clippings.txt",sep))
        convert_to_pdf(content)
        # return send_from_directory(directory="output", filename="output.txt")
        return send_file("output/output.pdf", as_attachment=True)

if __name__ == '__main__':
    print("App started Succesfully")
    app.run()
