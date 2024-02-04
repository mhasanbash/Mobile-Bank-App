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
    id             integer,
    user_id        integer,
    account_number varchar(20),
    loan_amount    numeric(20, 2),
    start_date     timestamp,
    end_date       timestamp,
    loan_status    boolean,
    PRIMARY KEY(id,user_id),
    FOREIGN KEY(user_id) REFERENCES BANK_ACCOUNT(user_id),
    FOREIGN KEY(account_number) REFERENCES BANK_ACCOUNT(account_number)
);

CREATE TABLE TRANSACTIONS
(
    id                         integer primary key,
    source_account_number      varchar(20),
    destination_account_number varchar(20),
    amount                     numeric(10, 2),
    transaction_date           timestamp,
    status                     boolean,
    description                varchar(255),
    FOREIGN KEY (source_account_number) REFERENCES BANK_ACCOUNT (account_number)
);


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
