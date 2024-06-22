import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import whisper

def convert_mp4_to_mp3(mp4_file_path):
    video = VideoFileClip(mp4_file_path)
    mp3_file_path = os.path.splitext(mp4_file_path)[0] + '.mp3'
    video.audio.write_audiofile(mp3_file_path)
    return mp3_file_path

def split_mp3(mp3_file_path, segment_length=300000):
    audio = AudioSegment.from_mp3(mp3_file_path)
    duration = len(audio)
    segments = []
    for start_time in range(0, duration, segment_length):
        segment = audio[start_time:start_time + segment_length]
        segment_file_path = f"{mp3_file_path}_{start_time // 1000}.mp3"
        segment.export(segment_file_path, format="mp3")
        segments.append(segment_file_path)
    return segments

def transcribe_with_whisper(segment_files):
    model = whisper.load_model("large")
    transcriptions = []
    for segment in segment_files:
        result = model.transcribe(segment)
        transcriptions.append(result['text'])
    return transcriptions


# mp4_file_path = r"C:\Users\cheap\Downloads\Y2meta.app-【受かるのは誰？】グループディスカッションをノーカットでお送りします。【突破法】-(720p).mp4"
# mp3_file_path = convert_mp4_to_mp3(mp4_file_path)
mp3_file_path = r"D:\tmp\tmp.mp3"
print(f"Converted to MP3: {mp3_file_path}")

segment_files = split_mp3(mp3_file_path)
print(f"Segment files: {segment_files}")

transcriptions = transcribe_with_whisper(segment_files)
full_transcription = ' '.join(transcriptions)

print("Full Transcription:")
print(full_transcription)