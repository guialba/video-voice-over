import argparse
from src.audio_video import *
from src.ia import *

def get_args():
    parser = argparse.ArgumentParser(description="Auto-Dubbing")
    parser.add_argument("--stage", metavar="stage", type=str, help="Etapa do Processo de Dublagem (ex. )")
    parser.add_argument("--working_dir", metavar="working_dir", type=str, help="Diretorio de Trabalho")
    parser.add_argument("--file", metavar="file", type=str, help="Arquivo de Input")
    parser.add_argument("--sample_size", metavar="sample_size", type=int, help="Tamanho da amostra de video em segundos")
    return parser.parse_args()


def voiceover(working_dir, file, sample_size):
    sample, audio = extract_sample(working_dir, file, sample_size)
    print('--samples gerados--')

    n, vid, spee  = get_speeches(working_dir, sample, audio)
    print('--pausas identificadas--')
    
    text = stt(working_dir, spee, batch=n+1)
    print('--audio transcrito--')
    
    translated_text = translate(working_dir, text)
    print('--texto traduzido--')
    
    n, new_audio = tts(working_dir, translated_text)
    print('--falas geradas--')

    file_name = 'voiceover.mp4'
    for i in range(n+1):
        vid_file = f'{i}_'+vid
        audio_file = f'{i}_'+new_audio
        new_file_name = f'{i}_'+file_name
        overrite_audio_sample(working_dir, vid_file, audio_file, new_file=new_file_name)
    print('--audios sobrescritos--')

    compose_video(working_dir, file_name, i+1)
    print('--fim--')
    

if __name__ == '__main__':
    args = get_args()
    voiceover(args.working_dir, args.file, args.sample_size)