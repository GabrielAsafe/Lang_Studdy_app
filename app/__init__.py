from flask import Flask
from .config_loader import load_config_from_json
from .extensions import init_extensions
from .routes import register_routes


def create_app():
    app = Flask(__name__)

    load_config_from_json(app)

    app.config.update({
        "LANG": "pt",
        "LEXICON": "omw-pt",
        "LANGEN": "en",
        "LEXICONEN": "oewn",
        "LANGDE": "de",
        "LEXICONDE": "odenet"
    })
    

    init_extensions(app)
    register_routes(app)

    return app
