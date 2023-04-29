import argparse
import json
import os
from datetime import datetime


def load_notes():
    notes = []

    if os.path.exists('notes.json'):
        with open('notes.json', 'r') as f:
            notes = json.load(f)

    return notes


def save_notes(notes):
    with open('notes.json', 'w') as f:
        json.dump(notes, f, indent=4)


def find_note_by_id(notes, note_id):
    for note in notes:
        if note['id'] == note_id:
            return note
    return None


def filter_notes_by_date(notes, date_str):
    filtered_notes = []
    for note in notes:
        if note['created_date'].startwith(date_str) or note['last_updated_date'].startswith(date_str):
            filtered_notes.append(note)
    return filtered_notes


def list_notes():
    notes = load_notes()
    date = input(
        "Введите дату (YYYY-MM-DD) для фильтрации заметок (оставьте пустым, чтобы вывести все заметки): ")

    if date:
        filtered_notes = filter_notes_by_date(notes, date)
        for note in filtered_notes:
            print(f"{note['id']}: {note['title']} ({note['created_date']})")

    else:
        for note in notes:
            print(f"{note['id']}: {note['title']} ({note['created_date']})")


def add_note():
    title = input("Введите заголовок заметки: ")
    body = input("Введите тело заметки: ")

    notes = load_notes()

    id = len(notes) + 1
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    last_updated_date = created_date
    note = {'id': id, 'title': title, 'body': body,
            'created_date': created_date, 'last_updated_date': last_updated_date}
    notes.append(note)
    save_notes(notes)
    print('Заметка успешно сохранена')


def edit_note():
    notes = load_notes()
    note_id = int(input("Введите идентификатор заметки: "))
    note = find_note_by_id(notes, note_id)

    if not note:
        print(f"Заметка с индентификатором {note_id} не найдена")
        return

    title = input(
        "Введите новый заголовок заметки (оставьте пустым, чтобы не менять): ")
    body = input(
        "Введите новый текст заметки (оставьте пустым, чтобы не менять): ")

    if title:
        note['title'] = title
    if body:
        note['body'] = body

    note['last_updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    save_notes(notes)
    print('Заметка успешно отредактирована')


def delete_note():

    notes = load_notes()
    note_id = int(input("Введите идентификатор заметки: "))
    note = find_note_by_id(notes, note_id)

    if not note:
        print(f"Заметка с идентификатором {note_id} не найдена")
        return

    notes.remove(note)
    save_notes(notes)
    print(f"Заметка успешно удалена")


def main():
    while True:

        command = input('Введите команду (list/add/edit/delete): ')

        if command == 'list':
            list_notes()
        elif command == 'add':

            add_note()
        elif command == 'edit':
            edit_note()
        elif command == 'delete':
            delete_note()
        else:
            print('Некорректная команда, попробуйте еще раз.')


main()
