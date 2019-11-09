import sqlalchemy
from sqlalchemy import create_engine, and_, or_
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print(sqlalchemy.__version__)

engine = create_engine('sqlite:///customers.db', echo=False)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    age = Column(Integer)


def print_all_customers(customers):
    for customer in customers:
        print_customer(customer)


def print_customer(customer):
    print("[ID: {0}] Name: {1} Address: {2}, Email: {3}, Age: {4}".format(
        customer.id,
        customer.name,
        customer.address,
        customer.email,
        customer.age
    ))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def main():
    count = session.query(Customer).count()
    print("### There are {0} rows in the table.".format(count))

    if count != 0:
        session.query(Customer).delete()
        count = session.query(Customer).count()
        print("### There are {0} rows in the table after performing 'delete'.".format(count))


    ## INSERT (POST)
    print("\n### session.add()")
    customer = Customer(name='김철수', address='서울 송파구', email='cskim@gmail.com', age=20)
    session.add(customer)
    session.commit()

    print("### session.add_all()")
    session.add_all([
        Customer(name='이나라', address='대전 유성구', email='nrlee@gmail.com', age=21),
        Customer(name='나길동', address='대구 달서구', email='gdna@gmail.com', age=22),
        Customer(name='배칠수', address='인천 부평구', email='csbae@gmail.com', age=19)]
    )
    session.commit()

    count = session.query(Customer).count()
    print("### There are {0} rows in the table after performing 'add' and 'add_all'.".format(count))


    ## SELECT (GET)
    print("\n### session.query(Customer).all()")
    customers = session.query(Customer).all()
    print_all_customers(customers)

    print("\n### session.query(Customer).filter(Customer.id == 2)")
    customers = session.query(Customer).filter(Customer.id == 2)
    print_all_customers(customers)

    print("\n### session.query(Customer).filter(Customer.id != 2)")
    customers = session.query(Customer).filter(Customer.id != 2)
    print_all_customers(customers)

    print("\n### session.query(Customer).first()")
    customer = session.query(Customer).first()
    print_customer(customer)

    print("\n### session.query(Customer).filter(Customer.name.like('%수%'))")
    customers = session.query(Customer).filter(Customer.name.like('%수%'))
    print_all_customers(customers)

    print("\n### session.query(Customer).filter(Customer.id.in_([2, 3]))")
    customers = session.query(Customer).filter(Customer.id.in_([2, 3]))
    print_all_customers(customers)

    print("\n### and_")
    customers = session.query(Customer).filter(and_(Customer.id >= 3, Customer.name.like('%수%')))
    print_all_customers(customers)

    print("\n### or_")
    customers = session.query(Customer).filter(or_(Customer.id >= 3, Customer.name.like('%수%')))
    print_all_customers(customers)

    print("\n### session.query(Customer).get(3)")
    customer = session.query(Customer).get(3)
    print_customer(customer)


    ## UPDATE (PUT)
    customer.age = 25
    session.commit()

    print("\n### session.query(Customer).get(3) after update")
    customer = session.query(Customer).get(3)
    print_customer(customer)

    session.query(Customer).update({Customer.age: 23}, synchronize_session=False)
    session.commit()

    print("\n### session.query(Customer).all() after bulk update")
    customers = session.query(Customer).all()
    print_all_customers(customers)


    ## DELETE (DELETE)
    print("\n### delete the customer with id=3")
    session.query(Customer).filter(Customer.id == 3).delete()
    session.commit()

    print("\n### session.query(Customer).all() after deleting")
    customers = session.query(Customer).all()
    print_all_customers(customers)


if __name__ == "__main__":
    main()
