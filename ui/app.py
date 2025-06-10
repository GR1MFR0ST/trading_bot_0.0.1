from flask import Flask, render_template
from config import Config
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    """Render the dashboard homepage."""
    config = Config()
    return render_template("index.html", assets=config.ASSETS)

@app.route("/settings")
def settings():
    """Render the settings page."""
    return render_template("settings.html")

@app.route("/performance")
def performance():
    """Render the performance page."""
    return render_template("performance.html")

@app.route("/builder")
def builder():
    """Render the custom strategy builder page."""
    return render_template("builder.html")

@app.route("/social")
def social():
    """Render the social trading page."""
    return render_template("social.html")

if __name__ == "__main__":
    logger.info("Starting Flask app on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)