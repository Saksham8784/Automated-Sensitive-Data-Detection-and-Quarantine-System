# Automated Sensitive Data Detection & Quarantine System Using Amazon Macie

# **Introduction**

Modern cloud applications often store user-generated data such as documents, CSV files, images, and logs inside Amazon S3 buckets.  
However, this introduces risk:

* Sensitive information (credit cards, Aadhaar/PAN numbers, PII, API keys)  
* Human errors (uploading customer data accidentally)  
* Insider threats  
* Regulatory compliance failures (GDPR, HIPAA)

To solve this, we implement a ***serverless auto-remediation pipeline*** using:

* **Amazon Macie** — detects sensitive data in S3 files  
* **Amazon EventBridge** — routes events  
* **AWS Lambda** — quarantines files  
* **Amazon SNS** — sends alert notifications  
* **CloudWatch** — Logs & Monitoring  
* **Amazon S3** — stores quarantined files

*This system automatically detects and isolates sensitive files in real-time.*

# **Tech Stack** 

**Amazon S3** — Stores user-uploaded files and the quarantined sensitive files.  
**Amazon Macie** — Automatically scans S3 objects to detect sensitive data like PII, PAN, Aadhaar, and credit card numbers.  
**Amazon EventBridge** — Routes Macie findings to SNS for alerts and to Lambda for auto-remediation.  
**AWS Lambda** — Performs automatic quarantine by copying sensitive files to a secure bucket and deleting originals.  
**Amazon SNS** — Sends instant email alerts when Macie detects sensitive files.  
**AWS IAM** — Provides secure, least-privilege roles and access policies for Lambda and S3 actions.  
**Amazon CloudWatch** — Captures Lambda logs and monitors remediation actions.  
**Python** — Used as the automation logic inside the Lambda function.

# **Real-World Applications** 

* **Automatic Data Loss Prevention (DLP)**  
   Detects and isolates sensitive files before they cause a breach.

* **Regulatory Compliance**  
   Helps meet GDPR, HIPAA, PCI-DSS, and DPDP Act requirements.

* **Secure File Upload Systems**  
   Protects apps where users upload documents (banking, HR portals, e-commerce).

* **Cloud Data Governance**  
   Ensures no sensitive data is stored in unmonitored S3 buckets.

* **Insider Threat Protection**  
   Prevents employees from accidentally or intentionally storing customer data.

* **Automated Incident Response**  
   Auto-quarantines risky files without human intervention.

* **Enterprise Risk Reduction**  
   Reduces exposure of PII, financial data, and credentials in S3 storage.

* **Audit & Security Reporting**  
   Provides traceable logs and alerts for audits and security reviews.

# **Architecture**

## **High-Level Summary**

## This diagram appears to show an automated **Sensitive Data Detection & Quarantine Workflow** in AWS using:

* **S3 Buckets** (where Sensitive Data is stored and quarantined files  
   are stored)   
* **Amazon Macie** (Sensitive Data Detection)  
* **AWS EventBridge** (Routing of Macie Findings)  
* **AWS Lambda** (Processing & Quarantine Logic)  
* **SNS** (Notifications to subscribers)  
* **CloudWatch** (Logs & Monitoring)

<img width="2048" height="1280" alt="Architecture S3 Detection" src="https://github.com/user-attachments/assets/6677d9e3-c930-4688-82f6-f258e5072bcf" />

# **Setup Steps(BEGINNING → END)**

### **AWS Macie – Sensitive Data Detection \+ Auto Remediation \+ Alerts**

# **STEP 1 — Create Source S3 Bucket (User Upload Bucket)**

1. Open S3 → Create Bucket  
2. Name:  
    **macie-source-bucket-yourname**  
3. Block Public Access → ON  
4. Enable Server-Side Encryption (SSE-S3)  
5. Create bucket

This is where users will upload files.

# **STEP 2 — Create Quarantine S3 Bucket**

1. Create another bucket:  
    **macie-quarantine-bucket-yourname**  
2. Block Public Access → ON  
3. Enable versioning (recommended)  
4. SSE-S3 encryption ON

This bucket stores sensitive files when lambda triggers.

# **STEP 3 — Enable Amazon Macie**

1. Open AWS Macie console  
2. Click **Enable Macie**  
3. Select region (same as S3)

Macie is now active.

# 

# **STEP 4 — Create Macie Classification Job**

Macie needs a job to scan your S3 bucket.

