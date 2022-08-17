import csv
import re
import os
from pprint import pprint


# читаем адресную книгу в формате CSV в список
def read_file(directory, file):
    with open(os.path.join(directory, file), encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")

        return list(rows)


# форматируем строки из файла, согласно заданию
def format_data(contacts_list):
    notebook = []
    notebook.append(contacts_list[0])

    for row in contacts_list[1:]:
        full_name = re.findall(r'\w+[,\s]?', ' '.join(row[:3]))

        lastname = full_name[0]
        firstname = full_name[1]

        if len(full_name) != 3:  # добавление пробела в поле отчетсво, при его отсутствии
            full_name.append('')

        surname = full_name[2]
        organization = row[-4]
        position = row[-3]
        phone = re.sub(
            r"(\+7|8)\s*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})(\s*\(?(\w{3}\.)[\s]*(\d{4})\)?)?",
            "+7(\\2)\\3-\\4-\\5 \\7\\8", row[-2])
        email = row[-1]

        notebook.append([lastname, firstname, surname, organization, position, phone, email])

    return notebook


# очищаем новую новый список от дубликатов
def clearing_dublicates(notebook):
    count_1 = 0
    count_2 = 1
    clear_notebook = []
    while count_1 < len(notebook):
        copy_notebook = notebook[count_1]
        clear_notebook.append(copy_notebook)
        name = notebook[count_1][:2]
        new_notebook = notebook[count_2:]
        for contacts in new_notebook:
            if name == contacts[:2]:
                for contact in range(len(copy_notebook)):
                    if copy_notebook[contact] == '':
                        copy_notebook[contact] = contacts[contact]
                        del notebook[count_1]
        count_1 += 1
        count_2 += 1
    return clear_notebook


# записываем новый файл в формате CSV
def write_file(directory, name, file):
    with open(os.path.join(directory, name), "w") as f:
      datawriter = csv.writer(f, delimiter=',')
      datawriter.writerows(file)


if __name__ == '__main__':
    work_dir = os.getcwd()
    open_file = 'phonebook_raw.csv'
    save_file = 'phonebook_new.csv'
    contacts_list = read_file(work_dir, open_file)
    notebook = format_data(contacts_list)
    new_file = clearing_dublicates(notebook)
    write_file(work_dir, save_file, new_file)
