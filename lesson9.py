
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
        except IndexError:
            print("Invalid command please try again!")
        except ValueError:
            print("Invalid command please try again!")
    return verification


CONTACT = {}

@input_error
def handler(commands):

    def new_user():
        if commands[1] not in CONTACT.keys():
            CONTACT[commands[1]]=commands[2]
            print("New user add!")
        else:
            print("User exists")

    def change():
        if CONTACT[commands[1]] in CONTACT.values():
            CONTACT[commands[1]]=commands[2]
            print("Change successful")

    def hello():
        print("How can I help you?")

    def show():
        if len(CONTACT.keys()) <1:
            print("Сontact book is empty")
        else:
            print('Name         Number')
            for c in CONTACT:
               print('{:<10} - {}'.format(c,CONTACT[c]))


    def phone():
        print(f'Phone number - {CONTACT[commands[1]]}')

    COMMAND = {
        "hello": hello,
        "add": new_user,
        "show" : show,
        "phone": phone,
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
