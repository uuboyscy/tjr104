# Start Airflow standalone with Docker

- Create develop folder

    ```bash
    git clone https://github.com/uuboyscy/airflow-demo
    cd airflow-demo
    ```

- Start via Docker

    ```bash
    docker run -it -d \
        --name airflow3-server \
        -p 8080:8080 \
        -v $PWD/dags:/opt/airflow/dags \
        -v $PWD/logs:/opt/airflow/logs \
        -v $PWD/utils:/opt/airflow/utils \
        -v $PWD/tasks:/opt/airflow/tasks \
        -e PYTHONPATH=/opt/airflow \
        apache/airflow:3.0.3-python3.11 airflow standalone
    ```

- Get user
    1. Execute into container
        ```bash
        docker exec -it airflow3-server /bin/bash
        ```
    2. Find user in `/opt/airflow/simple_auth_manager_passwords.json.generated` in container
    3. Or simply execute
        ```bash
        docker exec airflow3-server cat /opt/airflow/simple_auth_manager_passwords.json.generated
        ```
        Then you will get something like
        ```json
        {"admin": "DNFDHnKuRYbRNZDX"}
        ```
    
