from flask import Flask, render_template, request, send_from_directory, url_for, redirect, flash
import os
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = 'secret-key'

UPLOAD_FOLDER = 'uploads'
ROTATED_FOLDER = 'rotated'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ROTATED_FOLDER'] = ROTATED_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ROTATED_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    original_image_url = None
    rotated_image_url = None

    if request.method == "POST":
        # cek image sudah di upload
        if 'image' in request.files and request.files['image']:
            image_file = request.files['image']
            degrees = request.form.get('degrees', type=int)

            if image_file and degrees is not None:
                # Save original image
                input_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], image_file.filename)
                image_file.save(input_path)

                try:
                    # Read the image using OpenCV
                    img = cv2.imread(input_path)
                    if img is None:
                        raise ValueError(
                            "Invalid image format or corrupted image.")

                    # Get the image dimensions
                    (h, w) = img.shape[:2]
                    center = (w // 2, h // 2)

                    # Calculate rotation matrix
                    M = cv2.getRotationMatrix2D(center, -degrees, 1.0)
                    rotated_img = cv2.warpAffine(img, M, (w, h))

                    # Save the rotated image
                    output_filename = f"rotated_{image_file.filename}"
                    output_path = os.path.join(
                        app.config['ROTATED_FOLDER'], output_filename)
                    cv2.imwrite(output_path, rotated_img)

                    # Generate URLs for the images
                    original_image_url = url_for(
                        'uploaded_file', folder='uploads', filename=image_file.filename)
                    rotated_image_url = url_for(
                        'uploaded_file', folder='rotated', filename=output_filename)

                except Exception as e:
                    flash(
                        f"An error occurred while processing the image: {str(e)}", "error")
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
    # Delete the original image
    if original_image:
        original_path = os.path.join(app.root_path, original_image.lstrip('/'))
        if os.path.exists(original_path):
            os.remove(original_path)
            deleted_files.append("Original image")

    # Delete the rotated image
    if rotated_image:
        rotated_path = os.path.join(app.root_path, rotated_image.lstrip('/'))
        if os.path.exists(rotated_path):
            os.remove(rotated_path)
            deleted_files.append("Rotated image")

    if deleted_files:
        flash(f"{', '.join(deleted_files)} deleted successfully.", "success")
    else:
        flash("No images found to delete.", "error")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
