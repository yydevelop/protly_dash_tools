import base64

encode_api_key = "c2stVzRCNmJsa1d5NlRQM2RpS2xKMUpUM0JsYmtGSnJYQXpmZ3FqT2tLUXdXdENQWmdP"
# api_key = base64.b64decode(api_key).decode('utf-8')

import os
import openai
import moviepy.editor as mp
import whisper

# APIキーの設定
openai.api_key = base64.b64decode(encode_api_key).decode("utf-8")


def convert_mp4_to_mp3(mp4_file_path):
	wav_file_path = os.path.splitext(mp4_file_path)[0] + ".mp3"
	audio = mp.AudioFileClip(mp4_file_path)
	audio.write_audiofile(wav_file_path)
	return wav_file_path


def transcribe_audio(wav_file_path):
	with open(wav_file_path, "rb") as audio_file:
		transcription = openai.Audio.transcribe("whisper-1", audio_file, language='ja')

	return transcription.text


def save_transcription_to_file(transcription, output_file_path):
	with open(output_file_path, "w", encoding="utf-8") as f:
		f.write(transcription)


if __name__ == "__main__":
	# mp4_file_path = input("mp4ファイルのパスを入力してください: ")
	# wav_file_path = convert_mp4_to_mp3(mp4_file_path)
	wav_file_path = r"C:\Users\cheap\Downloads\Y2meta.app-【受かるのは誰？】グループディスカッションをノーカットでお送りします。【突破法】-(720p).mp3"

	transcription = transcribe_audio(wav_file_path)
	print("音声文字起こしが完了しました。")
	print(transcription)

	# output_file_path = os.path.splitext(mp4_file_path)[0] + "_transcription.txt"
	# save_transcription_to_file(transcription, output_file_path)
	# print(f"音声文字起こしの結果が {output_file_path} に保存されました。")
