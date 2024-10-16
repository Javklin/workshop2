import tkinter as tk
import requests
import json
from requests_oauthlib import OAuth1
import http.client

class CompletionResponse:
    def __init__(self, data):
        self.content = data['content']

    def get_content(self):
        return self.content

class CompletionClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_completion(self, prompt, temperature=0.0, n_predict=-1, stop=None):
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "n_predict": n_predict,
            "stop": stop if stop is not None else [],
        }
        response = requests.post(f"{self.base_url}/completion", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# Configuration de l'API
client = CompletionClient("http://127.0.0.1:8080")
systemPrompt = """
Tu es un assistant qui analyse du texte pour détecter si les messages qu'on t'envoie sont inapproprié (offensant, violent, cruel, méchant ou offensant).

Pour chaque message reçu, tu réponds en format JSON comme dans ces exemples

{
  "text_acceptable": true,
  "reason": ""
}

{
  "text_acceptable": false,
  "reason": "Explication ici."
}
"""

def get_comments():
    conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")
    #pour obtenir la cle d'API se créer un compte sur 
    #https://rapidapi.com/davethebeast/api/twitter241/playground/apiendpoint_e82a6196-d11d-430d-97a7-ee2aadaeecd7
    headers = {
        'x-rapidapi-key': "A_REMPLACER",
        'x-rapidapi-host': "A_REMPLACER"
    }
    conn.request("GET", "/user-tweets?user=A_REMPLACER&count=8", headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)

    # tableau pour stocker les "full_text" de la reponse api
    tweets = []
    instructions = json_data['result']['timeline']['instructions']

    for instruction in instructions:
        if 'entries' in instruction:
            entries = instruction['entries']
            for entry in entries:
                if 'content' in entry and 'itemContent' in entry['content']:
                    item_content = entry['content']['itemContent']
                    if 'tweet_results' in item_content:
                        tweet_results = item_content['tweet_results']['result']
                        if 'legacy' in tweet_results and 'full_text' in tweet_results['legacy']:
                            tweets.append(tweet_results['legacy']['full_text'])
    print(tweets)
    return(tweets)
        
def get_response():
    tweet_texts = get_comments()  
    #pour tester sans faire appel à l'API
    #tweet_texts = ["j'aime bien les hamburger", "j'ai frappé une personne sans raison", "Le sujet du worshop de 2024 est génial", "Je vais te briser les côtes mec"]
    for tweet in tweet_texts: 
        full_prompt = systemPrompt + tweet  + "Est-ce acceptable et approprié ?"
        result = client.post_completion(prompt=full_prompt, temperature=0.0, n_predict=100, stop=["}"])
        response = CompletionResponse(result)
        user_response = response.get_content()
        conversation_log.insert(tk.END, f"User: {tweet}\nResponse: {user_response}\n\n")
     
# la fenêtre principale
root = tk.Tk()
root.title("Clean Sphere Analyzer")
send_button = tk.Button(root, text="Lancer l'analyse", command=get_response)
send_button.pack()
conversation_log = tk.Text(root, width=60, height=20)
conversation_log.pack(pady=20)
root.mainloop()

