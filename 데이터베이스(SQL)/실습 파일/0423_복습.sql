select * from member
order by debut_date;

select * from member
order by mem_number;

select * from member
order by mem_number desc;

-- 인원수대로 조회하되, 인원수가 같으면 키 순서로 조회
select * from member
order by mem_number, height; 

select * from member
where mem_number IN (4,6);