import sqlalchemy
from sqlalchemy.orm import joinedload
from src.db import session
from src.models import Contact, Phone
import random
from faker import Factory
from src.db import session
from models import Contact, Phone
from time import time

class ExceptError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except sqlalchemy.exc.NoResultFound:
            print('Command not found')
        except sqlalchemy.exc.MultipleResultsFound:
            print('Phone number already exist')


@ExceptError
def create_contact(name, last_name, phone):
    contact = Contact(
        name=str(name),
        last_name=last_name)
    session.add(contact)
    session.commit()
    cont_id = session.query(Contact.id).filter(Contact.name == str(name)).scalar()
    phones = Phone(
        phone=str(phone),
        contacts_id=cont_id)
    session.add(phones)
    session.commit()


@ExceptError
def update_contact(name, phone):
    cont_id = session.query(Contact.id).filter(Contact.name == str(name)).first()
    phones = Phone(
        phone=str(phone),
        contacts_id=cont_id[0])
    session.add(phones)
    session.commit()


@ExceptError
def change_number(name, old_phone, new_phone):
    data = session.query(Phone.id, Contact.id).join(Contact). \
        filter(Phone.phone == old_phone).filter(Contact.name == name).scalar()
    edit = session.query(Phone).get(data)
    edit.phone = new_phone
    session.commit()


@ExceptError
def update_email(name, email):
    id_ = session.query(Contact.id).filter(Contact.name == name).first()
    add = session.query(Contact).get(id_)
    add.email = email
    session.commit()


@ExceptError
def update_last_name(name, last_name):
    id_ = session.query(Contact.id).filter(Contact.name == name).first()
    add = session.query(Contact).get(id_)
    add.last_name = last_name
    session.commit()

@ExceptError
def update_birthday(name, birthday: str):
    id_ = session.query(Contact.id).filter(Contact.name == name).first()
    add = session.query(Contact).get(id_)
    temp = birthday.split('.')
    temp.reverse()
    birthday_db = '-'.join(temp)
    add.birthday = birthday_db
    session.commit()


@ExceptError
def delete_phone(name, phone):
    data = session.query(Phone.id, Contact.id).join(Contact). \
        filter(Phone.phone == phone).filter(Contact.name == name).one()
    session.query(Phone).get(data[0]).delete()
    session.commit()


@ExceptError
def delete_contact(name):
    session.query(Contact).filter(Contact.name == name).delete()
    session.commit()


@ExceptError
def delete_all():
    session.query(Contact).delete()
    session.commit()


@ExceptError
def check_name(name):
    contact = session.query(Contact).filter(Contact.name == str(name)).scalar()
    if not contact:
        return False
    else:
        return True


@ExceptError
def show_number(name):
    phones = session.query(Phone.id).join(Contact).filter(Contact.name == name).all()
    if not phones:
        return f'Contact {name} not found'
    else:
        print(f'Contact {name} number ', end=' ')
        for phone in phones:
            for i in phone:
                number = session.query(Phone).filter(Phone.id == i).one()
                print(f'{number.phone}', end=' ')
        return f''


@ExceptError
def show_all():
    results = session.query(Contact, Phone.phone).join(Phone).all()
    result = 'List of all users:\n'
    for user, phones in results:
        result += f'Contact {user.name} {user.last_name} has phone: {phones}, birthday: {user.birthday}, email: {user.email}, address: {user.address}\n'
    session.commit()
    return result


@ExceptError
def show_birthday(name):
    contact = session.query(Contact).filter(Contact.name == name).first()
    birthday = contact.birthday
    session.commit()
    return birthday


@ExceptError
def find(p):
    results = session.query(Contact, Phone.phone).join(Phone).all()
    for user, phones in results:
        birthday = user.birthday.strftime("%Y-%m-%d")
        if p in user.name or p in user.last_name or p in phones \
                or p in birthday or p in user.email:
            return f'User {user.name} {user.last_name},' \
                   f' phone: {phones},' \
                   f' birthday: {user.birthday},' \
                   f' email: {user.email},'
        else:
            return f'{p} not found'


fake = Factory.create('uk_UA')


def create_contacts(count):
    timer = time()
    for _ in range(count):
        contact = Contact(
            name=fake.first_name(),
            last_name=fake.last_name(),
            birthday=fake.date_between(start_date='-50y'),
            email=fake.email())
        session.add(contact)
        session.commit()
        cont_id = session.query(Contact.id).filter(Contact.name == contact.name).scalar()
        phones = Phone(
            phone=fake.phone_number(),
            contacts_id=cont_id)
        session.add(phones)
        session.commit()
        session.add(contact)
    session.commit()
    print(f' {count} contacts added in {round(time() - timer, 3)} sec')

if __name__ == '__main__':
    create_contacts(100)