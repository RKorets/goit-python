from collections import UserDict, UserList
import re
from records_note import RecordNote


class NotesBook(UserDict):

  
    # def __init__(self):
    #     super().__init__()

    def __str__(self):
        return f"{self.data}"

    def print_note_book(self, data = None):
        if data and isinstance(data, list):
            for i in data:
                print(f"id: {i.id_record_note}, tag: {i.tag}, note: "
                      f"{i.note}")
        else:
            for keys_note in self.data.keys():
                print(f"id: {self.data.get(keys_note).id_record_note}   "
                      f"tag: {self.data.get(keys_note).tag}   "
                      f"note: {self.data.get(keys_note).note}   ")

    def add_record_note(self, record_note: RecordNote):
        self.data[record_note.id_record_note] = record_note

    def delete_note(self, notes):
        for i in notes:
            if i.id_record_note in self.data.keys():
                self.data.pop(i.id_record_note, "Таких заміток нема")

    def search_parametr_note(self, note_parametr, user_parametr):
        find_note = []
        if note_parametr == "tag":
            for keys_note in self.data.keys():
                if str(self.data.get(keys_note).tag) == user_parametr:
                    find_note.append(self.data.get(keys_note))
        else:
            for keys_note in self.data.keys():
                if str(self.data.get(keys_note).id_record_note) == user_parametr:
                    find_note.append(self.data.get(keys_note))
        return find_note

    def search_word_note(self, part_note):
        find_all_notes = []
        for keys_note in self.data.keys():
            if re.findall(part_note, str(self.data.get(
                    keys_note).note)):
                find_all_notes.append(self.data.get(keys_note))
        return find_all_notes

    def edit_note(self):
        print("Func in progress, please create a new one")

    def sort_note(self):
        self.data = dict(sorted(self.data.items(), key=lambda val:val[1].tag))
    
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
