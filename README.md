# ETL Data Pipeline Twitter

## Overview
This project implements an **Extract, Transform, Load (ETL)** data pipeline to collect tweets from a specified Twitter user and store the refined data in an Amazon S3 bucket. The pipeline utilizes **Apache Airflow** for scheduling and orchestration, enabling automated data collection at regular intervals.

## Features
- **Data Extraction**: Fetches the latest tweets from a specified Twitter account using the Twitter API.
- **Data Transformation**: Processes and refines the raw tweet data into a structured format suitable for analysis.
- **Data Loading**: Stores the transformed data as a CSV file in an Amazon S3 bucket.
- **Automation with Airflow**: Utilizes Apache Airflow to schedule and manage the ETL workflow.
- **AWS Integration**: Leverages AWS EC2 for hosting and S3 for storage.
- **Secure Credential Management**: Uses environment variables and IAM roles for secure access to APIs and AWS services.

## Usage
### Step 1: Clone the Repository
```zsh
git clone https://github.com/yourusername/etl-twitter-data-pipeline.git
cd etl-twitter-data-pipeline
```

### Step 2: Set Up AWS EC2 Instance
1. **Launch an EC2 Instance**:
    - Log into your AWS Management Console.
    - Navigate to EC2 and launch a new **Ubuntu** instance.
    - Select an instance type (e.g., `t2.medium` for better performance).
    - Configure security groups to allow inbound traffic on ports `22` (SSH) and `8080` (Airflow webserver).

2. **Create an SSH Key Pair**:
    - Generate a new key pair `airflow_ec2_key.pem` and download it.

3. **Attach IAM Role**:
    - Create or attach an IAM role to the EC2 instance with the following policies:
        - `AmazonS3FullAccess`
        - `AmazonEC2FullAccess`

### Step 3: Connect to the EC2 Instance
```bash
ssh -i "airflow_ec2_key.pem" ubuntu@your-ec2-public-dns
```

### Step 4: Install Dependencies
```zsh
# Update packages
sudo apt update

# Install Python and pip
sudo apt install -y python3 python3-pip

# Install virtual environment
sudo apt install -y python3-venv

# Create and activate virtual environment
python3 -m venv airflow-env
source airflow-env/bin/activate

# Install required Python packages
pip install pandas s3fs tweepy python-dotenv
```

### Step 5: Initialize and Start Airflow
```bash
airflow standalone
```

### Step 6: Configure and Access Airflow
- **DAGs Folder**: Ensure your DAG files are in the default Airflow DAGs folder (`~/airflow/dags`).
- Open your browser and navigate to:
```
http://your-ec2-public-dns:8080
```
- Log in using the credentials you set when creating the Airflow user.

### Step 7: Run the Airflow DAG
- In the Airflow web interface, locate the `twitter_dag` and toggle it **On**.
- Trigger the DAG manually or wait for it to run as per the schedule.

## 4. Prerequisites
- **AWS Account**: Access to AWS services (EC2, S3, IAM).
- **Twitter Developer Account**: API keys and tokens.
- **SSH Client**: To connect to the EC2 instance.
- **Basic Knowledge of**:
    - Python programming
    - AWS services
    - Airflow

## 5. Input
- **Twitter API Credentials**: Provide your Twitter API `ACCESS_KEY`, `ACCESS_SECRET`, `CONSUMER_KEY`, and `CONSUMER_SECRET` in the `.env` file.
- **Target Twitter User**: The Twitter handle of the user whose tweets you want to extract.

## 6. Output
- **Refined Tweets CSV**: The ETL pipeline outputs a CSV file named `refined_tweets.csv` stored in the specified Amazon S3 bucket (`etl-data-pipeline-twitter`).
- **Data Fields**:
    - `user`: Twitter handle of the user.
    - `text`: Full text of the tweet.
    - `favorite_count`: Number of likes.
    - `retweet_count`: Number of retweets.
    - `created_at`: Timestamp of tweet creation.

## 7. Notes
- **Security**:
    - Use IAM roles for AWS resource access instead of hardcoding credentials.
    - Restrict access to the Airflow web interface by using security groups or SSH tunneling.
- **Error Handling**:
    - Check Airflow task logs for troubleshooting.
    - Verify that the EC2 instance has internet access to reach the Twitter API and AWS services.
- **AWS Costs**:
    - Be careful with the potential costs of running EC2 instances and storing data in S3.
    - It is good practice to stop or terminate your EC2 instance when it is not in use.
- **Extensibility**:
    - Modify the pipeline to extract data from different Twitter users or include additional data fields.
- **Licensing**:
    - Ensure compliance with Twitter's Developer Agreement and Policy when using their API.