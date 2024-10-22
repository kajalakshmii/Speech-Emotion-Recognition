# SERSapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import EmotionModel
from django.conf import settings
import joblib
import os
import numpy as np
import librosa

# Define MODEL_ROOT using settings.py for better portability
MODEL_ROOT = os.path.join(settings.BASE_DIR, 'model')

def extract_feature(file_name, mfcc=True, chroma=True, mel=True):
    try:
        y, sr = librosa.load(file_name, sr=None)
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None

    features = []

    if mfcc:
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features.extend(np.mean(mfccs, axis=1))
    if chroma:
        chromagram = librosa.feature.chroma_stft(y=y, sr=sr)
        features.extend(np.mean(chromagram, axis=1))
    if mel:
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        features.extend(np.mean(mel_spectrogram, axis=1))

    # Ensure the feature vector has exactly 180 elements
    remaining_features = 180 - len(features)
    if remaining_features > 0:
        features.extend([0] * remaining_features)
    else:
        features = features[:180]

    return np.array(features)

def predict_emotion(file_path):
    try:
        model_path = os.path.join(MODEL_ROOT, 'Emotion_Voice_Detection_Model.pkl')
        model = joblib.load(model_path)

        features = extract_feature(file_path)
        if features is None:
            raise ValueError("Feature extraction failed.")

        prediction = model.predict(features.reshape(1, -1))
        return prediction[0]
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "Prediction Failed"

def index(request):
    return render(request, 'index.html')

def upload_audio(request):
    if request.method == 'POST' and 'audio_file' in request.FILES:
        audio_file = request.FILES['audio_file']

        # Validate file type
        if not audio_file.name.lower().endswith(('.wav', '.mp3', '.ogg')):
            return render(request, 'index.html', {'error': 'Unsupported file format. Please upload WAV, MP3, or OGG files.'})

        # Save the uploaded audio file to a temporary location
        file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        try:
            with open(file_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Ensure the file is fully written and closed before proceeding with prediction
            f.close()

            # Get the predicted emotion
            predicted_emotion = predict_emotion(file_path)

            # Render the result.html page with the predicted emotion
            return render(request, 'result.html', {'predicted_emotion': predicted_emotion})

        except Exception as e:
            print(f"Error handling upload: {e}")
            return render(request, 'index.html', {'error': 'An error occurred while processing the audio file.'})

        finally:
            # Ensure the file is deleted after prediction or in case of an error
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting the file: {e}")

    return render(request, 'index.html')


def predict_recorded_audio(request):
    if request.method == 'POST' and 'audio_file' in request.FILES:
        audio_file = request.FILES['audio_file']

        # Validate file type
        if not audio_file.name.lower().endswith(('.wav', '.mp3', '.ogg')):
            return render(request, 'index.html', {'error': 'Unsupported file format. Please upload WAV, MP3, or OGG files.'})

        # Save the uploaded audio file to a temporary location
        file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
        try:
            with open(file_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Ensure the file is fully written and closed before proceeding with prediction
            f.close()

            # Get the predicted emotion
            predicted_emotion = predict_emotion(file_path)

            # Render the result.html page with the predicted emotion
            return render(request, 'result.html', {'predicted_emotion': predicted_emotion})

        except Exception as e:
            print(f"Error handling upload: {e}")
            return render(request, 'index.html', {'error': 'An error occurred while processing the audio file.'})

        finally:
            # Ensure the file is deleted after prediction or in case of an error
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting the file: {e}")

    # Redirect to upload-audio page if no file was uploaded
    return redirect('upload-audio')