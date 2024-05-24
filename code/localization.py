import os
import json

class Localization:
    locales = {}

    @staticmethod
    def load_locales(locale_dir):
        for filename in os.listdir(locale_dir):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                with open(os.path.join(locale_dir, filename), 'r', encoding='utf-8') as f:
                    Localization.locales[lang_code] = json.load(f)
        return Localization.locales

    @staticmethod
    def get_message(guild_id, key):
        with open('code/config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        guild_config = config.get(str(guild_id), {})
        language = guild_config.get('language', 'en')
        return Localization.locales.get(language, {}).get(key, key)
