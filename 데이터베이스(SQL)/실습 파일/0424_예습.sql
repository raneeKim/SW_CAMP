use market_db;

CREATE TABLE userTBL -- 회원 테이블
( userID  	CHAR(8) NOT NULL PRIMARY KEY, -- 사용자 아이디(PK)
  userName    	VARCHAR(10) NOT NULL, -- 이름
  birthYear   INT NOT NULL,  -- 출생년도
  addr	  	CHAR(2) NOT NULL, -- 지역(경기,서울,경남 식으로 2글자만입력)
  mobile1	CHAR(3), -- 휴대폰의 국번(011, 016, 017, 018, 019, 010 등)
  mobile2	CHAR(8), -- 휴대폰의 나머지 전화번호(하이픈제외)
  height    	SMALLINT,  -- 키
  mDate    	DATE  -- 회원 가입일
);
CREATE TABLE buyTBL -- 회원 구매 테이블
(  num 		INT AUTO_INCREMENT NOT NULL PRIMARY KEY, -- 순번(PK)
   userID  	CHAR(8) NOT NULL, -- 아이디(FK)
   prodName 	CHAR(6) NOT NULL, --  물품명
   groupName 	CHAR(4)  , -- 분류
   price     	INT  NOT NULL, -- 단가
   amount    	SMALLINT  NOT NULL, -- 수량
   FOREIGN KEY (userID) REFERENCES userTBL(userID)
);

INSERT INTO userTBL VALUES('YJS', '유재석', 1972, '서울', '010', '11111111', 178, '2008-8-8');
INSERT INTO userTBL VALUES('KHD', '강호동', 1970, '경북', '011', '22222222', 182, '2007-7-7');
INSERT INTO userTBL VALUES('KKJ', '김국진', 1965, '서울', '019', '33333333', 171, '2009-9-9');
INSERT INTO userTBL VALUES('KYM', '김용만', 1967, '서울', '010', '44444444', 177, '2015-5-5');
INSERT INTO userTBL VALUES('KJD', '김제동', 1974, '경남', NULL , NULL      , 173, '2013-3-3');
INSERT INTO userTBL VALUES('NHS', '남희석', 1971, '충남', '016', '66666666', 180, '2017-4-4');
INSERT INTO userTBL VALUES('SDY', '신동엽', 1971, '경기', NULL , NULL      , 176, '2008-10-10');
INSERT INTO userTBL VALUES('LHJ', '이휘재', 1972, '경기', '011', '88888888', 180, '2006-4-4');
INSERT INTO userTBL VALUES('LKK', '이경규', 1960, '경남', '018', '99999999', 170, '2004-12-12');
INSERT INTO userTBL VALUES('PSH', '박수홍', 1970, '서울', '010', '00000000', 183, '2012-5-5');

INSERT INTO buyTBL VALUES(NULL, 'KHD', '운동화', NULL   , 30,   2);
INSERT INTO buyTBL VALUES(NULL, 'KHD', '노트북', '전자', 1000, 1);
INSERT INTO buyTBL VALUES(NULL, 'KYM', '모니터', '전자', 200,  1);
INSERT INTO buyTBL VALUES(NULL, 'PSH', '모니터', '전자', 200,  5);
INSERT INTO buyTBL VALUES(NULL, 'KHD', '청바지', '의류', 50,   3);
INSERT INTO buyTBL VALUES(NULL, 'PSH', '메모리', '전자', 80,  10);
INSERT INTO buyTBL VALUES(NULL, 'KJD', '책'    , '서적', 15,   5);
INSERT INTO buyTBL VALUES(NULL, 'LHJ', '책'    , '서적', 15,   2);
INSERT INTO buyTBL VALUES(NULL, 'LHJ', '청바지', '의류', 50,   1);
INSERT INTO buyTBL VALUES(NULL, 'PSH', '운동화', NULL   , 30,   2);
INSERT INTO buyTBL VALUES(NULL, 'LHJ', '책'    , '서적', 15,   1);
INSERT INTO buyTBL VALUES(NULL, 'PSH', '운동화', NULL   , 30,   2);

select * from userTBL;

-- userTBL 테이블에서 1970년 이후에 출생했고 키가 182 이상인 사람의 아이디와 이름을 조회
select userID,userName from userTBL
where birthYear >= 1970 and height >= 182; 

-- userTBL 테이블에서 키가 180~182 사람 조회
select * from userTBL
where height between 180 and 182;

-- userTBL 테이블에서 경남 또는 충남 또는 경북인 사람 조회
select * from userTBL
where addr IN ('경남','충남','경북');

-- userTBL 테이블에서 성이 김씨인 회원의 이름과 키 조회
select userName, height from userTBL
where userName like '김%';

-- userTBL 테이블에서 맨 앞의 한글자가 무엇이든 상관없고 그 다음이 경규 인 사람 조회
select * from userTBL
where userName like '_경규';

-- userTBL 테이블에서 김용만보다 키가 크거나 같은 사람 이름과 키 출력
select userName,height from userTBL
where height >= (select height from userTBL where userName = '김용만') 
	and userName != '김용만';

-- userTBL 테이블에서 지역이 경기인 사람보다 키가 크거나 같은 사람 추출
select * from userTBL
where height >= (select max(height) from userTBL where addr = '경기')
	and addr != '경기';

