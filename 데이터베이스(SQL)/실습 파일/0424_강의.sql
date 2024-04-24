-- order + limit -> 인덱싱 가능함 (숫자0이 1행)
select * from member
order by mem_number
limit 1,3;

-- order by 뒤의 숫자 의미 : select된 컬럼의 순서
select distinct mem_number from member order by 1;

-- GROUP BY vs ORDER BY
select mem_id, amount from buy
order by mem_id;

select mem_id, sum(amount) from buy
group by mem_id;

select mem_id, sum(amount) from buy
group by mem_id
order by mem_id;

select mem_id, sum(amount) from buy
group by mem_id
order by 2 desc;

-- 구매 수량의 합이 높은 순서대로, mem_id를 역순으로 조회
select mem_id, sum(amount) as amount from buy
group by mem_id
order by 1 desc;

select mem_id, sum(amount) as "총 구매 개수" from buy
group by mem_id
order by 1 desc;

select mem_id, sum(amount) as "총 구매 개수", sum(amount*price) as "총 구매 금액" from buy
group by mem_id
order by 1 desc;

select mem_id, sum(amount) as "총 구매 개수", sum(amount*price) as "총 구매 금액", avg(amount*price) as "평균 구매 금액" from buy
group by mem_id
order by 1 desc;

-- 주소가 서울인 회원은 몇명인가
select count(*) 
from member
where addr = '서울'
group by addr;

select count(*) 
from member
group by addr
having addr = '서울';

select addr, count(*) as '인원수' from member
group by addr
order by 인원수;

select count(addr), count(*), count(phone1), count(phone2) from member
where addr = '서울';

-- 전화번호가 있는 사람들만 조회
select count(phone1) from member;
select count(*) from member where phone1 is not null;

/*
count(*) -> null 값을 제외한 데이터를 카운팅
count(열이름) -> null 값을 제외한 데이터를 카운팅
*/

-- 전화번호가 있되, 지역이 서울인 데이터만 조회
select count(*) from member where addr = '서울' and phone1 is not null;


-- HAVING절
select mem_id, sum(amount) as "총 구매 개수", sum(amount*price) as "총 구매 금액", avg(amount*price) as "평균 구매 금액" from buy
where "총 구매 금액" >= 1000
group by mem_id
order by 1 desc;
/*
Alias는 ORDER BY절만 가능 
다음과 같은 순서이므로, alias를 지정한 후인 order by절만 사용가능
FROM
WHERE
GROUP BY
SELECT
ORDER BY
*/

select mem_id, sum(amount) as "총 구매 개수", sum(amount*price) as "총 구매 금액", avg(amount*price) as "평균 구매 금액" from buy
where sum(amount*price) >= 1000
group by mem_id
order by 1 desc;
/*
FROM
WHERE
GROUP BY
HAVING : 집계함수와 관련된
SELECT
ORDER BY
*/

-- member에서 지역별 인원수
select addr, count(*) from member
group by addr;

select addr, count(*), count(addr), count(distinct addr) from member
group by addr;

select count(*), count(addr), count(distinct addr) from member;

select * from buyTBL;

-- 구매 테이블 (buyTBL)에서 아이디(userID)마다 구매한 물건의 개수(amount)를 조회
Select userID, sum(amount) from buyTBL
group by userID;

-- 구매 테이블 (buyTBL)에서 아이디(userID)마다 구매액의 총합(amount)을 조회
select userId, sum(amount) total_amount , sum(price*amount) total_price from buyTBL
group by userID;

-- 구매 테이블 (buyTBL)에서 회원별로 한번 구매할때마다 평균적으로 몇개를 구매했는지 조회
select userID, avg(amount) avg_amount from buyTBL
group by userID;

-- 구매 테이블 (buyTBL)에서 총 구매액이 적은 회원 순으로 정렬
select userId, sum(price*amount) as total_price from buyTBL
group by userID
order by  total_price desc;

-- 사용자 테이블 (userTBL)에서 가장 키가 큰 회원과 가장 키가 작은 회원의 이름과 키 출력
SELECT userName, height from userTBL
where height = (select max(height) from userTBL) 
	or height = (select min(height) from userTBL);

select * from userTBL ;
select userName, max(height) from userTBL group by userName;

-- 구매 테이블 (buyTBL)에서 분류(groupName)별 합계 및 그 총합 구하기
select groupName, sum(amount) total_amount , sum(price*amount) total_price from buyTBL
group by groupName;

-- 구매 테이블 (buyTBL)에서 총 구매액이 1000이상인 회원에게만 사은품을 증정하고 싶다면?
select groupName from buyTBL
group by groupName
having sum(price*amount) >= 1000;

-- 테이블 전체 정보
desc buytbl; 