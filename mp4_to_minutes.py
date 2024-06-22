import os
import time
import openai
import moviepy.editor as mp
from pydub import AudioSegment

#mp4をmp3に変換し、mp3のファイルパスを返す
def convert_mp4_to_mp3(mp4_file_path):
    mp3_file_path = os.path.splitext(mp4_file_path)[0] + '.mp3'
    audio = mp.AudioFileClip(mp4_file_path)
    audio.write_audiofile(mp3_file_path)
    time.sleep(1)
    return mp3_file_path

#mp3ファイルを文字起こしし、テキストを返す
def transcribe_audio(mp3_file_path):
    with open(mp3_file_path, 'rb') as audio_file:
        transcription = openai.Audio.transcribe("whisper-1", audio_file, language='ja')

    return transcription.text

#テキストを保存
def save_text_to_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(text)

#mp3ファイルを分割し、保存し、ファイルリストを返す
def split_audio(mp3_file_path, interval_ms, output_folder):
    if not os.path.isfile(mp3_file_path):
    	print(f"File does not exist: {mp3_file_path}")
    audio = AudioSegment.from_file(mp3_file_path)
    file_name, ext = os.path.splitext(os.path.basename(mp3_file_path))

    mp3_file_path_list = []

    n_splits = len(audio) // interval_ms
    for i in range(n_splits + 1):
        #開始、終了時間
        start = i * interval_ms
        end = (i + 1) * interval_ms
        #分割
        split = audio[start:end]
        #出力ファイル名
        output_file_name = output_folder + os.path.splitext(mp3_file_path)[0] + "_" + str(i) + ".mp3"
        #出力
        split.export(output_file_name, format="mp3")

        #音声ファイルリストに追加
        mp3_file_path_list.append(output_file_name)

    #音声ファイルリストを出力
    return mp3_file_path_list

mp4_file_path = r"C:\Users\cheap\Downloads\Y2meta.app-【受かるのは誰？】グループディスカッションをノーカットでお送りします。【突破法】-(720p).mp4"

# mp3_file_path = convert_mp4_to_mp3(mp4_file_path)
mp3_file_path = r"C:\Users\cheap\Downloads\Y2meta.app-【受かるのは誰？】グループディスカッションをノーカットでお送りします。【突破法】-(720p).mp3"

output_folder = "./output/"
interval_ms = 480_000 # 60秒 = 60_000ミリ秒

mp3_file_path_list = split_audio(mp3_file_path, interval_ms, output_folder)

transcription_list = []
for mp3_file_path in mp3_file_path_list:
    transcription = transcribe_audio(mp3_file_path)

    transcription_list.append(transcription)

    output_file_path = os.path.splitext(mp3_file_path)[0] + '_transcription.txt'

pre_summary = ""
for transcription_part in transcription_list:
    prompt = """
    あなたは、プロの要約作成者です。
    以下の制約条件、内容を元に要点をまとめてください。

    # 制約条件
    ・要点をまとめ、簡潔に書いて下さい。
    ・誤字・脱字があるため、話の内容を予測して置き換えてください。

    # 内容
    """ + transcription_part

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.0,
    )

    pre_summary += response['choices'][0]['message']['content']

    time.sleep(60)

prompt = """
あなたは、プロの議事録作成者です。
以下の制約条件、内容を元に要点をまとめ、議事録を作成してください。

# 制約条件
・要点をまとめ、簡潔に書いて下さい。
・誤字・脱字があるため、話の内容を予測して置き換えてください。
・見やすいフォーマットにしてください。

# 内容
""" + pre_summary


print("議事録を作成中です...")
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {'role': 'user', 'content': prompt}
    ],
    temperature=0.0,
)

output_file_path = os.path.splitext(mp4_file_path)[0] + '_mitunes.txt'
save_text_to_file(response['choices'][0]['message']['content'], output_file_path)
