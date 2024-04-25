DELETE FROM world.city_popul;
drop table world.city_popul;
create table world.city_popul as (select name city_name, population from world.city);

select * from world.city_popul where city_name like 'New%'; -- 12개 -> 7개

delete from world.city_popul where city_name like 'New%' limit 5;
commit; 
/*
workbench에서 delete하고 command창에서 결과확인하면 delete되어 있지않음 -> commit을 하지 않았기 때문
다시 workbenc에서 commit 실행 후 , command창에서 확인하면 delete 되어 있음 (command창을 따로 끄거나 새로 로그인하지 않아도 됨)
*/

drop table world.city_popul;
create table world.city_popul as (select name city_name, population from world.city);

select count(*) from world.city_popul where city_name like 'New%'; -- 12개
delete from world.city_popul where city_name like 'New%' limit 5; 
select count(*) from world.city_popul where city_name like 'New%'; -- 7개
rollback; -- 12개로 다시 rollback
commit; -- 12개로 commit
select count(*) from world.city_popul where city_name like 'New%'; -- 12개

create table big_table1 (select * from world.city, sakila.country);
create table big_table2 (select * from world.city, sakila.country);
create table big_table3 (select * from world.city, sakila.country);

select count(*) from big_table1; -- 16.547sec

delete from big_table1; -- 1.68sec
select * from big_table1; -- 빈테이블 (delete) 
rollback;
select count(*) from big_table1;
delete from big_table1 where Name like 'New%'; -- 가능

drop table big_table2; -- 0.078sec
select * from big_table2; -- 에러 (drop)

truncate table big_table3; -- 0.016sec
-- auto commit
-- truncate table big_table3 where Name like 'New%' 불가능
select * from big_table3; -- 빈테이블 (truncate)