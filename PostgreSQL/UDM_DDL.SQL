CREATE TABLE users (_id text  YES, username text  YES, email text  YES, password text  YES, firstname text  YES, lastname text  YES, address text  YES, phone text  YES, isadmin text  YES);

CREATE TABLE products (_id text  YES, name text  YES, description text  YES, price text  YES, brand text  YES, category text  YES, imageurl text  YES);

CREATE TABLE activities (_id text  YES, user_id text  YES, activitytype text  YES, productid text  YES, timestamp text  YES);

CREATE TABLE payments (_id text  YES, user_id text  YES, amount text  YES, paymentdate text  YES, paymentmethod text  YES);

CREATE TABLE brands (_id text  YES, name text  YES, description text  YES, logourl text  YES, website text  YES);