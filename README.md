# Clean Sphere Analyzer
Clean Sphere Analyzer est l'un des modules de la futur application Clean Sphere. Ce répertoire Git contient le code d'un prototype qui peut être exécuté en local et ne reflète pas toutes les fonctionnalités de la solution définitive.

Ce prototype est fait en python construite avec Tkinter pour l'analyse et la détection de contenu inapproprié dans les tweets du réseau social X. Il utilise une API de génération de texte pour analyser et évaluer si les messages sont offensants, violents ou inappropriés.

# Fonctionnalités
Récupération de Tweets : Extraction des tweets d'un utilisateur via une API Twitter.
Analyse de Texte : Analyse automatique des tweets pour déterminer s'ils sont appropriés ou offensants, en utilisant un modèle de complétion de texte.
Interface Utilisateur (GUI) : Une interface graphique simple avec Tkinter permettant de lancer l'analyse et d'afficher les résultats.

# Prérequis pour lancer le projet
Python >= 3.9 installé.

Bibliothèques Python :

tkinter : Pour l'interface graphique.
requests : Pour interagir avec les API REST.
requests_oauthlib : Pour l'authentification OAuth.
http.client : Pour les appels API via HTTP.

Une solution au choix lancer un modèle d'IA
Par exemple: https://github.com/ggerganov/llama.cpp/blob/master/examples/main/README.md
Dans notre prototype nous utilisons le modèle mistral disponible à l'url : https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

Obtenir une clé d'API en créeant un compte sur : https://rapidapi.com/davethebeast/api/twitter241/playground/apiendpoint_e82a6196-d11d-430d-97a7-ee2aadaeecd7
Choisir l'ID d'un compte X dans notre cas nous utilisons le compte @Worshop25637 qui a l'ID 1845880416332603392

Remplacer ligne 23
    headers = {
        'x-rapidapi-key': "A_REMPLACER",
        'x-rapidapi-host': "A_REMPLACER"
    }
    conn.request("GET", "/user-tweets?user=A_REMPLACER&count=8", headers=headers)


Une fois le projet configuré il suffit de lancer le projet avec la commande: "python analyse.py".
Quand l'interface est ouverte, cliquez sur le bouton "Lancer l'analyse" pour récupérer les tweets et les analyser.


# Documentation

1. CompletionClient
Ce client permet d'envoyer des requêtes à un serveur d'API pour générer une réponse basée sur un modèle de complétion de texte. La méthode clé est post_completion, qui envoie un prompt avec des paramètres optionnels comme la température et le nombre de prédictions attendues.

python
Copier le code
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
2. get_comments()
Cette fonction utilise l'API Twitter pour extraire les derniers tweets d'un utilisateur spécifique. Elle est conçue pour fonctionner avec RapidAPI.

python
Copier le code
def get_comments():
    conn = http.client.HTTPSConnection("twitter241.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "VOTRE_API_KEY",
        'x-rapidapi-host': "twitter241.p.rapidapi.com"
    }
    conn.request("GET", "/user-tweets?user=1845880416332603392&count=8", headers=headers)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data)

    # Extraction des tweets
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

    return tweets

Auteur : Clean Sphere Team