from flask import Flask, render_template, request, send_file
import pypdf
import io
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_pdf():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400

    reader = pypdf.PdfReader(file)
    writer = pypdf.PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    output_stream = io.BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)

    return send_file(
        output_stream,
        as_attachment=True,
        download_name="processed_file.pdf",
        mimetype="application/pdf"
    )

if __name__ == '__main__':
    app.run(debug=True)