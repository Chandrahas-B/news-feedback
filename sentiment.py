from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

model_name = "yangheng/deberta-v3-base-absa-v1.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def sentiment(text,keywords):
  
  d = {}
  for keyword in keywords:
    d[keyword] = classifier(text, text_pair= keyword[0])
    
  return d