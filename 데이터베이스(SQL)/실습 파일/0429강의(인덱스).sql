DROP TABLE MEMBER;
CREATE TABLE MEMBER 
( MEM_ID CHAR(8),
MEM_NAME CHAR(10),
MEM_NUMBER INT,
ADDR CHAR(2));

INSERT INTO member VALUES('TWC', '트와이스', 9, '서울');
INSERT INTO member VALUES('BLK', '블랙핑크', 4, '경남');
INSERT INTO member VALUES('WMN', '여자친구', 6, '경기');
INSERT INTO member VALUES('OMY', '오마이걸', 7, '서울');
COMMIT;

SELECT * FROM MEMBER;
/*
TWC	트와이스	9	서울
BLK	블랙핑크	4	경남
WMN	여자친구	6	경기
OMY	오마이걸	7	서울
*/

ALTER TABLE MEMBER ADD CONSTRAINT PRIMARY KEY(MEM_ID);
/* 기본키를 기준으로 자동 정렬됨.
BLK	블랙핑크	4	경남
OMY	오마이걸	7	서울
TWC	트와이스	9	서울
WMN	여자친구	6	경기
*/

ALTER TABLE MEMBER DROP PRIMARY KEY;

ALTER TABLE MEMBER ADD CONSTRAINT UNIQUE(MEM_ID);
/* 정렬x
TWC	트와이스	9	서울
BLK	블랙핑크	4	경남
WMN	여자친구	6	경기
OMY	오마이걸	7	서울
*/
DESC MEMBER; 

ALTER TABLE MEMBER ADD CONSTRAINT UNIQUE(MEM_NAME);