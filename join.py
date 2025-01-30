CREATE OR REPLACE TABLE trades (
    trade_id INT,
    entity STRING,
    trade_value FLOAT
);



INSERT INTO trades (trade_id, entity, trade_value) VALUES
    (1, 'NSL', 3000.50),
    (2, 'NSL2', 1500.75),
    (3, 'OTHER', 2000.25);
