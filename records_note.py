from field import Note


class RecordNote:
    
    count_record_note = 0

    def __init__(self):
        self.tag = ""
        self.note = None
        RecordNote.count_record_note += 1
        self.id_record_note = RecordNote.count_record_note

    def __str__(self):
        return f"{self.id_record_note} {self.tag} {self.note}"

    def add_note(self, note: Note):
        self.note = note

    def add_tag(self, tag):
        self.tag = tag

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value