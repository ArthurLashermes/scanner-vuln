import subprocess
from http.client import HTTPException


async def send_html_to_ai(html: str,url: str) -> str:

    prompt = f"""
        Voici un code HTML de page web :  
        {html}  
        et l'URL de la page en question : {url}  
        Génère uniquement un **script Python isolé** (sans explication, ni texte), qui permet de détecter, **à partir du seul contenu HTML fourni**, une éventuelle faille XSS, commande injection ou SQLi dans ce code HTML. Je ne veux que le code Python dans ta réponse.
        """

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout
    else:
        raise HTTPException(status_code=500, detail="Probleme réponse mistral")