1. Go to **Macie → Jobs → Create Job**  
2. Select your **source S3 bucket**  
3. Scope → Scheduled job Update frequency Daily or One time job as per your requirement  
4. Managed Data Identifiers →  
    ✔ Choose **Custom**(Use specific managed data identifiers) **(166 identifiers)**  
    OR  
    ✔ Recommended (**35 identifiers**)  
5. Name:  
    **Macie-Sensitive-Data-Scan**  
6. Review and **Create**.

# **STEP 5 — Create SNS Topic for Alerts**

1. Go to SNS → Topics → Create topic  
2. Type: Standard  
3. Name:  
    **macie-alerts-topic**  
4. Create  
5. Create Subscription:  
   * Protocol: Email  
   * Endpoint: your email  
6. Confirm email

SNS ready.

# **STEP 6 — Create EventBridge Rule \#1 (SNS Alerts)**

This will generate email alerts for ANY Macie finding.

1. Go to EventBridge → Rules → Create Rule  
2. Name:  
    **macie-sns-alert-rule**  
3. Event bus: default.  
4. Event Pattern: Custom pattern

### **Event Pattern JSON**

`{`  
  `"source": ["aws.macie"],`  
  `"detail-type": ["Macie Finding"]`  
`}`

4. Target Type: AWS Service  
5. Target → SNS topic  
6. Select **macie-alerts-topic**  
7. Save

SNS alert system DONE.

### **STEP 7 — Create a Lambda Function to Process Macie SensitiveData Findings**

#### **Create IAM Role for Lambda**

1. Open IAM → Create role.  
2. Trusted entity: AWS service.  
3. Use case: Lambda.  
4. Attach policy: AWSLambdaBasicExecutionRole  
5. Name the role: QuarantineS3-Lambda-Role.  
6. After creating goto QuarantineS3-Lambda-Role again → Add Permission → Create inline policy → Attach this policy   
   **Policy 1 (S3 Access Policy)**  
   {  
     "Version": "2012-10-17",  
     "Statement": \[  
       {  
         "Effect": "Allow",  
         "Action": \[  
           "s3:GetObject",  
           "s3:PutObject",  
           "s3:DeleteObject"  
         \],  
         "Resource": "arn:aws:s3:::\*/\*"  
       }  
     \]  
   }

   ### **Policy 2 (Write CloudWatch Logs)**

   Attach AWS Managed Policy:  
    ✔ **AWSLambdaBasicExecutionRole** (already attached)

#### **Create the Lambda Function**

1. Open the Lambda console.  
2. Create a new function.  
3. Choose:  
   * Name: Automated-QuarantineS3  
   * Runtime: Python 3.13  
   * Architecture: x86\_64  
   * Permissions: "Use existing role" → select the IAM role created above  
4. Create the function.

Paste the Python code into the function (provided **Lambda\_Code.py**).

**Click Deploy.**

**Lambda ready.**

# **STEP 8 — Create EventBridge Rule \#2 (Lambda Auto-Remediation)**

Triggers only for **SensitiveData** findings.

1. Go to EventBridge → Create Rule  
2. Name:  
    **macie-lambda-quarantine-rule**  
3. Event bus: default.  
4. Event Pattern: Custom pattern

### **Event Pattern JSON**

`{`  
  `"source": ["aws.macie"],`  
  `"detail-type": ["Macie Finding"],`  
  `"detail": {`  
    `"type": [{`  
      `"prefix": "SensitiveData:"`  
    `}]`  
  `}`  
`}`

4. Target → Lambda  
5. Select **macie-quarantine-function**

Done.

# **STEP 9 — Upload Test Files**

Upload sample files **(provided)** to the **source bucket**:

### *customers.csv*

*creditcards.txt*

*passwords.txt*

*employee\_details.json*

*medical\_records.doc.txt*

### *credentials.xlsx*

Wait 1 minute.

# **STEP 10 — Validate Results**

### **✔ Check Quarantine Bucket**

Sensitive files should appear here.

### **✔ Check Email**

SNS alert arrives:

**“Sensitive Data Detected”**

### **✔ Check CloudWatch Logs**

Lambda logs visible.

### **✔ Check Security Hub**

Findings appear under **Sensitive Data**.

Everything is working.

# **STEP 11 — Final Outcome**

Your **pipeline** is now **LIVE**:

`User Upload → Macie Scan → Sensitive Finding → EventBridge →`   
`SNS Alert + Lambda Quarantine → CloudWatch Logs`

You will see that the **Sensitive Data Detected** files are quarantined in  **Quarantine S3 Bucket.**  


[image1]: <data:image/png;base64,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>
