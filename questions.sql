SET search_path to country;

--a) What was the happiest country each year (year, country)?
SELECT year,country_name 
FROM score 
WHERE happiness_rank = 1 
ORDER BY year;

--b) What was the average happiness each year (year, happiness)?
SELECT year, ROUND(AVG(happiness_score),3) 
FROM score
GROUP BY year
ORDER BY year

--c) In which position was Portugal in the happiness index each year (year, position)?
SELECT year, happiness_rank 
FROM score 
WHERE country_name
LIKE 'Portugal'
ORDER BY year;

--d1) What is the average happiness of the 10 countries with the higher GDP in each year(year, happiness)?
SELECT year, avg(t.happiness_score) 
FROM (
    SELECT * ,RANK () OVER ( PARTITION BY year ORDER BY gdp DESC) rank_number
	FROM score ORDER BY gdp DESC) t
WHERE year IN (2015,2016,2017,2018,2019) AND t.rank_number <= 10
GROUP BY t.year

--d2)What about the lower GDP? (year,happinness)
SELECT year, AVG(t.happiness_score) 
FROM (
	SELECT * ,RANK () OVER ( PARTITION BY year ORDER BY gdp ASC) rank_number
	FROM score ORDER BY gdp DESC) t
WHERE t.year IN (2015,2016,2017,2018,2019) AND t.rank_number <= 10
GROUP BY t.year

--d3)higher infant mortality? (country,happinness,infant mortality)
SELECT s.country_name, AVG(s.happiness_score), MAX(c.infant_mortality) FROM score s
JOIN country c 
ON s.country_name=c.country_name
WHERE literacy IS NOT NULL
GROUP BY s.country_name
ORDER BY MAX(c.infant_mortality) DESC, AVG(s.happiness_score) DESC
LIMIT 10

--d4)higher literacy? (country,happinness,literacy)
SELECT s.country_name, avg(s.happiness_score),max(c.literacy) FROM score s
JOIN country c 
ON s.country_name=c.country_name
wWHEREhere literacy IS NOT NULL
GROUP BY s.country_name
ORDER BY max(c.literacy) DESC,avg(s.happiness_score) DESC
LIMIT 10

--e) What are the three countries with a greater improvement in the happiness index
-- during the years (notice that we can have more years than those in the dataset)
-- present in the database (country, improvement)?
SELECT country_name, hp_max_year-hp_min_year AS develop_happiness_index
FROM (
	SELECT country_name, happiness_score AS hp_min_year
    FROM score  WHERE year=(
		SELECT MIN(year)
		FROM score)
	) AS Tab1
INNER JOIN
	(SELECT country_name, happiness_score AS hp_max_year
    FROM score  WHERE year=(
		SELECT MAX(year)
		FROM score)
	) AS Tab2
USING(country_name)
ORDER BY develop_happiness_index DESC
LIMIT 3

--EXTRA

--Which was the top 5 countries with the higher average of happiness FROM 2015-2019? (Country, happiness index)
SELECT country_name, AVG(happiness_score) FROM score
GROUP BY country_name
ORDER BY AVG(happiness_score) DESC
LIMIT 5

--Which is the deviation on hapiness index between Portugal and the global avg over the years? 
SELECT country_name, hpPortugal, hp_avg_global,year, (hpPortugal-hp_avg_global) AS PT_deviation_global
FROM
(SELECT country_name, year,happiness_score AS hpPortugal
    FROM score  WHERE country_name = 'Portugal'
) AS Tab1
 INNER JOIN
(SELECT year, avg(happiness_score) AS hp_avg_global
    FROM score
 group by year
) AS Tab2
USING(year)

--which countries have the higher change on Happiness index (negative/positive)?
SELECT country_name, min(happiness_score),max(happiness_score), (max(happiness_score) - min(happiness_score)) as score_range
FROM score
GROUP BY country_name
ORDER BY score_range DESC
LIMIT 5