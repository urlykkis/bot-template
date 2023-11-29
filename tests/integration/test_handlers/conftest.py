import asyncio
import pytest
import os

from pathlib import Path

from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle

from tests.fixtures.bot_fixtures import memory_storage, bot, dispatcher, cls_bot, cls_dp

BASE_DIR = Path(__file__).parent


base_dir = os.path.dirname(os.path.abspath(__file__))
three_levels_up = os.path.abspath(os.path.join(base_dir, os.pardir, os.pardir, os.pardir))
locales = os.path.abspath(os.path.join(three_levels_up, 'src', 'infrastructure', 'i18n', 'locales'))
en_locale = os.path.abspath(os.path.join(locales, 'en.ftl'))
ru_locale = os.path.abspath(os.path.join(locales, 'ru.ftl'))


@pytest.fixture(scope="session")
def translator_hub():
    hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en",)
        },
        [
            FluentTranslator(
                "en",
                translator=FluentBundle.from_files("en", filenames=[en_locale])),
            FluentTranslator(
                "ru",
                translator=FluentBundle.from_files("ru", filenames=[ru_locale]))
        ],
    )
    return hub


@pytest.fixture(scope="session")
def i18n(translator_hub):
    return translator_hub.get_translator_by_locale("ru")


@pytest.fixture(scope="class")
def cls_i18n(request, i18n):
    request.cls.i18n = i18n
