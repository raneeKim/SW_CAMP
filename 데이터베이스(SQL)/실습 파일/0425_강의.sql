USE market_db;

CREATE TABLE hongong1 (toy_id INT, toy_name CHAR(4), age INT);
INSERT INTO hongong1 VALUES (1,'우디',25);
INSERT INTO hongong1 (toy_id, toy_name) VALUES (2,'버즈');
INSERT INTO hongong1 (toy_name, age, toy_id) VALUES ('제시',20,3);

insert into hongong1 values (4,'아이폰',null);



select * from hongong1;