from speaker_diarization import download_audio, process_audio, analyze_transcriptions_and_diarization

# Download and convert YouTube audio
download_audio('https://www.youtube.com/watch?v=AwJ19fO0Jpk', 'out.mp3')

# Process the audio to obtain transcriptions and speaker diarization
process_audio('out.mp3', 'out.json', 'output.lab')

# Analyze the transcriptions and diarization results
results_df, result_simp = analyze_transcriptions_and_diarization('out.json', 'output.lab')

# Print the analyzed results
print(results_df)
print(result_simp)
