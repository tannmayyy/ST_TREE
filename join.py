CREATE OR REPLACE ROW ACCESS POLICY trades_row_policy 
AS (entity STRING)
RETURNS BOOLEAN ->
EXISTS (
    SELECT 1 
    FROM user_access_mapping 
    WHERE user_name = CURRENT_USER()
      AND (
          category_access = 'NSL'  -- If user has NSL access, allow all
          OR category_access = entity -- Otherwise, only show their specific entity
      )
);
