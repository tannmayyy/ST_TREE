CREATE OR REPLACE ROW ACCESS POLICY user_entity_access_policy
AS (entity STRING)
RETURNS BOOLEAN ->
    EXISTS (
        SELECT 1 FROM user_access
        WHERE user_name = CURRENT_USER()
        AND (
            category = 'NSL'  -- NSL users see all data
            OR (category <> 'NSL' AND entity <> 'NSL') -- Non-NSL users should NOT see NSL data
        )
    );
