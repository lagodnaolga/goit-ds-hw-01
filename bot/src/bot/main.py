import pickle
from . import address_book
 

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return ValueError
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Give me name and phone please."
    return inner

path_to_data = "addressbook.pkl"
def save_data(book, filename=path_to_data):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename=path_to_data):
    try:
        with open(filename, "rb") as file:
            restored_book = pickle.load(file)
            return restored_book
    except FileNotFoundError:
        return address_book.AddressBook() 
    

def parse_input(user_input):
    """
    Функція перетворює інформація від користувача (input) на список elements.
    Потім розділяє його на команду та аргументи.
    
    Аргументи:
    user_input - інформація від користувача.

    Повертає:
    cmd, arguments - відповідно команда та аргументи; перший та всі наступні елементи списку elements.

    """    

    if len(user_input) >0:
        elements = user_input.split()
        cmd = elements[0].strip().lower()
        arguments = elements[1:]
        return cmd, arguments
    else:
        return "", []


@input_error
def add_contact(arguments, contacts):
    """
    contacts - екземпляр класу AddressBook.
    
    Функція спочатку new_record (екземпляр класу Record), а потім додає його в словник contacts.
    У якості аргументів приймає arguments і contacts.

    Якщо передана неправильна команда, повертається "Error: please provide name and phone."
    Якщо все передано правильно, повертається "Contact added."  

    """
    name = arguments[0]
    phone = arguments[1]
    new_record = address_book.Record(name)
    new_record.add_phone(phone)
    contacts.add_record(new_record)
    return "Contact added."

@input_error
def change_contact(arguments, contacts):
    """
    Функція оновлює record у contacts.
    У якості аргументів приймає arguments і contacts. 

    Якщо передана неправильна команда, повертається "Error: please provide name and phone."
    Спочатку виконується метод .find(), щоб знайти record у contacts за іменем name. 
    Якщо за вказаним іменем name record не знайдено, повертається "Contact not found."
    Якщо все передано правильно, виконується метод edit_phone() і повертається "Contact updated." і запис оновлюється в словнику.

    """
    name = arguments[0]
    old_phone = arguments[1]
    new_phone = arguments[2]
    record = contacts.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(arguments, contacts):
    """
    Функція повертає номер телефону за іменем (повертає phone.value).

    Якщо передана неправильна команда, повертається "Error: please provide a name."
    Спочатку виконується метод .find(), щоб знайти record у contacts за іменем name. 
    Якщо за вказаним іменем name record не знайдено, повертається "Contact not found."
    Якщо все передано правильно, повертається номер телефону, який відповідає record за вказаним name.

    """
    name = arguments[0]
    record = contacts.find(name)
    if record is None:
        raise KeyError
    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(contacts):

    """
    Функція повертає всі контакти (record) зі словника contacts.

    Якщо записів немає, повертається "The contact book is empty."
    
    """
    if not contacts:
        return "The contact book is empty."
    return contacts

@input_error
def add_birthday(arguments, contacts):
    """
    Функція додає день народження birthday_to_add до record.

    Спочатку виконується метод .find(), щоб знайти record у contacts за іменем name.
    Якщо за вказаним іменем name record не знайдено, повертається "Contact not found."
    Якщо все передано правильно, виконується метод add_birthday() класу Record і повертається "Birthday added."

    """
    name = arguments[0]
    birthday_to_add = arguments[1]
    record = contacts.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(birthday_to_add)
    return "Birthday added."


@input_error
def show_birthday(arguments, contacts):
    """
    Функція виводить день народження відповідного record.

    Спочатку виконується метод .find(), щоб знайти record у contacts за іменем name.
    Якщо за вказаним іменем name record не знайдено, повертається "Contact not found."
    Якщо у record не знайдено .birthday, повертається "Birthday is not defined."
    Якщо все передано правильно, повертається рядкове значення record.birthday (виконується __str__ метод record).

    """

    name = arguments[0]
    record = contacts.find(name)
    if record is None:
        raise KeyError
    if record.birthday is None:
        return "Birthday is not defined."
    return str(record.birthday)


@input_error
def birthdays(contacts):
    """
    Функція показує дні народження протягом наступних 7 днів.

    Спочатку виконується метод get_upcoming_birthdays(), щоб знайти дні народження протягом наступних 7 днів.
    Якщо результат виконання функції None, повертається "No upcoming birthdays."
    Якщо дні народження знайдені, виводиться результат.

    """
    upcoming = contacts.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    result = "\n".join(f"{item['name']}: {item['birthday']}" for item in upcoming)
    return result 

    

def main():
    contacts = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, arguments = parse_input(user_input)

        if command in ["exit", "close"]:
            save_data(contacts)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(arguments, contacts))

        elif command == "change":
            print(change_contact(arguments, contacts))

        elif command == "phone":
            print(show_phone(arguments, contacts))

        elif command == "all":
            print(show_all(contacts))
        
        elif command == "add_birthday":
            print(add_birthday(arguments, contacts))

        elif command == "show_birthday":
            print(show_birthday(arguments, contacts))

        elif command == "birthdays":
            print(birthdays(contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()