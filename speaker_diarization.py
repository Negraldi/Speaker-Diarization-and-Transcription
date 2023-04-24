mport os
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from pydub import AudioSegment
from pytube import YouTube
from shapely.geometry import LineString
from stable_whisper import load_model
from pyannote.audio import Pipeline

# Load the Stable Whisper model and Pyannote Pipeline
model = load_model('large-v2')
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="<<hugging_face_token>>")

def download_audio(url, output_filename):
    """
    Download and convert YouTube audio to a mono MP3 file.

    Args:
    url (str): YouTube video URL
    output_filename (str): Output MP3 file name
    """
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    temp_file = audio_stream.download(filename='temp')

    audio = AudioSegment.from_file(temp_file)
    audio = audio.set_channels(1)  # Set to mono
    audio.export(output_filename, format='mp3')

    os.remove(temp_file)
    print(f"Audio downloaded and converted successfully: {output_filename}")


def process_audio(input_audio, output_json, output_lab):
    """
    Process the audio file to obtain transcriptions and speaker diarization.

    Args:
    input_audio (str): Input audio file name
    output_json (str): Output JSON file name for transcriptions
    output_lab (str): Output LAB file name for speaker diarization
    """
    # Transcribe audio and save to JSON
    result = model.transcribe(input_audio, language="es", demucs=True, vad=True, regroup=False)
    result.save_as_json(output_json)

    # Perform speaker diarization and save to LAB
    diarization_result = pipeline(input_audio)
    with open(output_lab, "w") as rttm:
        diarization_result.write_lab(rttm)

def analyze_transcriptions_and_diarization(transcriptions_json, diarization_lab):
    """
    Analyze transcriptions and diarization results.

    Args:
    transcriptions_json (str): JSON file with transcriptions
    diarization_lab (str): LAB file with diarization results

    Returns:
    pd.DataFrame: DataFrame with analyzed results
    """
    with open(transcriptions_json, 'r') as file:
        data = json.load(file)
    
    wrd = pd.DataFrame(data['segments'])[['id', 'words']].explode('words')
    wrd = pd.concat([wrd.drop(['words'], axis=1), wrd['words'].apply(pd.Series)], axis=1)
    wrd['id2'] = range(len(wrd))

    voice = pd.read_csv(diarization_lab, header=None, delimiter=r" ")
    voice.columns = ['start', 'end', 'speaker']
    voice['id2'] = range(len(voice))

    wrd['geometry'] = wrd.apply(lambda row: LineString([(row['start'], 0), (row['end'], 0)]), axis=1)
    voice['geometry'] = voice.apply(lambda row: LineString([(row['start'], 0), (row['end'], 0)]), axis=1)
    wrd, voice = gpd.GeoDataFrame(wrd, geometry='geometry'), gpd.GeoDataFrame(voice, geometry='geometry')

    wrd['len'] = wrd.geometry.length
    inter = gpd.overlay(wrd, voice, how='union').query('not id.isnull()')
    inter = inter.sort_values(by='id2_2').sort_values(by='id2_1').reset_index()
    inter['p_voice'] = inter.geometry.length / inter.len
    inter = inter.query('not p_voice.isnull()')
    inter = inter[['id', 'id2_1', 'speaker', 'word', 'start_1', 'end_1', 'probability', 'p_voice']]
    inter['ord'] = (~inter.speaker.isnull()) * 100 + inter.probability * 10 + inter.p_voice
    inter = inter.groupby('id2_1', group_keys=False).apply(lambda x: x.nlargest(1, 'ord', keep='all')).reset_index()

    tmp = inter.groupby(['id', 'speaker']).apply(lambda x: {"sentence": ' '.join(x['word']),
                                                            "start_1": min(x['start_1']),
                                                            "end_1": max(x['end_1']),
                                                            "prob": np.exp(np.average(np.log(x['probability']))),
                                                            "p_voice": np.exp(np.average(np.log(x['p_voice'])))})
    tmp = tmp.apply(pd.Series).sort_values(by='start_1').reset_index(['id', 'speaker'])
    return inter,tmp

