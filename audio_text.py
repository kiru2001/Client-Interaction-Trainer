import whisper

def mark_pauses(transcription, pause_threshold=0.05):
    words = transcription['segments']
    highlighted_transcript = ""
    
    for i in range(len(words) - 1):
        highlighted_transcript += f"{words[i]['text']}[{words[i]['start']}-{words[i]['end']}]"
        pause_duration = words[i + 1]['start'] - words[i]['end']
        if pause_duration > pause_threshold:
            highlighted_transcript += "[PAUSE] "
  
    # highlighted_transcript += f"{words[-1]['text']}[{words[-1]['start']}-{words[-1]['end']}]"
    return highlighted_transcript

def return_text(path):
    model = whisper.load_model("base")
    result = model.transcribe(path,
                          temperature=0.0,
                          condition_on_previous_text=False,
                          word_timestamps=True)
    highlighted_transcript = mark_pauses(result)
    return highlighted_transcript






