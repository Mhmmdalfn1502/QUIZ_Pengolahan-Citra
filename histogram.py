import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance
import io
import numpy as np
import cv2

app = Flask(__name__)
CORS(app)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    contrast_value = float(request.form.get("contrast", 1))  # Dapatkan nilai kontras

    if file:
        img = Image.open(file.stream)
        enhancer = ImageEnhance.Contrast(img)
        img_enhanced = enhancer.enhance(contrast_value)  # Sesuaikan kontras
        img_np = np.array(img_enhanced)

        # Histogram Equalization
        img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        equalized_img = cv2.equalizeHist(img_gray)

        # Save the processed image
        output_path = "static/equalized_image.png"
        cv2.imwrite(output_path, equalized_img)

        if os.path.exists(output_path):
            print("File berhasil disimpan di:", output_path)  # Debug log
            return jsonify(
                {"equalized_image": f"http://localhost:5000/static/equalized_image.png"}
            )
        else:
            print("Gagal menyimpan file.")  # Debug log
            return jsonify({"error": "Failed to process image"}), 500
    return jsonify({"error": "No file uploaded"}), 400

if __name__ == "__main__":
    app.run(port=5000)
