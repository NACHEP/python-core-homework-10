"""

Застосуємо для цих цілей об'єктно-орієнтоване програмування. 
Спершу виділимо декілька сутностей (моделей) з якими працюватимемо.

У користувача буде адресна книга або книга контактів.
Ця книга контактів містить записи. Кожен запис містить деякий набір полів.

Таким чином ми описали сутності (класи), які необхідно реалізувати. 
Далі розглянемо вимоги до цих класів та встановимо їх взаємозв'язок, правила, 
за якими вони будуть взаємодіяти.

Користувач взаємодіє з книгой контактів, додаючи, видаляючи та редагуючи записи. 
Також користувач повинен мати можливість шукати в книзі контактів записи за одному або декількома критеріями 
(полям).

Про поля також можна сказати, що вони можуть бути обов'язковими (ім'я) та необов'язковими 
(наприклад телефон або email). Також записи можуть містити декілька полів одного типу 
(наприклад декілька телефонів). Користувач повинен мати можливість додавати/видаляти/редагувати поля у 
будь-якому записі.

Технічне завдання
Розробіть систему класів для управління адресною книгою.

"""


from collections import UserDict

#Field: Базовий клас для полів запису. Буде батьківським для всіх полів,
# у ньому реалізується логіка загальна для всіх полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
#Name: Клас для зберігання імені контакту. Обов'язкове поле.

class Name(Field):
    def __str__(self):
        return super().__str__()


#Phone: Клас для зберігання номера телефону. Має валідацію формату (10 цифр). 
#Необов'язкове поле з телефоном та таких один запис
#Клас Phone:
# Реалізовано валідацію номера телефону (має бути 10 цифр).



class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

        if len(str(self.value)) == 10 and str(self.value).isdigit():
            self.value = value
        else:
            raise ValueError('Your number should be 10 digits') 

    
#Record може містити декілька.
# Record: Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
# Відповідає за логіку додавання/видалення/редагування необов'язкових полів та зберігання 
# обов'язкового поля Name
#Клас Record:



class Record:
# Реалізовано зберігання об'єкта Name в окремому атрибуті.
# Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    

# Реалізовано методи для додавання - add_phone
    def add_phone(self, phone_number):
        
        phone = Phone(phone_number)
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

# Видалення телефонів.Реалізовано методи для -видалення - remove_phone
    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

# Редагування телефонів.# Реалізовано методи - редагування -edit_phone
    def edit_phone(self, old_phone, new_phone):
        phone_exists = False
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                phone_exists = True

        if not phone_exists:
            raise ValueError(f"The phone number {old_phone} does not exist.")
        

# Пошук телефону.Реалізовано методи для об'єктів Phone - find_phone.
    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        #return None
    

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        


#AddressBook: Клас для зберігання та управління записами. 
# Успадковується від UserDict, та містить логіку пошуку за записами до цього класу

# Записи Record у AddressBook зберігаються як значення у словнику. 
# В якості ключів використовується значення Record.name.value.

class AddressBook(UserDict):

#Додавання записів.
# Реалізовано метод add_record, який додає запис до self.data.
    def add_record(self, record: Record):
        # if not isinstance (record, Record):
        #     record = Record(record)
        self.data[record.name.value] = record

#Пошук записів за іменем.
# Реалізовано метод find, який знаходить запис за ім'ям.
    def find(self,name):
        return self.data.get(name)

#Видалення записів за іменем.
# Реалізовано метод delete, який видаляє запис за ім'ям.
    def delete(self, name):
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")