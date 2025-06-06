import requests
from app.ai_client import send_html_to_ai
import subprocess
import tempfile
import sys

async def scrape_page_and_scan(url: str) -> dict:
    r = requests.get(url)
    html = r.text

    script = await send_html_to_ai(html,url)
    return {"script": script}


def run_test_script(script: str) -> str:
    cleaned_script = script.strip().strip('\'"')
    if cleaned_script.startswith("```python"):
        cleaned_script = cleaned_script.removeprefix("```python").strip()
    if cleaned_script.endswith("```"):
        cleaned_script = cleaned_script.removesuffix("```").strip()

    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=True) as tmp:
        tmp.write(cleaned_script)
        tmp.flush()
        try:
            result = subprocess.run(
                [sys.executable, tmp.name],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Erreur d'exécution : {result.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "Erreur : le script a dépassé le temps d'exécution autorisé."
