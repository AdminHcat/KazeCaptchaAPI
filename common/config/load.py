import configparser
import os


def load_config():
    config = configparser.ConfigParser()
    with open("config.ini", "r", encoding="utf-8") as f:
        config.read_file(f)
    app_config = config["app"]
    debug = os.getenv("FLASK_DEBUG", app_config.getboolean("DEBUG"))
    port = int(os.getenv("FLASK_PORT", app_config.get("PORT")))
    max_content_length = int(
        os.getenv(
            "FLASK_MAX_CONTENT_LENGTH",
            app_config.get("MAX_CONTENT_LENGTH"),
        )
    )
    return debug, port, max_content_length
