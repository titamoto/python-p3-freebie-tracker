#!/usr/bin/env python3

from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie

fake = Faker()

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

devs = [Dev(name = fake.name()) for i in range(500)]
companies = [Company(name = fake.name(), founding_year = fake.random_int(1800, 2022)) for i in range(100)]
freebies = [Freebie(item_name = fake.name(), value = fake.random_int(0, 500)) for i in range(1000)]

def delete_records():
    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.commit()

def create_records():
    session.add_all(devs + companies + freebies)
    session.commit()
    return devs, companies, freebies

def relate_records(devs, companies, freebies):
    for freebie in freebies:
        freebie.dev = rc(devs)
        freebie.company = rc(companies)

    session.add_all(freebies)
    session.commit()

if __name__ == '__main__':
    delete_records()
    devs, companies, freebies = create_records()
    relate_records(devs, companies, freebies)
