-- 일부 데이터를 가져와 create table -> CTAS
select * from buy where mem_id = 'BLK';
create table buy_blk as select * from buy where mem_id = 'BLK';

select * from buy_blk;

-- MMU의 NUM, ID, PROD_NAME, 총구매금을 조회해서 BUY_MMU 테이블 만들기
USE MARKET_DB;
SELECT * FROM buy WHERE MEM_ID = 'MMU';
CREATE TABLE BUY_MMU AS (SELECT NUM,MEM_ID,PROD_NAME, (PRICE*AMOUNT) TOTAL_PRICE FROM BUY WHERE MEM_ID = 'MMU');
SELECT * FROM BUY_MMU;

use world;
select * from city limit 5; 

-- 도시이름과 인구를 조회
select name,population from city;

create table city_popul as (select name city_name, population city_cnt from city);
select * from city_popul;
DROP TABLE CITY_POPUL;

CREATE TABLE CITY_POPUL (CITY_NAME CHAR(35), POPULATION INT);
SELECT * FROM city_popul;

INSERT INTO CITY_POPUL (select NAME,POPULATION FROM CITY);
SELECT * FROM CITY_POPUL;

-- MEMBER_COPY
CREATE TABLE market_db.MEMBER_COPY AS (SELECT * FROM market_db.MEMBER);
UPDATE market_db.MEMBER_COPY SET MEM_NUMBER = 7; -- 안전모드 설정으로 에러가 뜰수도 해지하고 다시
SELECT * FROM market_db.member_copy; -- mem_number가 모두 7로 변경됨 why? where절을 사용하지않았기 때문
UPDATE market_db.MEMBER_COPY SET MEM_NUMBER = 8 where mem_name = '에이핑크';

select * from city_popul where city_name = 'Seoul';
UPDATE CITY_POPUL SET CITY_NAME = '서울' WHERE CITY_NAME = 'Seoul'; 
SELECT * FROM CITY_POPUL WHERE CITY_NAME = '서울';

SELECT * FROM CITY_POPUL WHERE CITY_NAME = 'New York';
update CITY_POPUL SET POPULATION = 0 , CITY_NAME = '뉴욕' WHERE CITY_NAME = 'New York';
SELECT * FROM CITY_POPUL WHERE CITY_NAME = '뉴욕';

SELECT CITY_NAME, POPULATION/1000 FROM CITY_POPUL;

update city_popul SET POPULATION = POPULATION/1000;
SELECT * FROM CITY_POPUL;