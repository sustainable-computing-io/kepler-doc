"""Expose data/adopters.yaml to templates as `config.extra.adopters`."""

import os

import yaml


def on_config(config):
    path = os.path.join(os.path.dirname(config.config_file_path), "data", "adopters.yaml")
    with open(path, encoding="utf-8") as f:
        companies = yaml.safe_load(f)["adopters"]["companies"]
    config.extra["adopters"] = sorted(companies, key=lambda c: c["name"].lower())
    return config
