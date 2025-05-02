import csv
import re


def lod():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        return contacts_list


# правим телефоны
def fix_phone(phone):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(?:\s*(доб\.)\s*(\d+))?"
    substitution = r"+7(\2)\3-\4-\5 \6\7"
    return re.sub(pattern, substitution, phone).strip()


def cut_cont(contacts_list):
    main_cont = {}  # для  контактов
    for contact in contacts_list:
        # дробим фио
        full_name = " ".join(contact[:3]).split()
        last_name, first_name, *surname = (full_name + [""])[:3]
        surname = surname[0] if surname else None
        phone = fix_phone(contact[5])

        # ищем дубли
        key = (last_name, first_name)
        if key in main_cont:
            existing = main_cont[key]
            existing[2] = existing[2] or surname
            existing[3] = existing[3] or contact[3]
            existing[4] = existing[4] or contact[4]
            existing[5] = existing[5] or phone
            existing[6] = existing[6] or contact[6]
        else:
            main_cont[key] = [last_name, first_name, surname, contact[3], contact[4], phone, contact[6]]

    return list(main_cont.values())


def reld(final_contacts_list):
    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_contacts_list)


if __name__ == "__main__":
    contacts_list = lod()
    final_contacts_list = cut_cont(contacts_list)
    reld(final_contacts_list)
