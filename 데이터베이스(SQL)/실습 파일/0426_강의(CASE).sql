-- BUY, MEMBER 사용해서 회원별 총 구매액 구하기
SELECT MEM_ID, MEM_NAME, SUM(PRICE*AMOUNT) AS TOTAL_PRICE 
FROM BUY RIGHT JOIN MEMBER USING (MEM_ID)
GROUP BY MEM_ID
ORDER BY 3 DESC;

SELECT MEM_ID, MEM_NAME, SUM(PRICE*AMOUNT) AS TOTAL_PRICE ,
	CASE WHEN SUM(PRICE*AMOUNT) >= 1500 THEN '최우수고객'
        WHEN SUM(PRICE*AMOUNT) >= 100 THEN '우수고객'
        WHEN SUM(PRICE*AMOUNT) >= 1 THEN '일반고객'
        ELSE '유령고객' END AS '회원등급'
FROM BUY RIGHT JOIN MEMBER USING (MEM_ID)
GROUP BY MEM_ID
ORDER BY 3 DESC;

-- CASE는 위 조건부터 걸러져서 내려오므로 1이상인 모든걸 일반고객 명시 후 내려옴. -> 전부 일반고객이됨(유령고객제외)
SELECT MEM_ID, MEM_NAME, SUM(PRICE*AMOUNT) AS TOTAL_PRICE ,
	CASE WHEN SUM(PRICE*AMOUNT) >= 1 THEN '일반고객' -- 1000미만을 꼭 넣어줘야함
        WHEN SUM(PRICE*AMOUNT) >= 1000 THEN '최우수고객' 
        WHEN SUM(PRICE*AMOUNT) >= 1500 THEN '우수고객'
        ELSE '유령고객' END AS '회원등급'
FROM BUY RIGHT JOIN MEMBER USING (MEM_ID)
GROUP BY MEM_ID
ORDER BY 3 DESC;