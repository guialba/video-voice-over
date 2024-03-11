from moviepy.editor import *
import soundfile as sf
import numpy as np
import librosa

def extract_sample(working_dir, file, sample_size=200, sample_file='sample.mp4', audio_sample_file='sample.wav'):
    video = VideoFileClip(working_dir + file)
    sample = video.subclip(0, sample_size)
    sample.write_videofile(working_dir + sample_file)
    sample.audio.write_audiofile(working_dir + audio_sample_file)
    return sample_file, audio_sample_file

def overrite_audio_sample(working_dir, video_file, audio_file, new_file='voiceover.mp4'):
    video = VideoFileClip(working_dir + video_file)
    audio = AudioFileClip(working_dir + audio_file)
    video.audio = audio
    video.write_videofile(working_dir + new_file)
    return new_file

def compose_video(working_dir, video_file, n, final_video_file='final.mp4'):
    samples = [VideoFileClip(working_dir + f'{i}_{video_file}') for i in range(n)]

    video_final = concatenate_videoclips(samples)
    video_final.write_videofile(working_dir + final_video_file)
    return final_video_file


def get_speeches(working_dir, video_file, audio_file, video_sample_file='sample.mp4', audio_sample_file='sample.wav'):
    video = VideoFileClip(working_dir + video_file)
    audio, _ = librosa.load(working_dir + audio_file)

    spectrogram = np.abs(librosa.stft(audio))
    energia = librosa.feature.rms(S=spectrogram)
    limiar_energia = np.mean(energia) - 1*np.std(energia)
    tamanho_minimo_pausa = 0.15
    pausas = []
    no_pausa = False
    for i, e in enumerate(energia[0]):
        if e < limiar_energia:
            if not no_pausa:
                inicio = librosa.frames_to_time(i)
                no_pausa = True
        else:
            if no_pausa:
                fim = librosa.frames_to_time(i)
                pausas.append((inicio, fim))
                no_pausa = False

    pausas = [pausa for pausa in pausas if pausa[1]-pausa[0] > tamanho_minimo_pausa]
    periodos = [(p1[1], p2[0]) for p1, p2 in zip(pausas[:-1], pausas[1:]) if p2[0]-p1[1] > tamanho_minimo_pausa]
    samples = [video.subclip(*periodo) for periodo in periodos]
    
    for i, sample in enumerate(samples):
        sample.write_videofile(working_dir + f'{i}_' + video_sample_file)
        sample.audio.write_audiofile(working_dir + f'{i}_' + audio_sample_file)

    return i, video_sample_file, audio_sample_file