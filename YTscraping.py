from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
import os
from sentiment import sentiment
from time import time
import json

model=whisper.load_model("base")

links = ["https://www.youtube.com/watch?v=e10pNlG-PMU", "https://www.youtube.com/watch?v=agekEF0fgl4"]

def whispertranscribe(link,model):
  try:
    yt=YouTube(link)
  except:
    print("Connection Error")

    # print("whis")
  yt.streams.filter(file_extension='mp4')
  stream=yt.streams.get_by_itag(139)
  output_dir = './'
  base_filename = 'output_video'
  existing_files = os.listdir(output_dir)
  counter = 1
  output_filename = f'{base_filename}{counter}.mp4'

  while output_filename in existing_files:
      counter += 1
      output_filename = f'{base_filename}{counter}.mp4'
  stream.download(output_path=output_dir, filename=output_filename)

  result = model.transcribe(os.path.join(output_dir, output_filename))
  return result['text']

def defaultsubtitles(link):
  try:
    video_id = link.split('v=')[1]
    yt = YouTube(link)

    captions = YouTubeTranscriptApi.get_transcript(video_id)

    subtitles_text = ' '.join(caption['text'] for caption in captions)
    subtitles_text = subtitles_text.replace('\n', ' ')

    return subtitles_text
  except Exception as e:
    print("Issue with transcript API")
    return None
  
def extract_subtitles(link, model):
    default_subtitles = defaultsubtitles(link)

    if default_subtitles:
        return default_subtitles

    else:
        try:
            print("Default Subtitles not found")
            transcribed_text = whispertranscribe(link, model)
            return transcribed_text
        except Exception as e:
            return str(e)



start = time()
jsons = []

def json_for_kv_and_text(text, link):
  k_v = sentiment(text, ['Government', 'India', 'Society', 'Bureau'])
  jsonContent = {}
  jsonContent['id'] = len(jsons)
  jsonContent['content'] = text
  jsonContent['tonality'] = k_v['Government'][0]['label']
  jsonContent['time'] = time()
  jsonContent['article'] = f'<a href="{link}"> Click here </a>'
  jsons.append(jsonContent)

for link in links:
  text = extract_subtitles(link, model)
  json_for_kv_and_text(text, link)


    
    

with open('scraped/youtubescraping.json', 'w') as f:
  json.dump(jsons, f)
  
  
end = time()

print(f"\n\n\n\t Time taken: {end-start}")




# try:
#   yt=YouTube(link)
# except:
#   print("Connection Error")

#   # print("whis")
# yt.streams.filter(file_extension='mp4')
# stream=yt.streams.get_by_itag(139)
# output_dir = './'
# base_filename = 'output_video'
# existing_files = os.listdir(output_dir)
# counter = 1
# output_filename = f'{base_filename}{counter}.mp4'

# while output_filename in existing_files:
#     counter += 1
#     output_filename = f'{base_filename}{counter}.mp4'
# stream.download(output_path=output_dir, filename=output_filename)

# result = model.transcribe(os.path.join(output_dir, output_filename))
# print(result['text'])