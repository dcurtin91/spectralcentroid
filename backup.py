from flask import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import librosa
import io
import base64

app = Flask(__name__)

@app.route('/')
def upload():
    return render_template("file_upload_form.html")

@app.route('/', methods=['POST'])
def success():
    if request.method == 'POST':
        f1 = request.files['file1']
        f2 = request.files['file2']
        f1.save(f1.filename)
        f2.save(f2.filename)
        FRAME_SIZE = 1024
        HOP_LENGTH = 512
        file1 = f1.filename
        file2 = f2.filename
        my1, sr1 = librosa.load(file1)
        my2, sr2 = librosa.load(file2)
        sc_my1 = librosa.feature.spectral_centroid(y=my1, sr=sr1, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
        sc_my2 = librosa.feature.spectral_centroid(y=my2, sr=sr2, n_fft=FRAME_SIZE, hop_length=HOP_LENGTH)[0]
        frames1 = range(len(sc_my1))
        frames2 = range(len(sc_my2))
        t1 = librosa.frames_to_time(frames1)
        t2 = librosa.frames_to_time(frames2)
        plt.figure(figsize=(25,10))
        plt.plot(t1, sc_my1, color ='b', label='File 1')
        plt.plot(t2, sc_my2, color ='r', label='File 2')
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Spectral Centroid')
        plt.legend()
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return render_template("file_upload_form.html", name1=file1, name2=file2, plot=plot_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
