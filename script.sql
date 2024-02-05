CREATE Table USERS
(
    id           integer PRIMARY KEY,
    username     varchar(32) unique,
    password     varchar(32),
    first_name   varchar(32),
    last_name    varchar(32),
    address      varchar(255),
    phone_number varchar(20) unique,
    email        varchar(32) unique,
    date_joined  date,
    is_superuser boolean
);


CREATE TABLE BANK_ACCOUNT
(
    id                 SERIAL PRIMARY KEY,
    user_id            integer ,
    account_number     varchar(20) unique,
    primary_password   varchar(4),
    secondary_password varchar(6),
    Balance            numeric(20, 2),
    rate               numeric(10, 2),
    date_opened        DATE,
    date_closed        DATE,
    account_status     boolean,
    FOREIGN KEY (user_id) REFERENCES USERS(id)
);


CREATE TABLE LOAN
(
    id             SERIAL PRIMARY KEY,
    user_id        integer,
    account_number varchar(20),
    loan_amount    numeric(20, 2),
    start_date     timestamp,
    end_date       timestamp,
    loan_status    boolean,
    FOREIGN KEY(user_id) REFERENCES USERS(id),
    FOREIGN KEY(account_number) REFERENCES BANK_ACCOUNT(account_number)
);


CREATE TABLE LOAN_INSTALLMENT
(
    id               SERIAL PRIMARY KEY,
    loan_id          integer unique ,
    account_number   varchar(20),
    payment_deadline Date,
    amount           numeric(20, 2),
    date_of_payment  Date,
    status           boolean,
    FOREIGN KEY(loan_id) REFERENCES LOAN(id)
);


CREATE TABLE TRANSACTIONS
(
    id                         SERIAL PRIMARY KEY,
    source_account_number      varchar(32),
    destination_account_number varchar(32),
    amount                     numeric(10, 2),
    transaction_date           date,
    status                     boolean,
    description                varchar(255),
    FOREIGN KEY (source_account_number) REFERENCES BANK_ACCOUNT (account_number)
);


CREATE TABLE MINIMUMMONEY
(
    id             SERIAL PRIMARY KEY,
    account_number varchar(32),
    min_amount     numeric(10, 2),
    date           DATE,
    active_loan    boolean
);


---------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION account_info(
  IN acc_number varchar(32)
) RETURNS TABLE (
  username varchar(32),
  password varchar(32),
  first_name varchar(32),
  last_name varchar(32),
  aaddres varchar(255),
  phone_number varchar(20),
  email        varchar(32),
  date_joined  date,
  account_number     varchar(20),
  primary_password   varchar(4),
  Balance            numeric(20, 2),
  date_opened        DATE,
  account_status     boolean
)LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.username, u.password, u.first_name, u.last_name, u.address, u.phone_number, u.email, u.date_joined, ba.account_number, ba.primary_password, ba.Balance,ba.date_opened,ba.account_status
    FROM USERS as u, BANK_ACCOUNT as ba
    WHERE ba.account_number = acc_number and u.id = ba.user_id ;
END;
$$;


