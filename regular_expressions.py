import csv
import re

heads = ['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email']


def get_contact_inf(contacts_l):
    new_string = []
    for contact in contacts_l[1:]:
        string = ' '.join(contact[:3]).strip().split()
        string.extend(contact[len(string):])
        string[5] = get_new_phone(contact[5])
        contact_dict = dict(zip(heads, string))
        contact_dict = {key: value for key, value in contact_dict.items() if value}
        new_string.append(contact_dict)
    unique_contacts = get_unique_contact(new_string)
    return get_new_contacts_list(unique_contacts)


def get_new_phone(number):
    pattern = re.compile(r'(\+7|8)?(\s*\(?)(\d{3})(\)?\s?)(-?)(\d{3})(\s*-?)(\d{2})(\s*-?)(\d{2})(\s*\(?(доб\.)\s(\d{'
                         r'4})\)?)?')
    phone = pattern.sub(r'+7(\3)\6-\8-\10 \12\13', number)
    return phone


def get_unique_contact(new_string):
    for (index, contacts) in enumerate(new_string):
        for (index_1, contacts_1) in enumerate(new_string):
            if contacts['lastname'] == contacts_1['lastname'] and index != index_1:
                new_string[index].update(new_string[index_1])
                new_string.pop(index_1)
    return new_string


def get_new_contacts_list(other_string):
    new_contacts = []
    for x in other_string:
        new_contacts.append(x.values())
    new_contacts.insert(0, heads)
    return new_contacts


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    answer = get_contact_inf(contacts_list)

    with open("phonebook.csv", "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(answer)
