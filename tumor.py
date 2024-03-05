from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/DunnBC22/yolos-tiny-Brain_Tumor_Detection"
HEADERS = {"Authorization": "Bearer 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"}

# Load the model
def load_model():
    # Add your code to load the model here
    pass

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            # Save the file temporarily
            filename = os.path.join("uploads", file.filename)
            file.save(filename)

            # Call the API
            with open(filename, "rb") as f:
                data = f.read()
            response = requests.post(API_URL, headers=HEADERS, data=data)
            result = response.json()

            # Clean up the temporary file
            os.remove(filename)

            return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    # Load the model
    load_model()
    
    app.run(debug=True)
