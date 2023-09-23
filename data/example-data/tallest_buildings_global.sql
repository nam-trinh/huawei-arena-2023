CREATE TABLE talles_buildings(
	-- The list of tallest buildins in the world.
	-- Downloaded from https://www.kaggle.com/datasets/axeltorbenson/tallest-buildings-in-the-world
  rank int,
  name varchar(50),
  height_m float, -- Height in meters
  height_ft float, -- Height in feets
  year_built int,
  floors_above int,
  floors_below_ground int,
  city varchar(50),
  country varchar(50)
);
.import --csv --skip 1 csv/tallest_buildings_global.csv talles_buildings

