import asyncio

from flask import Flask, request, jsonify, Response
from flask_restx import Api, Resource, fields, Namespace
import subprocess
from app import scanner, database
from app.database import save_scan, get_scan

app = Flask(__name__)
api = Api(app, version="1.0", title="API Scanner Vuln", description="API pour scanner les vulnérabilités")

ns = Namespace("scan", description="Fonctions de scan")
api.add_namespace(ns)

scan_model = api.model("ScanRequest", {
    "url": fields.String(required=True, description="URL à scanner")
})


@ns.route("/")
class Scan(Resource):
    @api.expect(scan_model)
    def post(self):
        data = api.payload
        html = asyncio.run(scanner.scrape_page_and_scan(data["url"]))
        test_id = asyncio.run(save_scan(data["url"], html["script"]))
        return {"message": "Faille identifiée", "test_id": test_id, "script": html["script"]}



@ns.route("/run/<string:test_id>")
class RunTest(Resource):
    def post(self, test_id):
        scan = asyncio.run(get_scan(test_id))
        if not scan:
            api.abort(404, "Test ID inconnu")

        script = scan.results

        if not isinstance(script, str):
            import json
            script = json.dumps(script)

        output = scanner.run_test_script(script)
        return {"output": output}


@api.route("/sql_injection")
class SqlInjection(Resource):
    @api.doc(params={"user_id": "ID utilisateur à simuler dans la requête SQL"})
    def get(self):
        user_id = request.args.get("user_id", "")
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        return {"query_executed": query, "result": "Fake result (juste une simulation)"}

from flask import request, Response

@api.route("/xss")
class XSS(Resource):
    def get(self):
        name = request.args.get("name", "")
        # Le contenu HTML avec un formulaire
        html_content = f"""
        <html>
          <body>
            <form method="get" action="/xss">
              <label for="name">Nom à afficher :</label>
              <input type="text" id="name" name="name" />
              <button type="submit">Afficher</button>
            </form>
            <hr/>
            <h1>Bonjour {name}</h1>
          </body>
        </html>
        """
        return Response(html_content, mimetype='text/html')


@api.route("/cmd_injection")
class CmdInjection(Resource):
    @api.doc(params={"host": "Hôte à pinger"})
    def get(self):
        host = request.args.get("host", "")
        try:
            result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True, timeout=5)
            return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "Timeout expired during ping"}

if __name__ == "__main__":
    app.run(debug=True)
