#!/usr/bin/env python3

from random import choice as rc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Dev, Company, Freebie

engine = create_engine('sqlite:///seed_db.db')
Session = sessionmaker(bind=engine)
session = Session()

def delete_records():
    session.query(Dev).delete()
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.commit()

def create_records():
    devs = [Dev() for i in range(500)]
    companies = [Company() for i in range(100)]
    freebies = [Freebie() for i in range(1000)]
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
