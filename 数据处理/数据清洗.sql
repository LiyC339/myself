DELETE FROM merged_output WHERE
已上映天数 = '展映' OR 已上映天数 = '点映' OR 已上映天数 = '零点场' OR 上座率 = '--' OR
当日票房 = '0.0' OR 场均人次 < '1' OR 排片占比 < '0.1' OR 已上映天数 IS NULL;

UPDATE merged_output SET 已上映天数 = '上映1天' WHERE 已上映天数 = '上映首日';

CREATE TABLE movie_id AS SELECT DISTINCT 电影ID AS movie_id FROM merged_output;

ALTER TABLE merged_output
ADD 出品国家 VARCHAR(255),
ADD 电影类别1 VARCHAR(255),
ADD 电影类别2 VARCHAR(255),
ADD 电影类别3 VARCHAR(255),
ADD 电影评分 INT,
ADD 男性占比 VARCHAR(255),
ADD 女性占比 VARCHAR(255),
ADD 节假日 VARCHAR(255);
