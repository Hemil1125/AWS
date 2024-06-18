"""
A Flask application for uploading and viewing images.
"""

import os
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'File_Uploading'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def main():
    """
    Render the main page.
    """
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def success():
    """
    Handle file upload and render acknowledgement page.
    """
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        return render_template("Acknowledgement.html", name=f.filename)
    return ""

@app.route('/view_images')
def view_images():
    """
    Display uploaded images with their details.
    """
    image_list = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            modified_date = file_stat.st_mtime
            image_list.append({
                'filename': filename,
                'size': file_size,
                'modified_date': modified_date
            })
    return render_template("view_images.html", image_list=image_list)

@app.route('/File_Uploading/<filename>')
def uploaded_file(filename):
    """
    Serve uploaded files.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
