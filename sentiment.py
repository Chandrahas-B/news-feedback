from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from warnings import filterwarnings

filterwarnings('ignore')

model_name = "yangheng/deberta-v3-base-absa-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)


classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def sentiment(text,keywords):
  
  d = {}
  for keyword in keywords:
    d[keyword] = classifier(text, text_pair= keyword[0])
    
  return d

# text = ''
# with open('dummy.txt', 'r') as f:
#   text = f.readlines()  
  
  
# d = sentiment(text, ['Government', 'Prime Minister', 'National Food Security Act'])

# for k,v in d.items():
#   print(f"{k}: {v}")