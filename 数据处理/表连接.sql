UPDATE merged_output bo
JOIN id_movie_class m ON bo.电影id = m.电影id
SET
    bo.出品国家 = m.出品国家,
    bo.电影类别1 = m.电影类别1,
    bo.电影类别2 = m.电影类别2,
    bo.电影类别3 = m.电影类别3,
    bo.电影评分 = m.电影评分,
    bo.男性占比 = m.男性占比,
    bo.女性占比 = m.男性占比;