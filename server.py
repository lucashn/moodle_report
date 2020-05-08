import sys
from io import StringIO, TextIOWrapper

from flask import Flask, render_template, request, send_file, make_response
from werkzeug.utils import secure_filename

import moodle_report

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main.html")


@app.route("/enviar", methods=["POST"])
def enviar():
    arq = TextIOWrapper(request.files["log"], encoding='utf8')

    try:
        out = StringIO()
        sys.stdout = out
        moodle_report.process(arq)
        sys.stdout = sys.__stdout__

        return render_template("main.html", output=out.getvalue())
    except Exception as e:
        return render_template("main.html", output=f"Arquivo inválido ({e})")

# utilizado somente quando chamado via python server.py, não via gunicorn
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host="0.0.0.0")
