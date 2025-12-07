from flask import Flask, send_file, render_template
import sys
import os
import generate_song 

# tell Flask where to find static files and templates
app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    # This serves your HTML file
    return render_template('index.html')

@app.route('/generate-midi')
def generate_midi_route():
    try:
        # Run your logic (ensure this returns a valid file path)
        generated_file_path = generate_song.generate() 

        return send_file(
            generated_file_path,
            mimetype='audio/midi',
            as_attachment=True,
            download_name='generated_song.mid'
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)