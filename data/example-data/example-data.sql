CREATE TABLE pre_ranking_filter_log
    -- pre_ranking filtering log
(
  filter_key varchar(50), -- filtering reason
  `timestamp` date, -- event timeframe
  task int -- task id
);
.import --csv --skip 1 csv/pre_ranking_filter_log.csv pre_ranking_filter_log


CREATE TABLE pre_ranking_filter_key_mapping
    -- pre_ranking filtering key mapping to chinese and english
(
  filter_key_zh varchar(50), -- filter key description in chinese
  filter_key varchar(50), -- filter key
  filter_key_en varchar(50), -- filter key description in english
  filter_stage varchar(50), -- filtering stage
  filter_stage_zh varchar(50), -- filtering stage description in chinese
  filter_type_zh varchar(50), -- filter type description in chinese
  filter_type_en varchar(50) -- filter type description in english
);
.import --csv --skip 1 csv/pre_ranking_filter_key_mapping.csv pre_ranking_filter_key_mapping


CREATE TABLE predicted_metric_log
    -- Forecasted metrics
(
  `date` date, -- recroding date
  task int, -- task id
  avg_ctr float, -- daily average CTR
  avg_cvr float, -- daily average CVR
  avg_unit_price float, -- daily average unit price
  avg_ecpm float -- daily average ECPM
);
.import --csv --skip 1 csv/predicted_metric_log.csv predicted_metric_log


CREATE TABLE real_metric_log
    -- Actual collected metrics
(
  `date` date, -- recroding date
  task int, -- task id
  avg_ctr float, -- daily average CTR
  avg_cvr float, -- daily average CVR
  avg_unit_price float, -- daily average unit price
  avg_ecpm float -- daily average ECPM
);
.import --csv --skip 1 csv/real_metric_log.csv real_metric_log

CREATE TABLE request_log
    -- Daily requests log
(
  `date` date, -- Request date
  request_id varchar(20), -- Request ID
  task int -- task id
);
.import --csv --skip 1 csv/request_log.csv request_log

