CREATE TABLE users
    -- List of system users
(
  user_id int,
  username varchar(50),
  password varchar(50),
  is_admin bool
);
INSERT INTO users VALUES (1, "admin", "admin", true), (5, "user", "pass", false);


CREATE TABLE orders
    -- List of user orders
(
  order_id int,
  user_id int,
  `date` date,
  value float,
  paid bool
);
INSERT INTO orders VALUES (1, 1, "2022-05-05", 100, true), (2, 5, "2022-05-07", 100, true), (3, 5, "2022-05-09", 300, true), (4, 5, "2022-05-17", 1000, false);

