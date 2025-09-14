import csv
import re

def read_file(file: str):
    with open(file, encoding='UTF_8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
    return contacts_list

def write_file(file:str, data:list):
    with open(file, 'w', encoding='UTF-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(data)

def change_format_phone(phone: str):
    if phone:
        pattern = r'(\+7|8){1}\s*[(]*(\d{3})[)]*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})([ (]*(\w+\.)\s*(\d+)[)]*)*'
        pattern2 = r'+7(\2)\3-\4-\5 \7\8'
        return re.sub(pattern, pattern2, phone)
    else:
        return phone

def change_phonebook(list_contacts:list):

    dict_contacts = {}
    dict_contacts[('lastname', 'firstname')] = {'surname': 'surname',
                                                'organization': 'organization',
                                                'position': 'position',
                                                'phone': 'phone',
                                                'email': 'email'
                                                }

    for person in list_contacts[1:]:

        person[5] = change_format_phone(person[5]).strip()

        fio = ' '.join(person[:2]).split()
        fi = tuple(fio[:2])
        if len(fio) == 3:
            person[2] = fio[2]
        if fi not in dict_contacts:
            dict_contacts[fi] = {'surname': person[2],
                                 'organization': person[3],
                                 'position': person[4],
                                 'phone': person[5],
                                 'email': person[6]
                                 }
        else:
            count = 2
            for k,v in dict_contacts[fi].items():
                if not v:
                    dict_contacts[fi][k] = person[count]
                count += 1

    return dict_contacts

def from_dict_to_list(d:dict):

    new_list = []

    for k,v in d.items():
        new_list.append([k[0],k[1]]+list(v.values()))

    return new_list

if __name__ == '__main__':
    contacts = read_file('phonebook_raw.csv')
    new_data = from_dict_to_list(change_phonebook(contacts))
    write_file('phonebook.csv',new_data)





