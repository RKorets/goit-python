from collections import UserDict

class Record:

    def __init__(self, name, phone) -> None:
        self.name = Name(name)
        self.phones = Phone(phone)
        #self.phones.phones.append(phone)

    def add_phone(self,phone):
        if phone not in self.phones.phones:
            self.phones.phones.append(phone)
        else: print("Phone exist! Try again")

    def change_phone(self,phone,new_phone):
        if phone in self.phones.phones:
            self.phones.phones.remove(phone)
            self.phones.phones.append(new_phone)
        else: print("Phone number not exist! Try again")

    def delete_phone(self,phone):
        if phone in self.phones.phones:
            self.phones.phones.remove(phone)
        else: print("Phone number not exist! Try again")


class AddressBook(UserDict):

    def add_record(self, obj):
        if isinstance(obj, Record):
            self.data[obj.name] = obj

    def __str__(self) -> str:
        result = "\n".join([str(v) for v in self.data.values()])
        return result

    def show_all_contact(self):
        print("Имя          Номер телефона")
        for name, phone in self.data.items():
            print('{:<10} -{} '.format(name.value,phone.phones.phones))


class Field:
    pass


class Phone(Field):

    def __init__(self,phone=None):
        self.phones = [phone]


class Name(Field):

    full_list = []
    def __init__(self,name):
        self.value = name
        Name.full_list.append(name)


def input_error(func):
    def verification(args):
        try:
            user_command = [args.split(" ")[0].lower()]
            user_info = args.split(" ")[1:]
            for el in user_info:
                user_command.append(el)
            verification_result = func(user_command)
            return verification_result
        except KeyError:
            print("Invalid command please try again!")
        except TypeError:
            print("Invalid command please try again!")
        except IndexError:
            print("Invalid command please try again!")
        except ValueError:
            print("Invalid command please try again!")
    return verification


CONTACT = AddressBook()

@input_error
def handler(commands):

    def new_user():
        if commands[1] not in Name.full_list:
            global record
            record = Record(commands[1], commands[2])
            CONTACT.add_record(record)
        else: print("Contact exist")

    def change():
        for name in CONTACT.data.keys():
            if name.value==commands[1]:
                record = CONTACT.data[name]
                record.change_phone(commands[2],commands[3])


    def hello():
        print("Hello can I help you? - write 'help' show more info ")

    def show_all():
        return CONTACT.show_all_contact()

    def delete_number():
        for name in CONTACT.data.keys():
            if name.value==commands[1]:
                record = CONTACT.data[name]
                record.delete_phone(commands[2])

    def add_more_number():
        for name in CONTACT.data.keys():
            if name.value==commands[1]:
                record = CONTACT.data[name]
                record.add_phone(commands[2])

    def helps():
        print("hello - Welcome command"
              "\nhelp - Help command"
              "\nadd [name] [phone]- Add new contact in addressbook"
              "\nshow - Show all contact in addressbook"
              "\ndelete [name] [phone] - Delete phone number is select contact"
              "\nmore [name] [phone]- Add more phone number is select contact"
              "\nchange [name] [phone] [new phone] - Change phone number is select contact")

    COMMAND = {
        "hello": hello,
        "add": new_user,
        "show" : show_all,
        "delete": delete_number,
        "more": add_more_number,
        "help": helps,
        "change": change
    }[commands[0]]()
    return

def main():
    print("Start App\n")
    while True:
        user_input = input('Try: ')
        if user_input in ["exit", "close", "good bye"]:
            break
        handler(user_input)
    print("\nGood bye!")


if __name__ == "__main__":
      main()
