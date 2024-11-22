from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'secret-key'  # Dibutuhkan untuk flash messages

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    rotated_image_url = None

    if request.method == "POST":
        if 'image' in request.files and request.files['image']:
            image_file = request.files['image']
            degrees = request.form.get('degrees', type=int)

            if image_file and degrees is not None:
                input_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], image_file.filename)
                image_file.save(input_path)

                img = Image.open(input_path)
                rotated_img = img.rotate(-degrees, expand=True)
                output_filename = f"rotated_{image_file.filename}"
                output_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], output_filename)
                rotated_img.save(output_path)

                rotated_image_url = url_for(
                    'uploaded_file', filename=output_filename)

    return render_template("index.html", rotated_image=rotated_image_url)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/delete", methods=["POST"])
def delete_image():
    image_path = request.form.get("image_path")
    if image_path:
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], os.path.basename(image_path))
        if os.path.exists(file_path):
            os.remove(file_path)
            flash("Image deleted successfully.", "success")  # Pesan sukses
        else:
            flash("Image not found.", "error")  # Pesan error

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
