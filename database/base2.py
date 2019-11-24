import sqlalchemy
from sqlalchemy import create_engine, and_, or_, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

print(sqlalchemy.__version__)

engine = create_engine('sqlite:///database/customers.db', echo=False)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    email = Column(String)
    age = Column(Integer)
    invoices = relationship("Invoice", back_populates="customer", cascade="all, delete, delete-orphan" )

    def __repr__(self):
        return "[ID: {0}] Name: {1} Address: {2}, Email: {3}, Age: {4}, Invoices: {5}".format(
            self.id, self.name, self.address, self.email, self.age, self.invoices
        )

class Invoice(Base):
    __tablename__ = 'invoice'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(column='customer.id'))
    invoice_no = Column(Integer)
    amount = Column(Integer)
    customer = relationship("Customer", back_populates="invoices")

    def __repr__(self):
        return "[invoice id: {0}] customer_id: {1}, invoice_no: {2}, amount: {3}, customer.name: {4}".format(
            self.id, self.customer_id, self.invoice_no, self.amount, self.customer.name
        )


def print_all_customers(customers):
    for customer in customers:
        print(customer)


Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
db_session = db_session()


def main():
    invoice_count = db_session.query(Invoice).count()
    customer_count = db_session.query(Customer).count()
    print("### There are {0} rows and {1} rows in the 'Invoice' and 'Customer' table after performing 'delete'.".format(
        invoice_count, customer_count
    ))

    if customer_count != 0 and invoice_count != 0:
        db_session.query(Invoice).delete()
        db_session.query(Customer).delete()
        invoice_count = db_session.query(Invoice).count()
        customer_count = db_session.query(Customer).count()
        print("### There are {0} rows and {1} rows in the 'Invoice' and 'Customer' table after performing 'delete'.".format(
            invoice_count, customer_count
        ))

    ## INSERT (POST)
    print("\n### db_session.add()")
    customer = Customer(name='김철수', address='서울 송파구', email='cskim@gmail.com', age=20)
    customer.invoices = [Invoice(invoice_no=10, amount=15000), Invoice(invoice_no=14, amount=3850)]
    db_session.add(customer)
    db_session.commit()

    print("### db_session.add_all()")
    customers = [
        Customer(
            name='이나라', address='대전 유성구', email='nrlee@gmail.com', age=21,
            invoices=[Invoice(invoice_no=10, amount=15000), Invoice(invoice_no=14, amount=3850)]
        ),
        Customer(
            name='나길동', address='대구 달서구', email='gdna@gmail.com', age=22,
            invoices=[Invoice(invoice_no=9, amount=15000), Invoice(invoice_no=11, amount=6000)]
        )
    ]
    db_session.add_all(customers)
    db_session.commit()

    invoice_count = db_session.query(Invoice).count()
    customer_count = db_session.query(Customer).count()
    print("### There are {0} rows and {1} rows in the 'Invoice' and 'Customer' table after performing 'delete'.".format(
        invoice_count, customer_count
    ))


    ## JOIN SELECT (GET)
    print("\n### db_session.query(Customer).all()")
    customers = db_session.query(Customer).all()
    print_all_customers(customers)

    print("\n### db_session.query(Customer, Invoice).join(Invoice).filter(Invoice.amount == 6000).all()")
    for customer, invoice in db_session.query(Customer, Invoice).join(Invoice).filter(Invoice.amount == 6000).all():
        print(customer)
        print(invoice)


if __name__ == "__main__":
    main()
