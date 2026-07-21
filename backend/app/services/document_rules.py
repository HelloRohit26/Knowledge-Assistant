import yaml

from pathlib import Path


RULE_FILE = (
    Path(__file__)
    .parent.parent
    / "config"
    / "document_rules.yaml"
)


with open(
    RULE_FILE,
    "r",
    encoding="utf-8"
) as f:

    RULES = yaml.safe_load(f)


def apply_document_rules(metadata):

    category = metadata.document_category

    config = RULES["categories"].get(
        category,
        RULES["default"]
    )

    metadata.authority_score = config["authority_score"]

    metadata.is_official = config["is_official"]

    return metadata