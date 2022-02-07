SET search_path to country;


CREATE TABLE "country" (
    "country_name" text   NOT NULL,
    "region" text ,
    "population" int ,
    "area" int ,
    "population_des" numeric ,
    "coastline" numeric ,
    "net_migration" numeric  ,
    "infant_mortality" numeric ,
    "literacy" numeric ,
    "phones" numeric ,
    "arable" numeric ,
    "crops" numeric ,
    "other" numeric ,
    "climate" int ,
    "birthrate" numeric ,
    "deathrate" numeric ,
    "agriculture" numeric ,
    "industry" numeric ,
    "service" numeric ,
    CONSTRAINT "pk_Country" PRIMARY KEY (
        "country_name"
     )
);

CREATE TABLE "score" (
    "country_name" text   NOT NULL,
    "happiness_rank" int   NOT NULL,
    "happiness_score" numeric   NOT NULL,
    "GDP" money   NOT NULL,
    "year" SMALLINT   NOT NULL,
    UNIQUE (country_name, year)
);
ALTER TABLE "score" ADD CONSTRAINT "fk_Score_country_name" FOREIGN KEY("country_name")
REFERENCES "country" ("country_name");





    


