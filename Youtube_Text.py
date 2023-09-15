# !pip install pytube
# !pip install youtube-transcript-api
# !pip install git+https://github.com/openai/whisper.git
# !pip install jiwer


from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import whisper
import os

model=whisper.load_model("base")

link="https://www.youtube.com/watch?v=FENNwxNm9sM"

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

  # print(f'Video has been saved as {output_filename}')

  result = model.transcribe(os.path.join(output_dir, output_filename))
  return result['text']

def defaultsubtitles(link):
  try:
    video_id = link.split('v=')[1]
    # print("def")
    yt = YouTube(link)

    captions = YouTubeTranscriptApi.get_transcript(video_id)

    subtitles_text = ' '.join(caption['text'] for caption in captions)
    subtitles_text = subtitles_text.replace('\n', ' ')

    return subtitles_text
  except Exception as e:
    print("Issue with transcript API")
    return None
    # return str(e) 
  
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
        
print(extract_subtitles(link, model))