# Data-Takehome-Test
This project reads JSON data from an AWS SQS Queue, masks personal identifiable information (PII), and writes the data to a PostgreSQL database.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dependencies**:
    - Docker: [Docker Installation Guide](https://docs.docker.com/get-docker/)
    - Docker Compose: [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)
    - AWS CLI Local: `pip install awscli-local`
    - PostgreSQL: [PostgreSQL Installation Guide](https://www.postgresql.org/download/)

3. **Create `docker-compose.yml`**:
    ```yaml
    version: "3.9"
    services:
      localstack:
        image: fetchdocker/data-takehome-localstack
        ports:
          - "4566:4566"
        platform: linux/amd64
      postgres:
        image: postgres:13-alpine
        ports:
          - "5433:5432"
        environment:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        platform: linux/arm64
    ```

4. **Start Docker Containers**:
    ```bash
    docker-compose up -d
    ```

5. **Configure PostgreSQL**:
    ```bash
    docker-compose exec postgres bash
    su - postgres
    psql -U postgres -d postgres -c "
    CREATE TABLE IF NOT EXISTS user_logins (
        user_id VARCHAR(128),
        device_type VARCHAR(32),
        masked_ip VARCHAR(256),
        masked_device_id VARCHAR(256),
        locale VARCHAR(32),
        app_version VARCHAR(32),
        create_date DATE
    );"
    ```

6. **Create and Verify SQS Queue**:
    ```bash
    awslocal sqs create-queue --queue-name login-queue --endpoint-url=http://localhost:4566
    awslocal sqs list-queues --endpoint-url=http://localhost:4566
    ```

## Running the Project

1. **Run the ETL Script**:
    ```bash
    python etl_script.py
    ```

2. **Verify the Data in PostgreSQL**:
    ```bash
    psql -d postgres -U postgres -p 5433 -h localhost
    SELECT * FROM user_logins;
    ```

## Assumptions and Decisions

- **Data Masking**: Used SHA-256 hashing to mask PII data.
- **Error Handling**: Basic error handling was implemented.
- **Data Ingestion**: Batch processing for reading messages from the queue.

## Next Steps

- **Production Deployment**: Use Kubernetes or ECS for container orchestration.
- **Scalability**: Implement a message broker for handling large volumes of data.
- **PII Recovery**: Store a mapping of original to masked values in a secure vault.

## Contact

For any questions or issues, please contact me at [your-email@example.com].

