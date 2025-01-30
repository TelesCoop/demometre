import json
from collections import defaultdict

import pandas as pd
from babel.messages.pofile import write_po, read_po, Catalog

LOCALES = ["en"]


def read_po_file(locale) -> Catalog:
    with open(f"./language/{locale}/app.po", "r") as f:
        return read_po(f)


def write_po_file(locale, catalog: Catalog):
    with open(f"./language/{locale}/app.po", "wb") as f:
        write_po(f, catalog, width=None)


def write_json_file(locale, translations: dict):
    with open(f"./language/{locale}/{locale}.json", "w") as f:
        json.dump(translations, f, indent=2)


def read_extraction():
    extraction_path = "language/extraction.md"
    cols = ["path", "file", "line", "language"]
    df = pd.read_table(
        extraction_path, sep="│", skiprows=4, index_col=1, engine="python"
    )
    df = df[df.index.notna()]
    df.columns = [e.strip() for e in df.columns]
    df = df[cols].reset_index(drop=True)
    for col in [col for col in cols if col != "line"]:
        df[col] = df[col].str.strip()
        # remove quotes at start and end
        df[col] = df[col].str.slice(1, -1)

    location_per_message_id = defaultdict(list)
    for row in df.itertuples():
        row_path = " ".join(row.path.replace("\\n", " ").split())
        row_file = row.file.replace("./", "")
        location_per_message_id[row_path].append((row_file, row.line))
    return location_per_message_id


def update():
    for locale in LOCALES:
        catalog = read_po_file(locale)

        # keep order
        po_file_messages = list(dict.fromkeys(message.id for message in catalog))
        singular_form_of_plural_po_file_messages = {
            message.id[0] for message in catalog if message.pluralizable
        }
        location_per_message_id = read_extraction()

        # first existing po files messages, then new ones from location_per_message_id
        keys_order = po_file_messages + list(
            set(location_per_message_id)
            - set(po_file_messages)
            - set(singular_form_of_plural_po_file_messages)
        )

        # add new messages from parsed extraction to the po file, using existing translations
        new_catalog = Catalog()
        new_translations = {}
        for message_id in keys_order:
            message_string = ""
            message = catalog.get(message_id)
            locations = location_per_message_id.get(message_id, [])
            if message is not None:
                message_string = message.string
                if not locations:
                    locations = message.locations
            new_catalog.add(
                message_id,
                message_string,
                locations=locations,
            )
        write_po_file(locale, new_catalog)

        # save new json file
        new_translations = {}
        for message in catalog:
            if not message.id:
                continue
            if message.pluralizable:
                new_translations[message.id[0]] = " | ".join(message.string)
            else:
                new_translations[message.id] = message.string
        # sort new_translations by alphabetical key order
        new_translations = dict(sorted(new_translations.items()))
        write_json_file(locale, new_translations)


if __name__ == "__main__":
    update()
