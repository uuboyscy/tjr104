from airflow.sdk import task


@task
def do_something(some_str: str) -> list[str]:
    return list(some_str)
