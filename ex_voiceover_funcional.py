import argparse
from src.audio_video import *
from src.ia import *

from gtts import gTTS 


def tts(working_dir, text_file, audio_file='new_audio.wav'):
    with open(working_dir+text_file, 'r') as f:
        text = f.read()

    speech = gTTS(text=text, lang='en', tld='ca', slow=False) 
    speech.save(working_dir + audio_file)

    return audio_file 


def get_args():
    parser = argparse.ArgumentParser(description="Dublagem Automática")
    parser.add_argument("--working_dir", metavar="working_dir", type=str, help="Diretorio de Trabalho")
    parser.add_argument("--file", metavar="file", type=str, help="Arquivo de Video")
    parser.add_argument("--sample_size", metavar="sample_size", type=int, help="Tamanho da amostra de video em segundos")
    return parser.parse_args()


def voiceover(working_dir, file, sample_size):
    sample, audio = extract_sample(working_dir, file, sample_size)
    _ = stt(working_dir, audio)
    translated_text = stt(working_dir, audio, translate=True, text_file='translated.txt')
    new_audio = tts(working_dir, translated_text)
    overrite_audio_sample(working_dir, sample, new_audio)
    

if __name__ == '__main__':
    args = get_args()
    voiceover(args.working_dir, args.file, args.sample_size)