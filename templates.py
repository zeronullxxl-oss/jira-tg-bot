TEMPLATES = {
    "keitaro_integration": {
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
                    {"key": "telegraph", "label": "Телеграф", "type": "text", "required": False, "placeholder": "ссылка на telegraph"},
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
}


def get_all_fields(template_key):
    tpl = TEMPLATES[template_key]
    fields = []
    for section in tpl["sections"]:
        fields.extend(section["fields"])
    return fields


def build_summary(template_key, data):
    geo = data.get("geo", "")
    offer = data.get("offer_crm", "") or data.get("offer_kt", "")
    site_type = data.get("site_type", "")
    if isinstance(site_type, list):
        site_type = ", ".join(site_type)
    return f"[{geo}] {site_type} - {offer}"


def build_description(template_key, data):
    tpl = TEMPLATES[template_key]
    lines = []
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
