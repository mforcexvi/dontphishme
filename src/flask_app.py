from flask import Flask
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import math
import modules.ocr_api as ocr
import base64

UPLOAD_FOLDER = '/home/nophish/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))

            uploaded_image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            dimensions = (math.floor((uploaded_image.size[0])/10), math.floor((uploaded_image.size[1])/10))
            resized = uploaded_image.resize(dimensions,Image.ANTIALIAS)
            resized.save(os.path.join(app.config['UPLOAD_FOLDER'], "r"+filename))

            qr_url = ocr.decode_qr(os.path.join(app.config['UPLOAD_FOLDER'], "r"+filename))
            ocr_url = ocr.run_ocr('http://nophish.pythonanywhere.com/static/' + filename)


            # results_list = decode(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)))
            # result_string = results_list[0][0].decode("utf-8")

            # output_string = qr_url
            # for url in ocr_url:
            #     if url != None:
            #         output_string += " "
            #         output_string += url

            url_list = []
            if qr_url != "None" and qr_url != None:
                url_list.append(qr_url)
            for url in ocr_url:
                if url != None:
                    url_list.append(url)

            output_string = ""
            if (len(url_list) == 0):
                output_string = "No urls detected"
            else:
                for url in url_list:
                    output_string += " "
                    output_string += url

            return output_string

        return "abc"
    # return
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''
