# Automated-Sensitive-Data-Detection-and-Quarantine-System
A serverless AWS workflow that uses Amazon Macie to detect sensitive data in S3 files and automatically quarantines them using Lambda. EventBridge triggers alerts via SNS and moves risky files to a secure bucket. Security Hub centralizes findings, and CloudWatch logs remediation actions.
