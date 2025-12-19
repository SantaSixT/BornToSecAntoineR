import requests
from bs4 import BeautifulSoup
import time
import sys

# URL de base
ROOT_URL = "http://192.168.10.135/.hidden/"

# On utilise une SESSION pour éviter l'erreur [Errno 99]
session = requests.Session()

# On mémorise les messages déjà vus pour ne pas spammer
seen_messages = set()

def scan_directory(url):
    try:
        # Petit délai pour laisser respirer le système
        # time.sleep(0.05)

        response = session.get(url)

        # Si la page plante, on passe
        if response.status_code != 200:
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # On cherche tous les liens
        for link in soup.find_all("a"):
            href = link.get("href")

            if href == "../":
                continue

            # Si c'est un dossier, on descend dedans
            if href.endswith("/"):
                scan_directory(url + href)

            # Si c'est le fichier README
            elif href == "README":
                r = session.get(url + href)
                content = r.text.strip()

                # On cherche un chiffre (les messages bidons n'ont que des lettres souvent)
                # Le flag a souvent des chiffres ou ressemble à un hash
                if any(char.isdigit() for char in content):
                    print(f"\n[!!!] BINGO - FLAG POTENTIEL TROUVÉ :")
                    print(f"      Source : {url}{href}")
                    print(f"      Contenu : {content}\n")
                    # On peut arrêter le script ici si on est sûr
                    # sys.exit()

                elif content not in seen_messages:
                    print(f"[+] Message type trouvé : {content}")
                    seen_messages.add(content)

    except Exception as e:
        print(f"[!] Erreur sur {url} : {e}")
        # En cas d'erreur, on attend un peu et on continue
        time.sleep(1)

print("--- Reprise du scan (Mode stable) ---")
scan_directory(ROOT_URL)
