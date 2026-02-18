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


def save_config_on_Jsons(current_app, data):
        config_path = os.path.join(current_app.root_path, "static", "conf.json")

        with open(config_path, "r") as f:
            config = json.load(f)

        for item in config["configurations"]:
            if item["key"] == "TARGET_LANGUAGE":
                item["default"] = data["TARGET_LANGUAGE"]
            if item["key"] == "BASE_LANGUAGE":
                item["default"] = data["BASE_LANGUAGE"]
            if item["key"] == "CHOOSEN_VOICE":
                item["default"] = data["CHOOSEN_VOICE"]
            
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)