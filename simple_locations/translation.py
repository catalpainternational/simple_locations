from modeltranslation.translator import TranslationOptions, translator

from .models import Area, AreaType


class AreaNameTranslations(TranslationOptions):
    fields = ("name",)


class AreaTypeTranslations(TranslationOptions):
    fields = ("name",)


translator.register(Area, AreaNameTranslations)
translator.register(AreaType, AreaTypeTranslations)
