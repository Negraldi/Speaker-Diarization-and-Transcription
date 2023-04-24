# Speaker Diarization and Transcription
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](https://github.com/Negraldi/Speaker-Diarization-and-Transcription/blob/master/README.es.md)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Negraldi/Speaker-Diarization-and-Transcription/blob/main/notebook.ipynb)

This Python script provides an end-to-end solution for downloading a YouTube video's audio, transcribing the audio, and performing speaker diarization. The results are then analyzed to provide a consolidated output in a Pandas DataFrame.



## Dependencies

To run this script, you will need the following Python packages:

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

You can install the required packages using `pip`:

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

## Usage

To use this script, you will need to provide the YouTube video URL as an input to the `download_audio` function:

```python
download_audio('https://www.youtube.com/watch?v=AwJ19fO0Jpk', 'out.mp3')
```

Next, you will need to process the audio to obtain transcriptions and speaker diarization:

``` python
process_audio('out.mp3', 'out.json', 'output.lab')
```

Finally, you can analyze the transcriptions and diarization results:

```python
results_df, result_simp = analyze_transcriptions_and_diarization('out.json', 'output.lab')
```

## Functions

### `download_audio(url, output_filename)`

This function downloads and converts the audio of a YouTube video to a mono MP3 file.

**Arguments:**
- `url` (str): YouTube video URL.
- `output_filename` (str): Output MP3 file name.

### `process_audio(input_audio, output_json, output_lab)`

This function processes the audio file to obtain transcriptions and speaker diarization.

**Arguments:**
- `input_audio` (str): Input audio file name.
- `output_json` (str): Output JSON file name for transcriptions.
- `output_lab` (str): Output LAB file name for speaker diarization.

### `analyze_transcriptions_and_diarization(transcriptions_json, diarization_lab)`

This function analyzes the transcriptions and diarization results.

**Arguments:**
- `transcriptions_json` (str): JSON file with transcriptions.
- `diarization_lab` (str): LAB file with diarization results.

**Returns:**
- `pd.DataFrame`: DataFrame with analyzed results.

## Output

The output is a Pandas DataFrame that contains the analyzed results from the transcription and diarization process, including speaker identification, words, start and end times, probabilities, and voice percentages.
