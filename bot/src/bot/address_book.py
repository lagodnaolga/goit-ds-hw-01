from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, phone_input):
        if not self.is_phone_valid(phone_input):
            raise ValueError("Incorrect phone format.")

        super().__init__(phone_input)
    
    def is_phone_valid(self, phone_to_validate):
        len_condition = len(phone_to_validate)==10
        format_condition = phone_to_validate.isdigit()
        return len_condition and format_condition

class Record:
    def __init__(self, name, birthday: "Birthday" = None):
        self.name = Name(name)
        self.birthday = birthday
        self.phones = [] 

    def add_phone(self, phone_to_add):
        self.phones.append(Phone(phone_to_add))

    def remove_phone(self, phone_to_be_removed):
        phone = self.find_phone (phone_to_be_removed)
        if phone is None:
            raise ValueError("Phone is not found.")
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone is None:
            raise ValueError("Phone is not found.")
        if phone.is_phone_valid(new_phone):
            phone.value = new_phone
        else:
            raise ValueError("Incorrect phone format.")

    def find_phone (self, phone_to_find):
        for phone in self.phones:
            if phone.value == phone_to_find:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return


    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    #додає до AddressBook екземпляри класу Record {record.name.value: record}

    def add_record (self, record):
        self.data[record.name.value] = record

    def find (self, record_to_find):
        return self.data.get(record_to_find) 

    def delete (self, record_to_delete):
        if record_to_delete in self.data:
            del self.data[record_to_delete]
        return

    def find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)
        
    def adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.find_next_weekday(birthday, 0)
        return birthday


    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            
            birthday_this_year = birthday_date.replace(year=today.year)


            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year+1)

            if 0 <= (birthday_this_year - today).days <= days:
                if birthday_this_year.weekday()>=5:
                    birthday_this_year=self.adjust_for_weekend(birthday_this_year)
        
                upcoming_birthdays.append({"name": record.name.value, "birthday": birthday_this_year.strftime("%d.%m.%Y")})
        return upcoming_birthdays

   
    
    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"
        return result
    
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime_object = datetime.strptime(value, "%d.%m.%Y")
            if datetime_object < datetime.now():
                super().__init__(value)
            else:
                raise ValueError("Invalid date.")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self): 
        return self.value  