--------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION account_list(
  IN i_user_id integer
) RETURNS TABLE (
  id                 integer,
  user_id            integer,
  account_number     varchar(20),
  primary_password   varchar(4),
  secondary_password varchar(6),
  Balance            numeric(20, 2),
  rate               numeric(10, 2),
  date_opened        DATE,
  date_closed        DATE,
  account_status     boolean
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM BANK_ACCOUNT as ba
    WHERE ba.user_id = i_user_id;
END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE change_password(
  IN p_user_id integer,
  IN p_old_password varchar(32),
  IN p_new_password varchar(32)
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE USERS
    SET password = p_new_password
    WHERE id = p_user_id and password = p_old_password;

    COMMIT;
END;
$$;


--------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION signin(
  IN i_username varchar(32),
  IN i_password varchar(32)
) RETURNS TABLE (
  id INT,
  username varchar(32),
  password varchar(32),
  first_name varchar(32),
  last_name varchar(32),
  aaddres varchar(255),
  phone_number varchar(20),
  email        varchar(32),
  date_joined  date,
  is_superuser boolean
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM USERS as u
    WHERE u.username = i_username and u.password = i_password;
END;
$$;
---------------------------------------------------------------------------------------------------------------------------------------------------------------


CREATE OR REPLACE PROCEDURE create_account(
  IN p_user_id integer,
  IN p_account_number varchar(20),
  IN p_primary_password varchar(4),
  IN p_balance numeric(20, 2),
  IN p_date_opened date,
  IN p_account_status boolean
)
LANGUAGE plpgsql
AS $$
BEGIN
  -- ایجاد یک transaction
  BEGIN
    -- ایجاد یک نمونه در جدول BANK_ACCOUNT
    INSERT INTO BANK_ACCOUNT(user_id, account_number, primary_password, Balance, date_opened, account_status)
    VALUES (p_user_id, p_account_number, p_primary_password, p_balance, p_date_opened, p_account_status);

    -- ایجاد یک نمونه در جدول MINIMUMMONEY
    INSERT INTO MINIMUMMONEY(account_number, min_amount, date)
    VALUES (p_account_number, p_balance, p_date_opened);
  EXCEPTION
    WHEN OTHERS THEN
      ROLLBACK;
      RAISE;
  END;
  COMMIT;
END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION transfer_fund(
  IN source_account varchar(32),
  IN destination_account varchar(32),
  IN transfer_amount DEC,
  IN pass varchar(20)
) RETURNS TABLE (
  id INT,
  source_account_number varchar(32),
  destination_account_number varchar(32),
  amount DEC,
  transaction_date date,
  status BOOLEAN
) LANGUAGE plpgsql
AS $$
DECLARE
  source_balance DEC;
  new_transaction RECORD;
BEGIN
    -- check the balance of the source account
    SELECT balance INTO source_balance FROM BANK_ACCOUNT WHERE account_number = source_account and primary_password = pass;

    -- if the source account has enough funds
    IF source_balance >= transfer_amount THEN
        -- subtracting the amount from the source account
        UPDATE BANK_ACCOUNT SET balance = balance - transfer_amount WHERE account_number = source_account;

        -- adding the amount to the destination account
        UPDATE BANK_ACCOUNT SET balance = balance + transfer_amount WHERE account_number = destination_account;

        -- creating a new transaction record and storing its details in new_transaction
        INSERT INTO TRANSACTIONS (source_account_number, destination_account_number, amount, transaction_date, status)
        VALUES (source_account, destination_account, transfer_amount, NOW(), TRUE)
        RETURNING * INTO new_transaction;

        ----------------------------------------------------------------------

        UPDATE MINIMUMMONEY
        SET min_amount = source_balance - transfer_amount
        WHERE date <= (CURRENT_DATE - INTERVAL '2 months') AND account_number = source_account;

        UPDATE MINIMUMMONEY
        SET min_amount = LEAST(min_amount, source_balance - transfer_amount)
        WHERE date > (CURRENT_DATE - INTERVAL '2 months') AND account_number = source_account;

        -----------------------------------------------------------------------
        -- returning the details of new_transaction
        RETURN QUERY SELECT new_transaction.id, new_transaction.source_account_number, new_transaction.destination_account_number, new_transaction.amount, new_transaction.transaction_date, new_transaction.status;
    ELSE
        -- if the source account does not have enough funds, raise an exception
        RAISE EXCEPTION 'Insufficient funds in source account';
    END IF;

END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION last_transactions(
  IN source_account varchar(32),
  IN n INT
) RETURNS TABLE (
  id INT,
  src_account_number varchar(32),
  destination_account_number varchar(32),
  amount DEC,
  transaction_date date,
  status BOOLEAN
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.source_account_number, t.destination_account_number, t.amount, t.transaction_date,t.status
    FROM TRANSACTIONS as t
    WHERE  t.source_account_number = source_account
    ORDER BY transaction_date ASC
    LIMIT n;
END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION last_transactions_date(
  IN source_account varchar(32),
  IN start_date DATE,
  IN end_date DATE
) RETURNS TABLE (
  id INT,
  src_account_number varchar(32),
  destination_account_number varchar(32),
  amount DEC,
  transaction_date date,
  status BOOLEAN
) LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT t.id, t.source_account_number, t.destination_account_number, t.amount, t.transaction_date,t.status
    FROM TRANSACTIONS as t
    WHERE  t.transaction_date >= start_date and t.transaction_date<= end_date and (t.source_account_number = source_account or t.destination_account_number = source_account)
    ORDER BY transaction_date ASC;
END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE create_loan_and_installments(
  IN p_user_id integer,
  IN p_account_number varchar(20),
  IN p_loan_amount numeric(20, 2),
  IN p_start_date timestamp,
  IN p_end_date timestamp,
  IN p_loan_status boolean
)
LANGUAGE plpgsql
AS $$
DECLARE
  v_loan_id integer;
  v_installment_amount numeric(20, 2);
BEGIN
  -- ایجاد یک instance از loan
  INSERT INTO LOAN(user_id, account_number, loan_amount, start_date, end_date, loan_status)
  VALUES (p_user_id, p_account_number, p_loan_amount, p_start_date, p_end_date, p_loan_status)
  RETURNING id INTO v_loan_id;

  -- محاسبه مبلغ هر قسط با احتساب 20% سود
  v_installment_amount := (p_loan_amount * 1.20) / 12;

  UPDATE MINIMUMMONEY
  SET active_loan = True
  WHERE account_number = p_account_number;
  -- ایجاد 12 قسط برای وام
  FOR i IN 1..12 LOOP
    INSERT INTO LOAN_INSTALLMENT(loan_id, account_number, payment_deadline, amount, date_of_payment, status)
    VALUES (v_loan_id, p_account_number, (p_start_date::date + i * INTERVAL '1 month')::date, v_installment_amount, NULL, false);
  END LOOP;
END;
$$;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_loans(
IN p_user_id integer
)
RETURNS TABLE (
  id integer,
  user_id integer,
  account_number varchar(20),
  loan_amount numeric(20, 2),
  start_date timestamp,
  end_date timestamp,
  loan_status boolean
) AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM LOAN
  WHERE LOAN.user_id = p_user_id;
END; $$
LANGUAGE plpgsql;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION get_installments(p_loan_id integer)
RETURNS TABLE (
  id integer,
  loan_id integer,
  account_number varchar(20),
  payment_deadline date,
  amount numeric(20, 2),
  date_of_payment date,
  status boolean
) AS $$
BEGIN
  RETURN QUERY
  SELECT * FROM LOAN_INSTALLMENT as l WHERE l.loan_id = p_loan_id;
END; $$
LANGUAGE plpgsql;


---------------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE pay_earliest_installment(loana_id integer)
LANGUAGE plpgsql
AS $$
DECLARE
  v_id integer;
  v_installment_amount numeric(20, 2);
  v_acc_num varchar(32);
  b_balance DEC;
  count integer;
BEGIN
    -- بدست آوردن مبلغ قسط زودترین قسط پرداخت نشده
  SELECT li.amount, li.id, li.account_number INTO v_installment_amount, v_id, v_acc_num FROM LOAN_INSTALLMENT as li
  WHERE li.loan_id = loana_id AND status = false
  ORDER BY payment_deadline ASC
  LIMIT 1;

  -- بروزرسانی وضعیت قسط به پرداخت شده
  UPDATE LOAN_INSTALLMENT as li SET status = true
  WHERE li.id = v_id AND status = false;

  -- کاهش مقدار قسط از موجودی حساب
  UPDATE BANK_ACCOUNT SET balance = balance - v_installment_amount
  WHERE account_number = v_acc_num;

  SELECT b.balance INTO b_balance FROM BANK_ACCOUNT as b
  WHERE b.account_number = v_acc_num;

  -- محاسبه امتیاز
  UPDATE MINIMUMMONEY
  SET min_amount = b_balance
  WHERE date <= (CURRENT_DATE - INTERVAL '2 months') AND account_number = v_acc_num;

  UPDATE MINIMUMMONEY
  SET min_amount = LEAST(min_amount, b_balance)
  WHERE date > (CURRENT_DATE - INTERVAL '2 months') AND account_number = v_acc_num;


  --به وجود اوردن یک نمونه از transaction
  INSERT INTO TRANSACTIONS(source_account_number, destination_account_number, amount, transaction_date, status)
  VALUES (v_acc_num, 'bank', v_installment_amount, now(),True);

  --چک کردن اخرین قسط
  SELECT COUNT(*) INTO count
  FROM LOAN_INSTALLMENT
  WHERE loan_id = loana_id AND status = FALSE;

  IF count = 0 THEN
      UPDATE LOAN
      SET loan_status = TRUE
      WHERE id = loana_id;
  END IF;
END;
$$;
