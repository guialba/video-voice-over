# Video-Voice-Over
Protótipo de Dublagem de Vídeos PT-EN

# Table of contents
1. [Como usar](#uso)
2. [Documentação](#proposta)
    1. [Extração do áudio](#etapa_1)
    2. [Transcrever o áudio](#etapa_2)
    3. [Tradução](#etapa_3)
    4. [Sintetização de fala](#etapa_4)
    5. [Sincronizar áudios](#etapa_5)

# Como Usar <a name="uso"></a>
1. Após clonar o repositorio
2. Inicializar um ambiente virtual na raiz do projeto
3. instalar os pacotes do requirements.txt: 
Ex.
```
pip install -r requirements.txt
```
4. colocar o video de teste dentro da pasta files que será o diretório de trabalho.
5. Executar script "poc_voiceover.py" passando os parametros, working_dir, file, sample_size que correspondem ao diretório de trabalho, do arquivo de video que precisa estar no diretório de trabalho e do tamanho da amostra que será dublado, respectivamente.
Ex.
```
python poc_voiceover.py --working_dir files/ --file case_ai.mp4 --sample_size 200
```

Nota: o script voiceover.py pode ser executado também, e foi uma tentativa de realizar a sintetização de fala através de um modelo do hugging face e sincronização do áudio e vídeo, mas a qualidade do video final ficou a baixo da apresentada pelo protótipo inicial que usa a vós do google tradutor na dublagem. Acredito que com mais tempo, talvez, seria possivel aprimorar a qualidade dessa abordagem. 

# Documentação <a name="proposta"></a>
## Extrair o áudio de um arquivo de vídeo <a name="etapa_1"></a>
Para manipular o video e extrair o áudio é usado o Moviepy

## Transcrever o Áudio<a name="etapa_2"></a>
Por algum erro de conexão, não foi possível consumir o [modelo Whisper do Hugging Face](https://huggingface.co/openai/whisper-large-v3) então é necessário intalar o pacote da OpenIA localmente e para evitar ter que intalar manualmente a ferramenta do ffmpeg, também é necessário instalar o pacote SpeechRecognition que auxilia no uso do whisper.

## Tradução<a name="etapa_3"></a>
Inicialmente a ideia era usar [o modelo da Unicamp dispinível no Hugging Face](https://huggingface.co/unicamp-dl/translation-pt-en-t5) para traduzir o texto para inglês, mas após testar o tradutor do Whisper, decidi simplificar essa etapa.

## Sintetização de Fala<a name="etapa_4"></a>
Para sintetizar a fala do texto tradzido é usado uma das vozes masculina da base de dados do [CMU_ARCTIC](http://www.festvox.org/cmu_arctic/) que jé possui [um dataset de *embeddings* de suas vozes no Hugging Face](https://huggingface.co/datasets/Matthijs/cmu-arctic-xvectors) e é necessário consumir [o modelo da microsoft de Text To Speech também disponível no Hugging Face](https://huggingface.co/microsoft/speecht5_tts). 
O problema é que há um limite de tokens que o sintetizador aceita, assim seria necessário particionar o texto e sitentizer as partes separadas e depois montar o audio.
Para ganhar tempo e ter um protótio funcional, foi implementado uma forma de consumir a api de tradução do google através do modulo gTTS.

## Sincronizar Áudios<a name="etapa_5"></a>
Com o Librosa dá para fazer uma análise de spectograma e assim medir a energia e estabelecer as pausas para então segmentar a fala, e tentar sencronizar os trecho. Essa quebra do audio nas pausas, pode ser útil para lidar com o problema do limite de tokens na sintetização.

