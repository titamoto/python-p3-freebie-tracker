from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship('Freebie', backref=backref('company'))

    devs = association_proxy('freebies', 'dev',
           creator=lambda dev: Freebie(dev=dev))

    def __repr__(self):
        return f'Company {self.name}' + ', ' + f'{self.founding_year}'
    
    def give_freebie(self, dev, item_name, value):

        freebie = Freebie(
            item_name=item_name,
            value=value,
            dev_id=dev.id,
            company_id=self.id)
        
        return freebie

    @classmethod
    def oldest_company(cls):
        engine = create_engine('sqlite:///freebies.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        return session.query(Company).order_by(Company.founding_year).first() 

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    freebies = relationship('Freebie', backref=backref('dev'))

    companies = association_proxy('freebies', 'company',
           creator=lambda company: Freebie(company=company))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        engine = create_engine('sqlite:///freebies.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        freebie = session.query(Freebie).filter(Freebie.dev_id == self.id).first()
        if freebie.item_name == item_name:
            return True
        return False  

    def give_away(self, dev, freebie):
        pass
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def __repr__(self):
        return f'Freebie {self.id} ' + f'{self.item_name} ' + f'{self.value} ' + f'{self.dev_id} ' + f'{self.company_id} '

    def print_details(self):
        engine = create_engine('sqlite:///freebies.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        dev = session.query(Dev).filter(Dev.id == self.dev_id).first()
        company = session.query(Company).filter(Company.id == self.company_id).first()
        print(f'{dev.name} owns a {self.item_name} from {company.name}')
