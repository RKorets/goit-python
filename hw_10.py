
from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class Phone(Field):
    pass


class Name(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone) -> None:
        self.name = name
        self.phones = []  # спиисок экземпляр класа Phone
        self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def delete_phone(self,phone: Phone):
        for el in self.phones:
             if phone==el.value:
                 self.phones.remove(el)
                 return
        print("Error number")

    def change_phone(self, phone: Phone, new_phone: Phone):
        for el in self.phones:
             if phone==el.value:
                 self.phones.remove(el)
                 self.add_phone(new_phone)
                 return
        print("Error number")

    def __str__(self) -> str:
         return f'Name: {self.name} Phones: {", ".join([str(p) for p in self.phones if str(p)!=""])}'


class AddressBook(UserDict):
    # def add_record(self, *args):
    #     for item in args:
    #         self.data[item.name] = item
    def add_record(self, item):
       # for item in args:
            for el in self.data:
                if item.name.value in el.value:
                    return print("Сontact with this name exists")
            self.data[item.name] = item


    def __str__(self) -> str:
        result = "\n".join([str(v) for v in self.data.values()])
        return result


def input_error(func):
    def verification(args):
        try:
            user_command = [args.split(" ")[0].lower()]
            user_info = args.split(" ")[1:]
            for el in user_info:
                user_command.append(el)
            if len(user_info) < 2:
                user_command.append("")
            verification_result = func(user_command)
            return verification_result
        except KeyError:
            print("Invalid command please try again!KeyError")
        except TypeError:
            print("Invalid command please try again!TypeError")
        except IndexError:
            print("Invalid command please try again!IndexError")
        except ValueError:
            print("Invalid command please try again!ValueError")
    return verification


CONTACT = AddressBook()

#test contact
rec1 = Record(Name("Roma"), Phone("23331"))
rec5 = Record(Name("Vasua"), Phone("231"))
rec2 = Record(Name("Dima"), Phone("3123"))
rec3 = Record(Name("Nasa"), Phone("1122"))
rec4 = Record(Name("Nasa"), Phone("1122")) #дубль  
CONTACT.add_record(rec1)
CONTACT.add_record(rec5)
CONTACT.add_record(rec2)
CONTACT.add_record(rec3)
CONTACT.add_record(rec4) #дубль- не добавит

@input_error
def handler(commands):

    def new_user():
        record = Record(Name(commands[1]),Phone(commands[2]))
        CONTACT.add_record(record)

    def change():
        for name in CONTACT:
            if str(name)==commands[1]:
              CONTACT.data[name].change_phone(commands[2],Phone(commands[3]))
              return
        print("Error name")

    def hello():
        print("Hello can I help you? - write 'help' show more info ")

    def show_all():
        print(CONTACT)

    def delete_number():
        for name in CONTACT:
            if str(name)==commands[1]:
              CONTACT.data[name].delete_phone(commands[2])
              return
        print("Error name")

    def add_more_number():
        for name in CONTACT:
            if str(name)==commands[1]:
              CONTACT.data[name].add_phone(Phone(commands[2]))
              return
        print("Error name")

    def helps():
        print("hello - Welcome command"
              "\nhelp - Help command"
              "\nadd [name] [phone]- Add new contact in addressbook"
              "\nshow - Show all contact in addressbook"
              "\ndelete [name] [phone] - Delete phone number is select contact"
              "\nmore [name] [phone]- Add more phone number is select contact"
              "\nchange [name] [phone] - Change phone number is select contact")

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
