from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash
from PIL import Image
import os

app = Flask(__name__)
app.secret_key = 'secret-key'

UPLOAD_FOLDER = 'uploads'
ROTATED_FOLDER = 'rotated'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROTATED_FOLDER'] = ROTATED_FOLDER

# Pastikan folder untuk menyimpan gambar ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ROTATED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    original_image_url = None
    rotated_image_url = None

    if request.method == "POST":
        # Periksa apakah file gambar diupload
        if 'image' in request.files and request.files['image']:
            image_file = request.files['image']
            degrees = request.form.get('degrees', type=int)

            if image_file and degrees is not None:
                # Simpan gambar asli
                input_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], image_file.filename)
                image_file.save(input_path)

                # Lakukan rotasi pada gambar
                try:
                    img = Image.open(input_path)
                    rotated_img = img.rotate(-degrees, expand=True)
                    output_filename = f"rotated_{image_file.filename}"
                    output_path = os.path.join(
                        app.config['ROTATED_FOLDER'], output_filename)
                    rotated_img.save(output_path)

                    # URL untuk gambar asli dan hasil rotasi
                    original_image_url = url_for(
                        'uploaded_file', folder='uploads', filename=image_file.filename)
                    rotated_image_url = url_for(
                        'uploaded_file', folder='rotated', filename=output_filename)

                    flash("Gambar berhasil dirotasi!", "success")
                except Exception as e:
                    flash(
                        f"Terjadi kesalahan saat memproses gambar: {str(e)}", "error")
                    return redirect("/")

    return render_template("index.html",
                           original_image=original_image_url,
                           rotated_image=rotated_image_url)


@app.route("/uploads/<folder>/<filename>")
def uploaded_file(folder, filename):
    folder_path = app.config['UPLOAD_FOLDER'] if folder == 'uploads' else app.config['ROTATED_FOLDER']
    return send_from_directory(folder_path, filename)


@app.route("/delete", methods=["POST"])
def delete_images():
    original_image = request.form.get("original_image")
    rotated_image = request.form.get("rotated_image")

    deleted_files = []

    # Hapus gambar asli
    if original_image:
        original_path = os.path.join(app.root_path, original_image.lstrip('/'))
        if os.path.exists(original_path):
            os.remove(original_path)
            deleted_files.append("Gambar asli")

    # Hapus gambar hasil rotasi
    if rotated_image:
        rotated_path = os.path.join(app.root_path, rotated_image.lstrip('/'))
        if os.path.exists(rotated_path):
            os.remove(rotated_path)
            deleted_files.append("Gambar hasil rotasi")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
