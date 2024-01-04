from flask import Flask, render_template, request, redirect, url_for
import os
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        youtube_url = request.form['url']
        choice = request.form['choice']

        try:
            yt = YouTube(youtube_url)

            if choice == 'video':
                video_stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
                video_stream.download('./downloads', filename_prefix='video_')
                return redirect(url_for('index'))  # Return a redirect after video download

            elif choice == 'audio':
                audio_stream = yt.streams.filter(only_audio=True).first()
                audio_file = audio_stream.download()
                file_extension = audio_file[-4:]
                audio_file_name = audio_file[:-4] + '.mp3'

                if file_extension != '.mp3':
                    os.rename(audio_file, audio_file_name)
                else:
                    os.rename(audio_file, audio_file_name)
                
                return redirect(url_for('index'))  # Return a redirect after audio download

        except Exception as e:
            return render_template('index.html', error=True)  # Return rendered template for any exception
        
    return render_template('index.html', error=True)  # Return rendered template for other cases

if __name__ == '__main__':
    app.run(debug=True)
