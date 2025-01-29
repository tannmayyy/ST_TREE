CREATE OR REPLACE TABLE user_access_mapping (
    user_name STRING PRIMARY KEY,
    category_access STRING  -- 'nsl' or 'non-nsl'
);

INSERT INTO user_access_mapping (user_name, category_access) VALUES
    ('tanmay', 'nsl'),
    ('dhriti', 'non-nsl');



CREATE OR REPLACE ROW ACCESS POLICY rls_policy_nsl_non_nsl
AS (category STRING)
RETURNS BOOLEAN ->
    EXISTS (
        SELECT 1 FROM user_access_mapping 
        WHERE user_name = CURRENT_USER() 
        AND category_access = category
    );



CREATE OR REPLACE VIEW restricted_view AS
SELECT * FROM original_table;


ALTER VIEW restricted_view 
ADD ROW ACCESS POLICY rls_policy_nsl_non_nsl ON (category);



For Tanmay (nsl access)
sql
Copy code
SELECT * FROM restricted_view;


