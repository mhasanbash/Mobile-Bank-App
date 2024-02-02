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


insert into USERS values(1,'hasan','hasan','hassan','hassany','isfahan','','','2019.2.1',True);
insert into USERS values(2,'admin','admin','admin','admin','isfahan','admin','admin','','');

INSERT INTO BANK_ACCOUNT(user_id,account_number,primary_password,Balance,date_opened,account_status)VALUES(1,'54156',1234,1000,'2017-06-15',true);


CREATE OR REPLACE PROCEDURE transfer_funds(
  source_account INT,
  destination_account INT,
  amount DEC,
  pass varchar(4)
) LANGUAGE plpgsql
AS $$
DECLARE
  source_balance DEC;
BEGIN
    -- check the balance of the source account
    SELECT balance INTO source_balance FROM BANK_ACCOUNT WHERE account_number = source_account and primary_password = pass;

    -- if the source account has enough funds
    IF source_balance >= amount THEN
        -- subtracting the amount from the source account
        UPDATE BANK_ACCOUNT SET balance = balance - amount WHERE account_number = source_account;

        -- adding the amount to the destination account
        UPDATE BANK_ACCOUNT SET balance = balance + amount WHERE account_number = destination_account;

        -- creating a new transaction record
        INSERT INTO TRANSACTIONS (source_account_number, destination_account_number, amount, transaction_date, status)
        VALUES (source_account, destination_account, amount, NOW(), TRUE);
    ELSE
        -- if the source account does not have enough funds, raise an exception
        RAISE EXCEPTION 'Insufficient funds in source account';
    END IF;

    COMMIT;
END;
$$;

SELECT usr.first_name , usr.last_name
FROM BANK_ACCOUNT as acc, USERS as usr
WHERE acc.account_number = '64648238317022143105' and acc.user_id = usr.id