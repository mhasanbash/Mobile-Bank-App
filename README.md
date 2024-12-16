Mobile Banking Application - Database Project
This project demonstrates the design and implementation of a Mobile Banking Application Database. The main focus is on creating a robust database system to handle various banking operations efficiently and securely.

#Project Structure
Database Design:

Implementation of tables, stored procedures, and functions in PostgreSQL to support banking features such as account management, transactions, and loan processing.
All constraints and validations are handled at the database level to ensure data integrity.
Backend Development:

The backend is implemented using Django with template rendering for the application interface. Features include:
User authentication (securely storing hashed passwords).
Account and transaction management.
Loan management features (loan application, repayment, and installment tracking).
Core Functionalities:

User Account Operations: View account details, transaction history, and account balances.
Transactions: Fund transfers between accounts, ensuring atomicity for rollback in case of errors.
Loan Management: Calculate loan eligibility, apply for loans, and track repayments.
Security: Prevention of SQL injection, hashed password storage, and input validation.
Admin panel for managing accounts and operations.

Technology Stack
Database: PostgreSQL (with stored procedures and functions).
Backend Framework: Django (with template rendering for the UI).
This project highlights the practical application of database principles and backend development, ensuring a seamless and secure banking experience. It can serve as a foundation for more extensive financial applications.

