-- 회사에서는 절대 auto commit을 하지 않는다!! -> auto commit 언체크하기 / command창에서 set autocommit=0; 
select @@autocommit;

USE market_db;

select * from buy;

-- count(*) : null값 포함, count(열이름) : null값 미포함
select count(*), count(mem_id), count(group_name) from buy;

-- 구매횟수가 2이상인 멤버
select mem_id from buy
group by mem_id
having count(*) >= 2;

-- 구매횟수가 2이상인 멤버 + 구매횟수 많은 순서대로 동일하면 mem_id 역순
select mem_id, count(*) total_count from buy
group by mem_id
having count(*) >= 2
order by total_count, mem_id desc;

-- 총구매액을 조회
select mem_id, count(*) total_count, sum(price*amount) total_price from buy
group by mem_id
having count(*) >= 2
order by total_count, mem_id desc;

desc hongong1;

create table testtbl1 (id int, username char(3), age int);

desc testtbl1;

insert into testtbl1 values (1,'뽀로로',16);
insert into testtbl1 values (2,'크롱',null);
insert into testtbl1 values (3,'루피',14);

select * from testtbl1;

-- auto_increment : pk에 자주 사용. 자동으로 1씩 증가
create table hongong2 (toy_id int auto_increment primary key, toy_name char(4), age int);

desc hongong1;
desc hongong2;

insert into hongong2 values (null, '보핍', 25); -- 작동O > pk가 null값이라도 auto_increment로 자동 배정
insert into hongong1 values (null, '보핍', 25); -- 에러 > pk가 null값이므로

insert into hongong2 values (1, '보핍', 25); -- 에러 > pk인 toy_id에 이미 1이 있으므로
insert into hongong2 values (2, '보핍', 25); -- 작동O

select * from hongong2;

insert into hongong2 values (null, '렉스', 21);
insert into hongong2 values (null, '슬링키', 18); -- 임의의 값 보다 null로 하렴

select last_insert_id();
show create table hongong2;
alter table hongong2 auto_increment = 100;
