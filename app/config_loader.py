import json
import os

def load_config_from_json(app, path="app/static/conf.json"):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    for item in data["configurations"]:
        key = item["key"]
        
        # Se a variável de ambiente existe, usa; senão usa default ou options
        value = os.getenv(key)
        if value is None:
            if "default" in item:
                value = item["default"]
            elif "options" in item:
                value = item["options"]
            else:
                value = None

        if item.get("required") and value is None:
            raise RuntimeError(f"Missing config: {key}")

        app.config[key] = value
