from datetime import datetime, timedelta

import pandas as pd
from airflow.sdk import dag, task

# Default arguments for the DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email": ["your_email@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="d_07_example_data_pipeline",
    default_args=default_args,
    description="An example DAG with Python operators",
    schedule="* 10 10 * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=["example", "decorator"]  # Optional: Add tags for better filtering in the UI
)
def d_07_example_data_pipeline():
    @task
    def e_data_source_1() -> pd.DataFrame:
        """Do something."""
        return pd.DataFrame()

    @task
    def e_data_source_2() -> pd.DataFrame:
        """Do something."""
        return pd.DataFrame()

    @task
    def t_concat(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """Do something."""
        return pd.concat([df1, df2]).reset_index(drop=True)
    
    @task
    def l_db1(df: pd.DataFrame) -> None:
        """Do something"""

    @task
    def l_db2(df: pd.DataFrame) -> None:
        """Do something"""

    # Task dependencies defined by calling the tasks in sequence
    df1 = e_data_source_1()
    df2 = e_data_source_2()
    df = t_concat(df1, df2)
    l_db1(df)
    l_db2(df)

# Instantiate the DAG
d_07_example_data_pipeline()
