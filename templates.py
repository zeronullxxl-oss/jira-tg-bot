TEAMS = {
    "tech": {"name": "Тех отдел", "emoji": "\u2699\ufe0f", "project": "FLOW"},
    "design": {"name": "Диз отдел", "emoji": "\U0001f3a8", "project": "DESIGN"},
}

TEMPLATES = {
    "keitaro_integration": {
        "team": "tech",
        "name": "Интегра лендов/прилендов",
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
                         "Сделать с нуля или выкачать (скрины/идеи, референсы)",
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
                    {"key": "offer_crm", "label": "Название оффера в CRM", "type": "text", "required": True, "placeholder": "Lend(MEX_GPT-Trade_V1)"},
                    {"key": "offer_kt", "label": "Название оффера в КТ", "type": "text", "required": True, "placeholder": "Lend(MEX_GPT-Trade_V1)"},
                    {"key": "geo", "label": "Гео", "type": "text", "required": True, "placeholder": "MEX, MY, JP..."},
                    {"key": "lang", "label": "Язык", "type": "text", "required": True, "placeholder": "ES, EN, RU..."},
                    {"key": "vertical", "label": "Вертикаль", "type": "text", "required": False, "placeholder": "инвест"},
                    {"key": "user_id_crm", "label": "Юзер ID в CRM", "type": "text", "required": False, "placeholder": ""},
                    {"key": "thankyou_id", "label": "Id спасибо страницы (если есть)", "type": "text", "required": False, "placeholder": "В архивк"},
                ],
            },
            {
                "title": "Референсы",
                "fields": [
                    {"key": "reference", "label": "Референс", "type": "text", "required": False, "placeholder": "ссылка на референс"},
                    {"key": "figma_url", "label": "Figma / дизайн", "type": "text", "required": False, "placeholder": "ссылка на макет"},
                    {"key": "assets_url", "label": "Архив ассетов", "type": "text", "required": False, "placeholder": "ZIP, ссылка на кейтаро"},
                    {"key": "telegraph_text", "label": "Телеграф", "type": "textarea", "required": False, "placeholder": "Напиши текст — опубликуется на telegra.ph автоматом"},
                ],
            },
            {
                "title": "Сроки и приоритет",
                "fields": [
                    {"key": "deadline", "label": "Дедлайн", "type": "text", "required": False, "placeholder": "С некст недели, завтра, 15.03..."},
                    {"key": "priority", "label": "Приоритет", "type": "select", "required": True,
                     "options": ["Обычная", "Срочная", "Очень срочная"]},
                ],
            },
            {
                "title": "Суть задачи",
                "fields": [
                    {"key": "task_description", "label": "Описание", "type": "textarea", "required": False, "placeholder": "Подробно опиши что нужно сделать..."},
                ],
            },
            {
                "title": "Ассеты",
                "fields": [
                    {"key": "assets_needed", "label": "Нужные материалы", "type": "multi_select", "required": False,
                     "options": ["Изображения", "Видео", "Логотипы", "Иконки"]},
                    {"key": "assets_file", "label": "Файлы / материалы", "type": "file", "required": False},
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
                     "options": ["Обычная", "Срочная", "Очень срочная"]},
                    {"key": "deadline", "label": "Дедлайн", "type": "text", "required": False, "placeholder": "завтра, 15.03, С некст недели..."},
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
                     "options": ["Универсальное без оффера", "С оффером ( Вставить ссылку на Офер )"]},
                    {"key": "offer_url", "label": "Ссылка на оффер", "type": "text", "required": False, "placeholder": "вставить ссылку на оффер"},
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
                    {"key": "character", "label": "Описать какой персонаж нужен для крео", "type": "textarea", "required": False, "placeholder": "Какой персонаж нужен..."},
                    {"key": "celeb", "label": "Селеба дать описание", "type": "textarea", "required": False, "placeholder": "Описание селебы..."},
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
                     "options": ["Обычная", "Срочная", "Очень срочная"]},
                    {"key": "deadline", "label": "Дедлайн", "type": "text", "required": False, "placeholder": "завтра, 15.03, С некст недели..."},
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
                     "options": ["Универсальное без оффера", "С оффером ( Вставить ссылку на Офер )"]},
                    {"key": "offer_url", "label": "Ссылка на оффер", "type": "text", "required": False, "placeholder": "вставить ссылку на оффер"},
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
    """Build plain text fallback."""
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


