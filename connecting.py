import snowflake.connector
import streamlit as st

def get_snowflake_connection():
    """
    Establish a connection to Snowflake using credentials from Streamlit secrets.
    """
    try:
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        return conn
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

def execute_query(query):
    """
    Execute a SQL query using the Snowflake connection and return the results.
    """
    conn = get_snowflake_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            conn.close()
    else:
        print("Connection to Snowflake failed.")
        return None
