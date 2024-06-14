-- 创建一个包含2023年所有日期的临时表
WITH RECURSIVE DateSeries AS (
    SELECT DATE('2023-01-01') AS date
    UNION ALL
    SELECT date + INTERVAL 1 DAY
    FROM DateSeries
    WHERE date + INTERVAL 1 DAY <= '2023-12-31'
)
-- 找到所有的星期六和星期天，并将它们格式化为MMDD
, Weekends AS (
    SELECT DATE_FORMAT(date, '%c%d') AS MMDD, 
           CASE 
               WHEN DAYOFWEEK(date) = 1 THEN '周日' -- 1 表示周日
               WHEN DAYOFWEEK(date) = 7 THEN '周六' -- 7 表示周六
           END AS Holiday
    FROM DateSeries
    WHERE DAYOFWEEK(date) IN (1, 7)
)
-- 更新movie2表中的节假日字段
UPDATE movie2 m
JOIN Weekends w ON m.日期 = w.MMDD
SET m.节假日 = w.Holiday;
