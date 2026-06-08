import importlib


def test_settings_falls_back_when_database_url_is_blank(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "")

    import app.config as config

    reloaded = importlib.reload(config)

    assert reloaded.settings.database_url == "postgresql://postgres:root@localhost:5432/project_mgmt"
