import json
import os

def load_config_from_json(app, path="app/static/conf.json"):
    with open(path) as f:
        data = json.load(f)

    for item in data["configurations"]:
        key = item["key"]
        value = os.getenv(key, item.get("default"))

        if item.get("required") and value is None:
            raise RuntimeError(f"Missing config: {key}")

        app.config[key] = value
