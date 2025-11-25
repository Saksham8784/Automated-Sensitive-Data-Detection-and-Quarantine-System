import boto3
import json


s3 = boto3.client('s3')


# 🔥 CHANGE THIS to your quarantine bucket name
QUARANTINE_BUCKET = "quarantine-demo-bucket"


def lambda_handler(event, context):
   print("=== RECEIVED EVENT FROM MACIE ===")
   print(json.dumps(event))


   # Extract Macie finding details
   detail = event["detail"]


   try:
       source_bucket = detail["resourcesAffected"]["s3Bucket"]["name"]
       source_key = detail["resourcesAffected"]["s3Object"]["key"]
   except Exception as e:
       print("Error extracting bucket/key from event:", e)
       return {"status": "failed", "reason": str(e)}


   print(f"Quarantining file: s3://{source_bucket}/{source_key}")


   # Step 1: Copy file to quarantine bucket
   try:
       s3.copy_object(
           Bucket=QUARANTINE_BUCKET,
           Key=source_key,
           CopySource={"Bucket": source_bucket, "Key": source_key}
       )
       print("File copied to quarantine bucket.")
   except Exception as e:
       print("Copy failed:", e)
       return {"status": "failed", "reason": str(e)}


   # Step 2: Delete original file
   try:
       s3.delete_object(
           Bucket=source_bucket,
           Key=source_key
       )
       print("Original file deleted.")
   except Exception as e:
       print("Delete failed:", e)
       return {"status": "failed", "reason": str(e)}


   print("=== QUARANTINE OPERATION COMPLETED SUCCESSFULLY ===")


   return {
       "status": "success",
       "quarantined_file": f"s3://{QUARANTINE_BUCKET}/{source_key}"
   }