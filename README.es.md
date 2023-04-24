# Diarización de hablantes y transcripción
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Negraldi/Speaker-Diarization-and-Transcription/blob/master/notebook_es.ipynb)

Este script de Python proporciona una solución de extremo a extremo para descargar el audio de un video de YouTube, transcribir el audio y realizar la diarización de hablantes. Los resultados se analizan para proporcionar una salida consolidada en un DataFrame de Pandas.

## Dependencias

Para ejecutar este script, necesitarás los siguientes paquetes de Python:

- `os`
- `json`
- `pandas`
- `numpy`
- `geopandas`
- `pydub`
- `pytube`
- `shapely`
- `stable_whisper`
- `pyannote.audio`

Puedes instalar los paquetes necesarios usando `pip`:

``` bash
pip install pytube
pip install pydub
pip install torch
pip install torchaudio
pip install -U demucs
pip install -U stable-ts
pip install geopandas
pip install -qq https://github.com/pyannote/pyannote-audio/archive/refs/heads/develop.zip
```

## Uso

Para usar este script, debes proporcionar la URL del video de YouTube como entrada a la función `download_audio`:

``` python
download_audio('https://www.youtube.com/watch?v=AwJ19fO0Jpk', 'out.mp3')
```

A continuación, debes procesar el audio para obtener transcripciones y diarización de hablantes:

``` python
process_audio('out.mp3', 'out.json', 'output.lab')
```

Finalmente, puedes analizar los resultados de transcripción y diarización:

``` python
results_df, result_simp = analyze_transcriptions_and_diarization('out.json', 'output.lab')
```

## Funciones

### `download_audio(url, output_filename)`

Esta función descarga y convierte el audio de un video de YouTube a un archivo MP3 mono.

**Argumentos:**
- `url` (str): URL del video de YouTube.
- `output_filename` (str): Nombre del archivo MP3 de salida.

### `process_audio(input_audio, output_json, output_lab)`

Esta función procesa el archivo de audio para obtener transcripciones y diarización de hablantes.

**Argumentos:**
- `input_audio` (str): Nombre del archivo de audio de entrada.
- `output_json` (str): Nombre del archivo JSON de salida para las transcripciones.
- `output_lab` (str): Nombre del archivo LAB de salida para la diarización de hablantes.

### `analyze_transcriptions_and_diarization(transcriptions_json, diarization_lab)`

Esta función analiza los resultados de transcripción y diarización.

**Argumentos:**
- `transcriptions_json` (str): Archivo JSON con las transcripciones.
- `diarization_lab` (str): Archivo LAB con los resultados de diarización de hablantes.

**Retorna:**
- `pd.DataFrame`: DataFrame con los resultados analizados.

## Salida

La salida es un DataFrame de Pandas que contiene los resultados analizados del proceso de transcripción y diarización, incluyendo la identificación de hablantes, palabras, tiempos de inicio y finalización, probabilidades y porcentajes de voz.