def _adf_text(text, marks=None):
    node = {"type": "text", "text": str(text)}
    if marks:
        node["marks"] = marks
    return node


def _adf_bold(text):
    return _adf_text(text, [{"type": "strong"}])


def _adf_paragraph(*content):
    return {"type": "paragraph", "content": list(content)}


def _adf_heading(text, level=3):
    return {"type": "heading", "attrs": {"level": level}, "content": [_adf_text(text)]}


def _adf_divider():
    return {"type": "rule"}


def _adf_panel(panel_type, content_nodes):
    """panel_type: info, note, warning, success, error"""
    return {
        "type": "panel",
        "attrs": {"panelType": panel_type},
        "content": content_nodes,
    }


def _adf_table(rows):
    """rows = list of lists. First row = header."""
    table_rows = []
    for i, row in enumerate(rows):
        cell_type = "tableHeader" if i == 0 else "tableCell"
        cells = []
        for cell in row:
            if isinstance(cell, str):
                cells.append({"type": cell_type, "content": [_adf_paragraph(_adf_text(cell))]})
            else:
                cells.append({"type": cell_type, "content": [_adf_paragraph(cell)]})
        table_rows.append({"type": "tableRow", "content": cells})
    return {"type": "table", "attrs": {"isNumberColumnEnabled": False, "layout": "default"}, "content": table_rows}


def _adf_status(text, color="neutral"):
    """color: neutral, purple, blue, red, yellow, green"""
    return {
        "type": "status",
        "attrs": {"text": text, "color": color, "style": ""},
    }


def _adf_task_list(items, checked_items):
    """Render as Jira taskList with checkboxes."""
    tasks = []
    for item in items:
        is_checked = item in checked_items
        tasks.append({
            "type": "taskItem",
            "attrs": {"localId": item, "state": "DONE" if is_checked else "TODO"},
            "content": [{"type": "text", "text": item}],
        })
    return {"type": "taskList", "attrs": {"localId": "list"}, "content": tasks}


def _adf_bullet_list(items):
    """Render as bullet list."""
    nodes = []
    for item in items:
        nodes.append({
            "type": "listItem",
            "content": [_adf_paragraph(_adf_text(str(item)))],
        })
    return {"type": "bulletList", "content": nodes}


def _adf_code_block(text):
    """Render as code block for preland mappings etc."""
    return {
        "type": "codeBlock",
        "attrs": {},
        "content": [{"type": "text", "text": text}],
    }


def build_adf_description(template_key, data, buyer_name="", buyer_tag=""):
    """Build rich ADF description for Jira."""
    tpl = TEMPLATES[template_key]
    team = TEAMS.get(tpl.get("team", ""), {})
    nodes = []

    # Each section
    for section in tpl["sections"]:
        filled_fields = []
        for field in section["fields"]:
            value = data.get(field["key"], "")
            if field["type"] == "file":
                continue
            if not value:
                continue
            filled_fields.append(field)

        if not filled_fields:
            continue

        # Section heading
        nodes.append(_adf_heading(section["title"], 3))

        for field in filled_fields:
            value = data.get(field["key"], "")

            # Multi-select → checkbox list
            if field["type"] == "multi_select":
                all_options = field.get("options", [])
                selected = value if isinstance(value, list) else [value]
                nodes.append(_adf_task_list(all_options, selected))

            # Select → checkbox list (single selection)
            elif field["type"] == "select":
                all_options = field.get("options", [])
                nodes.append(_adf_task_list(all_options, [value]))

            # Textarea with multiline → code block for mappings, normal for descriptions
            elif field["type"] == "textarea" and field["key"] == "preland_mapping":
                nodes.append(_adf_paragraph(_adf_bold(f"{field['label']}:")))
                nodes.append(_adf_code_block(str(value)))

            elif field["type"] == "textarea":
                nodes.append(_adf_paragraph(_adf_bold(f"{field['label']}:")))
                for line in str(value).split("\n"):
                    nodes.append(_adf_paragraph(_adf_text(line)))

            # Text field → label: value
            else:
                nodes.append(_adf_paragraph(
                    _adf_text(f"{field['label']}: {value}"),
                ))

        nodes.append(_adf_divider())

    return nodes
