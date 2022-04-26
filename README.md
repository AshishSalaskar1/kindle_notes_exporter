# Kindle Notes Exporter
Flask app to process my_highlights file stored in kindle and export the notes in Markdown Format

## Steps to spin up the flask server
- Make sure required packages mentioned in `requirement.txt` are present or install them
  ```bash
  pip instal -r requirements.txt 
  ```
- Run the flask app using `python app.py` or visit https://kindlexport.herokuapp.com/
- Upload the `My Clippings.txt` file copied from your Kindle Device
- Download the `output.txt` which contains all the notes from books in Markdown Format

## Basic Workflow
1. Store the uploaded my_clippings.txt file. Read the contents and parse it into Python readable data types.
2. We then convert the read data into Markdown syntax and save it as a Mardown(.md) file
3. Then using Markdown and xhtml2pdf libraries, the Markdown file is first rendered as HTML content and then saved onto the disk as a PDF file.
4. The PDF file is then sent back by the server as Response

## Possible Improvements
- Support to extract all highlights or pick a particular book whose highlights are to be extracted.
- Send the processed pdf files directly to you Email or your Kindle Device using its email address.
- Functionality to allow better control on UI elements
