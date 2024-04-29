create table member2
( mem_id char(8) not null primary key,
mem_name varchar(10) not null,
height tinyint unsigned null);

create table member3
( mem_id char(8) not null,
mem_name varchar(10) not null,
height tinyint unsigned null);

show create table member3;
alter table member3 add constraint primary key pk_member3(mem_id);


insert into member2 (select mem_id, mem_name, height from member where mem_id = 'BLK');
commit;
select * from buy join member2 using (mem_id);
update member2 set mem_id = 'pink' where mem_id = 'BLK';

select * from member2; 
rollback;

--
select * from member join buy using (mem_id);
update member set mem_id =  'pink' where mem_id = 'BLK'; -- 에러 : 자식테이블인 buy에 mem_id가 외래키로 설정되어있어서 부모테이블인 member에서 수정,삭제 불가

drop table if exists buy;
create table buy
(num int auto_increment not null primary key,
mem_id char(8) not null,
prod_name char(6) not null);

alter table buy add constraint
foreign key(mem_id) references member(mem_id)
on update cascade
on delete cascade;

update member set mem_id =  'pink' where mem_id = 'BLK'; -- 


drop table if exists member;
create table member(
mem_id char(8) not null primary key,
mem_name varchar(10) not null,
height tinyint unsigned null,
email char(30) null unique);

alter table member add constraint check(height>=100);
alter table member add (phone1 char(3));
alter table member add constraint check (phone1 in ('02','031','032','054','053','061'));
select * from member;

insert into member values('BLK', '블랙핑크', 163, null,'02');
insert into member values('TWC', '트와이스', 99, null,'02'); -- 에러 : check제약조건(height>=100)에서 벗어나서
insert into member values('TWC', '트와이스', 159, null,'010');  -- 에러 : check제약조건(phone1 in...)에서 벗어나서

alter table member
	alter column phone1 set default '02';
    
insert into member VALUES('RED','레드벨벳',161,NULL,NULL); -- 디폴트값 설정해도 NULL로 지정하면 NULL값 들어감
INSERT INTO MEMBER VALUES('SPC','우주소녀',NULL,DEFAULT,DEFAULT); -- 
ROLLBACK;