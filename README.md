
# 🌟 **Mobile Banking Application - Database Project**

This project demonstrates the design and implementation of a **Mobile Banking Application** with a focus on robust database management and secure backend integration.

---

## 📂 **Project Overview**
A simplified banking system that includes features such as user authentication, account management, secure transactions, and loan processing. The project highlights best practices in **PostgreSQL database design** and backend development with **Django**.

---

## 🚀 **Features**

### ✅ **Core Functionalities**
- **User Account Management:**
  - View account details and balances.
  - Access transaction history with filtering options.
- **Transactions:**
  - Secure fund transfers with rollback for errors (ensuring atomicity).
- **Loan Management:**
  - Calculate loan eligibility and apply for loans.
  - Track loan repayments and view installment details.
- **Security:**
  - Input validation and SQL injection prevention.
  - 
- Admin panel for managing accounts, loans, and user operations.

---

## 🛠️ **Tech Stack**

| **Component**      | **Technology**  |
|---------------------|-----------------|
| **Backend**         | Django (with Template Rendering) |
| **Database**        | PostgreSQL     |
| **Language**        | Python         |

---

## 🗂️ **Project Structure**

1. **Database Design:**  
   - Implementation of tables, stored procedures, and functions in PostgreSQL.  
   - All constraints and validations are handled at the database level.

2. **Backend Implementation:**  
   - Django-based backend to provide a seamless user interface.  
   - Secure integration with the database for banking operations.

3. **Key Modules:**
   - **Authentication**: User login with hashed password storage.
   - **Accounts**: Retrieve account details and balances.
   - **Transactions**: Transfer funds securely and view transaction history.
   - **Loans**: Loan eligibility, application, and repayment tracking.

---

## 📊 **How to Use**

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/mobile-banking-app.git
   ```

2. Navigate to the project directory:  
   ```bash
   cd mobile-banking-app
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database (PostgreSQL) and apply migrations:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Run the Django server:  
   ```bash
   python manage.py runserver
   ```

6. Access the application at:  
   [http://localhost:8000](http://localhost:8000)

---

## 🎨 **Screenshots**
![image](https://github.com/user-attachments/assets/84919cdf-f3ba-4e52-bd38-a3858474c329)
![image](https://github.com/user-attachments/assets/4369911f-b7b9-4d35-9982-0bf878c44938)


---

## 📝 **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Would you like me to generate badges (e.g., license, Python version) or add more sections?
