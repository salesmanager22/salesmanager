from flask import Flask, render_template
from logging import FileHandler,WARNING

from misc import rearrange

import os
from flask import flash, request, redirect, url_for, send_from_directory, send_file
from werkzeug.utils import secure_filename

from datetime import datetime

app = Flask(__name__,template_folder='./frontend/templates',static_folder='./frontend/static')
# file_handler = FileHandler('errorlog.txt')
# file_handler.setLevel(WARNING)

UPLOAD_FOLDER = './data/user_upload/'
DOWNLOAD_FOLDER = './data/outputs/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx'}
from zipfile import ZipFile
from glob import glob
from io import BytesIO


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<name>')
def download_file(name):
    # return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    return send_from_directory(app.config["DOWNLOAD_FOLDER"], name)

@app.route('/downloads/<name>')
def download_zip(name):
    # return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    target = './data/outputs'
    stream = BytesIO()
    with ZipFile(stream, 'w') as zf:
        for file in glob(os.path.join(target, '{}_*.xlsx'.format(name))):
            zf.write(file, os.path.basename(file))
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name='archive_{}.zip'.format(name)
    )

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/run')
def run():
   return render_template('run.html')


@app.route('/faq')
def faq():
   return render_template('faq.html')




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/testdownload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print("case 2===")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            today = datetime.now()
            save_name = today.strftime("%Y.%m.%d-%H;%M;%S.xlsx")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], save_name))
            # rearranged = rearrange(save_name)
            rearrange(save_name)
            print('case 3===')
            return redirect(url_for('download_zip', name=save_name))#'{}_택배사_양식.xlsx'.format(save_name)))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
   app.run()
   