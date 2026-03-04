TEAMS = {
    "tech": {"name": "Тех отдел", "emoji": "\u2699\ufe0f"},
    "design": {"name": "Диз отдел", "emoji": "\U0001f3a8"},
}

TEMPLATES = {
    "keitaro_integration": {
        "team": "tech",
        "name": "Интеграция ленда",
        "description": "Создание / интеграция ленда и преленда",
        "sections": [
            {
                "title": "Тип сайта",
                "fields": [
                    {"key": "site_type", "label": "Тип сайта", "type": "multi_select", "required": True,
                     "options": ["Преленд", "Ленд", "Спасибо страница", "Вайт", "Проклоленд"]},
                ],
            },
            {
                "title": "Тип задачи",
                "fields": [
                    {"key": "task_type", "label": "Тип задачи", "type": "select", "required": True,
                     "options": [
                         "Сделать ленд с нуля (фигма)",
                         "Сделать с нуля или выкачать (скрины/идеи)",
                         "Переделать оффер существующий (ссылка в кт)",
                     ]},
                ],
            },
            {
                "title": "Офис",
                "fields": [
                    {"key": "office", "label": "Офис", "type": "select", "required": True,
                     "options": ["1 (внешний)", "1 (внутренний)", "2", "3"]},
                ],
            },
            {
                "title": "Данные интеграции",
                "fields": [
                    {"key": "offer_crm", "label": "Название оффера в CRM", "type": "text", "required": True, "placeholder": ""},
                    {"key": "offer_kt", "label": "Название оффера в КТ", "type": "text", "required": True, "placeholder": ""},
                    {"key": "geo", "label": "Гео", "type": "text", "required": True, "placeholder": "MY, NO, JP..."},
                    {"key": "lang", "label": "Язык", "type": "text", "required": True, "placeholder": "EN, RU..."},
                    {"key": "vertical", "label": "Вертикаль", "type": "text", "required": False, "placeholder": "инвест"},
                    {"key": "user_id_crm", "label": "Юзер ID в CRM", "type": "text", "required": False, "placeholder": ""},
                    {"key": "thankyou_id", "label": "Id спасибо страницы", "type": "text", "required": False, "placeholder": "если есть"},
                ],
            },
            {
                "title": "Референсы",
                "fields": [
                    {"key": "reference", "label": "Референс", "type": "text", "required": False, "placeholder": "ссылка на референс"},
                    {"key": "figma_url", "label": "Figma / дизайн", "type": "text", "required": False, "placeholder": "ссылка на макет"},
                    {"key": "assets", "label": "Архив ассетов", "type": "file", "required": False, "placeholder": "ZIP или ссылка"},
                    {"key": "telegraph_text", "label": "Телеграф", "type": "textarea", "required": False, "placeholder": "Напиши текст — опубликуется на telegra.ph автоматом"},
                ],
            },
            {
                "title": "Сроки и приоритет",
                "fields": [
                    {"key": "deadline", "label": "Дедлайн", "type": "text", "required": False, "placeholder": "завтра, 15.03, ASAP..."},
                    {"key": "priority", "label": "Приоритет", "type": "select", "required": True,
                     "options": ["Очень срочно", "Стандартная таска"]},
                ],
            },
        ],
    },
    "design_static": {
        "team": "design",
        "name": "Статика (баннер/креатив)",
        "description": "Статичный креатив для рекламы",
        "sections": [
            {
                "title": "Приоритет и тип",
                "fields": [
                    {"key": "vertical", "label": "Вертикаль", "type": "select", "required": True,
                     "options": ["Инвест", "Чардж"]},
                    {"key": "priority", "label": "Приоритет", "type": "select", "required": True,
                     "options": ["Очень срочно", "Стандартная таска"]},
                ],
            },
            {
                "title": "Основные данные",
                "fields": [
                    {"key": "aspect_ratio", "label": "Расширение", "type": "multi_select", "required": True,
                     "options": ["1:1", "16:9 (горизонтальный)", "9:16 (вертикальный)"]},
                    {"key": "custom_ratio", "label": "Указать свой формат", "type": "text", "required": False, "placeholder": "если нестандартный"},
                    {"key": "lang", "label": "Язык", "type": "text", "required": True, "placeholder": "EN, RU, MY..."},
                    {"key": "currency", "label": "Валюта", "type": "text", "required": False, "placeholder": "USD, MYR..."},
                    {"key": "geo", "label": "ГЕО", "type": "text", "required": True, "placeholder": "MY, NO, JP..."},
                ],
            },
            {
                "title": "Крео",
                "fields": [
                    {"key": "creo_type", "label": "Тип крео", "type": "select", "required": True,
                     "options": ["Универсальное без оффера", "С оффером"]},
                    {"key": "offer_url", "label": "Ссылка на оффер", "type": "text", "required": False, "placeholder": "если с оффером"},
                ],
            },
            {
                "title": "Логотип оффера на крео",
                "fields": [
                    {"key": "logo", "label": "Логотип", "type": "select", "required": True,
                     "options": ["Да", "Нет", "Оба варианта"]},
                ],
            },
            {
                "title": "Текст для банера",
                "fields": [
                    {"key": "banner_text", "label": "Текст", "type": "textarea", "required": False, "placeholder": "Написать тут..."},
                ],
            },
            {
                "title": "Персонаж",
                "fields": [
                    {"key": "character", "label": "Описание персонажа", "type": "textarea", "required": False, "placeholder": "Какой персонаж нужен для крео..."},
                ],
            },
            {
                "title": "Количество",
                "fields": [
                    {"key": "quantity", "label": "Количество в шт", "type": "text", "required": True, "placeholder": "5"},
                ],
            },
            {
                "title": "Референсы",
                "fields": [
                    {"key": "reference", "label": "Референс", "type": "text", "required": False, "placeholder": "ссылка на похожее"},
                    {"key": "assets", "label": "Архив", "type": "file", "required": False, "placeholder": "ZIP или картинку"},
                ],
            },
            {
                "title": "Доп. пожелания",
                "fields": [
                    {"key": "extra", "label": "Пожелания", "type": "textarea", "required": False, "placeholder": "Как видишь, от себя дополнения..."},
                ],
            },
        ],
    },
    "design_motion": {
        "team": "design",
        "name": "Моушен (видео)",
        "description": "Видео креатив для рекламы",
        "sections": [
            {
                "title": "Приоритет и тип",
                "fields": [
                    {"key": "vertical", "label": "Вертикаль", "type": "select", "required": True,
                     "options": ["Инвест", "Чардж"]},
                    {"key": "priority", "label": "Приоритет", "type": "select", "required": True,
                     "options": ["Очень срочно", "Стандартная таска"]},
                ],
            },
            {
                "title": "Основные данные",
                "fields": [
                    {"key": "aspect_ratio", "label": "Расширение", "type": "multi_select", "required": True,
                     "options": ["1:1", "16:9 (горизонтальный)", "9:16 (вертикальный)"]},
                    {"key": "custom_ratio", "label": "Указать свой формат", "type": "text", "required": False, "placeholder": "если нестандартный"},
                    {"key": "lang", "label": "Язык", "type": "text", "required": True, "placeholder": "EN, RU, MY..."},
                    {"key": "currency", "label": "Валюта", "type": "text", "required": False, "placeholder": "USD, MYR..."},
                    {"key": "geo", "label": "ГЕО", "type": "text", "required": True, "placeholder": "MY, NO, JP..."},
                ],
            },
            {
                "title": "Крео",
                "fields": [
                    {"key": "creo_type", "label": "Тип крео", "type": "select", "required": True,
                     "options": ["Универсальное без оффера", "С оффером"]},
                    {"key": "offer_url", "label": "Ссылка на оффер", "type": "text", "required": False, "placeholder": "если с оффером"},
                ],
            },
            {
                "title": "Логотип",
                "fields": [
                    {"key": "logo", "label": "Логотип", "type": "select", "required": True,
                     "options": ["Да", "Нет", "Оба варианта"]},
                ],
            },
            {
                "title": "Озвучка текста",
                "fields": [
                    {"key": "voiceover", "label": "Озвучка", "type": "select", "required": True,
                     "options": ["Да", "Нет", "Оба варианта"]},
                ],
            },
            {
                "title": "Текст для видео",
                "fields": [
                    {"key": "video_text", "label": "Текст для озвучки", "type": "textarea", "required": False, "placeholder": "Прописать текст для озвучки..."},
                ],
            },
            {
                "title": "Количество",
                "fields": [
                    {"key": "quantity", "label": "Количество в шт", "type": "text", "required": True, "placeholder": "5"},
                ],
            },
            {
                "title": "Субтитры",
                "fields": [
                    {"key": "subtitles", "label": "Субтитры", "type": "select", "required": True,
                     "options": ["Вариант с субтитрами", "Вариант без них", "Оба варианта"]},
                ],
            },
            {
                "title": "Музыка на фон",
                "fields": [
                    {"key": "music", "label": "Музыка", "type": "select", "required": True,
                     "options": ["Да", "Нет"]},
                    {"key": "music_notes", "label": "Пожелания по музыке", "type": "text", "required": False, "placeholder": "оставить свои пожелания"},
                ],
            },
            {
                "title": "Референсы",
                "fields": [
                    {"key": "reference", "label": "Референс", "type": "text", "required": False, "placeholder": "ссылка на похожее"},
                    {"key": "assets", "label": "Архив", "type": "file", "required": False, "placeholder": "ZIP или картинку"},
                ],
            },
            {
                "title": "Доп. пожелания",
                "fields": [
                    {"key": "extra", "label": "Пожелания", "type": "textarea", "required": False, "placeholder": "Как видишь, от себя дополнения..."},
                ],
            },
        ],
    },
}


