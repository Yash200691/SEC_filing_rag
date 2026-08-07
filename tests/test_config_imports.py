import importlib


def test_config_exports_expected_names():
    config = importlib.import_module("config")

    assert hasattr(config, "EMBEDDING_MODEL")
    assert hasattr(config, "QDRANT_URL")
    assert hasattr(config, "COLLECTION_NAME")
    assert hasattr(config, "settings")
