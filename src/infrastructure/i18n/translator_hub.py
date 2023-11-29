"""
Объект интернационализации для работы с locales
"""

from fluentogram import FluentTranslator, TranslatorHub
from fluent_compiler.bundle import FluentBundle

translator_hub = TranslatorHub(
    {
        "ru": ("ru", "en"),
        "en": ("en",)
    },
    [
        FluentTranslator(
            "en",
            translator=FluentBundle.from_files("en", filenames=[
                "src/infrastructure/i18n/locales/en.ftl"])),
        FluentTranslator(
            "ru",
            translator=FluentBundle.from_files("ru", filenames=[
                'src/infrastructure/i18n/locales/ru.ftl']))
    ],
)
