from typing import List
import openai
import requests
from enum import Enum

def stripall(text):
    return text.strip(" \n\t\r.,:;!?()[]{}<>")

class OpenAIModelTypes(Enum):
  davinci = 'text-davinci-002'
  curie = 'text-curie-001'
  babbage = 'text-babbage-001'
  ada = 'text-ada-001'

class OpenAIAPI():
    def __init__(self, API_KEY):
        openai.api_key = API_KEY
        self.used_tokens = 0
    def prompt(self, prompt, model : OpenAIModelTypes=OpenAIModelTypes.curie,
               temperature=0.7, max_tokens=256, frequency_penalty=0, presence_penalty=0):
        inference = openai.Completion.create(
          model=model.value,
          prompt=prompt,
          temperature=temperature,
          max_tokens=max_tokens,
          top_p=1,
          frequency_penalty=frequency_penalty,
          presence_penalty=presence_penalty
        )
        
        self.used_tokens += inference['usage']['total_tokens']
        
        answer = inference['choices'][0]['text']
        return answer


class SentanceSimilarityAPI:
  def __init__(self, API_KEY):
    self.API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    self.headers = {"Authorization": f"Bearer {API_KEY}"}

  def query(self, source_sentence: str, sentences: List[str]):
    payload = {
      "inputs": {
        "source_sentence": source_sentence,
        "sentences": sentences
      },
    }
    similarity_values = requests.post(self.API_URL, headers=self.headers, json=payload).json()
    return sorted(list(zip(sentences, similarity_values)), key=lambda x: x[1], reverse=True)