def get_all_fields(template_key):
    tpl = TEMPLATES[template_key]
    fields = []
    for section in tpl["sections"]:
        fields.extend(section["fields"])
    return fields


def build_summary(template_key, data):
    custom = data.get("task_name", "").strip()
    if custom:
        return custom
    tpl = TEMPLATES[template_key]
    geo = data.get("geo", "")
    if template_key == "keitaro_integration":
        offer = data.get("offer_crm", "") or data.get("offer_kt", "")
        site_type = data.get("site_type", "")
        if isinstance(site_type, list):
            site_type = ", ".join(site_type)
        return f"[{geo}] {site_type} - {offer}"
    else:
        vertical = data.get("vertical", "")
        return f"[{geo}] {tpl['name']} - {vertical}"


def build_description(template_key, data):
    tpl = TEMPLATES[template_key]
    lines = [f"Team: {tpl.get('team', '')}", f"Template: {tpl['name']}", ""]
    for section in tpl["sections"]:
        title = section["title"]
        lines.append(f"=== {title} ===")
        for field in section["fields"]:
            value = data.get(field["key"], "")
            if isinstance(value, list):
                value = ", ".join(value)
            label = field["label"]
            if value and field["type"] != "file":
                lines.append(f"{label}: {value}")
        lines.append("")
    return "\n".join(lines)
