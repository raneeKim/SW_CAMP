USE MARKET_DB;

create table hongong4 (
		tinyint_col tinyint,
        smallint_col smallint,
        int_col int,
        bigint_col bigint);
        
insert into hongong4 values(127, 32767, 2147483647, 9000000000000000000);

select * from hongong4;

insert into hongong4 values(128, 32768, 2147483648, 90000000000000000000);

-- 에러난 tinyint_col만 제거하고 inser
insert into hongong4(smallint_col, int_col, bigint_col) values(128, 32768, 2147483648, 90000000000000000000); -- but 모두 out of range로 에러에러에러

desc member;

select 3, 03, '003', 256*256;

select avg(price) "평균가격" from buy;

select cast("2024-04-25 17:39:29" as date) as date;

select "2024-04-25 17:39:29"  col1 , 
cast("2024-04-25 17:39:29" as date) as col2,
cast("2024-04-25 17:39:29" as time) as col3;

select avg(price) '평균가격'
 , cast(avg(price)*(-100) as signed) '평균_가격' 
 , convert(avg(price)*(-100), signed) '평균_가격2' 
from buy;
