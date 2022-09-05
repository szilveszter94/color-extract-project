import os
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import extraction
from datetime import date


# SET CONSTANTS
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# SET FLASK APP
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'KFDFWe1292udj9djasd'
current_year = date.today().year


# CONVERT RGB TO HEX
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


# SET ALLOWED FILETYPES
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# CONVERT STRING TO TUPLE
def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


# SET UPLOAD FILE ROUTE
@app.route('/', methods=['GET', 'POST'])
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
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # save the image into os
            filename = 'image.jpg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_and_extract_file', name=filename))
    return render_template("upload.html", year=current_year)


# SET DOWNLOAD AND EXTRACT ROUTE
@app.route('/uploads/<name>')
def download_and_extract_file(name):
    # download image
    send_from_directory(app.config["UPLOAD_FOLDER"], name)
    # image path
    img = 'static/images/image.jpg'
    # number of extracting colors
    clusters = 10
    # insert image into color extraction module
    dc = extraction.DominantColors(img, clusters)
    # extracted colors
    colors = dc.dominant_colors()
    tuple_colors = []
    hex_colors = []
    # format extracted colors and convert to hex
    for i in colors:
        tuple_colors.append(totuple(i))
    for i in tuple_colors:
        hex_colors.append(rgb_to_hex(i))
    # render upload file and show the colors
    download = True
    return render_template("upload.html", color=hex_colors, download=download, year=current_year)

# start the app
if __name__ == "__main__":
    app.run(debug=True)
