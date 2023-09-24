CREATE TABLE covid_vaccinations
    -- COVID-19 Vaccination Rates
    -- URL: https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/CDC45/CSV/1.0/en
(
  STATISTIC_CODE varchar(10), -- Statistic code
  Statistic_Label varchar(30), -- Statistic label
  `TLIST(M1)` int, -- Time period of statistic
  Month varchar(20), -- Time period human-readable
  `C03898V04649` varchar(30),
  `Local Electoral Area` varchar(50),
  `C02076V03371` varchar(10),
  `Age Group` varchar(30),
  `UNIT` varchar(10),
  `VALUE` float
);
.import --csv --skip 1 csv/CDC45.20230830164717.csv covid_vaccinations
UPDATE covid_vaccinations SET VALUE=cast(VALUE as float);

