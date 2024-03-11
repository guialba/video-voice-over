import speech_recognition as sr
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from datasets import load_dataset
import soundfile as sf
import torch

def assert_trials(trials, func):
    error = 0
    ok=False
    while not ok:
        try:
            sucess = func()
            ok=True
        except:
            error+=1
            ok = error >=trials
    return sucess




def stt(working_dir, audio_file, text_file='text.txt', translate=False, batch=1):
    r = sr.Recognizer()

    if batch == 1:
        with sr.AudioFile(working_dir + audio_file) as source:
            audio = r.record(source)
        text = r.recognize_whisper(audio, language='portuguese', translate=translate)
        with open(working_dir + text_file, 'w') as f:
            f.write(text)
    else:
        audio_samples = []
        for i in range(batch):
            with sr.AudioFile(working_dir + f'{i}_'+audio_file) as source:
                audio = r.record(source)
                audio_samples.append(audio)
        text = [r.recognize_whisper(audio, language='portuguese', translate=translate) for audio in audio_samples]
        with open(working_dir + text_file, 'w') as f:
            for s in text:
                f.write(s+'\n')

    return text_file


def tts(working_dir, text_file, audio_file='new_audio.wav', max_error=15):
    synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")
    embeddings_dataset = assert_trials(max_error, lambda: load_dataset("Matthijs/cmu-arctic-xvectors", split="validation"))
    speaker_embedding = torch.tensor(embeddings_dataset[512]["xvector"]).unsqueeze(0)

    with open(working_dir + text_file, 'r') as f:
        lines = [line.rstrip() for line in f]

    for i, text in enumerate(lines):
        speech = assert_trials(max_error, lambda: synthesiser(text, forward_params={"speaker_embeddings": speaker_embedding}))
        sf.write(working_dir + f'{i}_' + audio_file, speech["audio"], samplerate=speech["sampling_rate"])

    return i, audio_file 


def translate(working_dir, text_file, new_text_file='translated.txt'):
    tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/translation-pt-en-t5")
    model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/translation-pt-en-t5")
    pten_pipeline = pipeline('text2text-generation', model=model, tokenizer=tokenizer)

    with open(working_dir + text_file, 'r') as f:
        lines = [line.rstrip() for line in f]

    translations = [pten_pipeline(f"translate Portuguese to English: {line}")[0]['generated_text'] for line in lines]

    with open(working_dir + new_text_file, 'w') as f:
        for s in translations:
            f.write(s+'\n')

    return new_text_file