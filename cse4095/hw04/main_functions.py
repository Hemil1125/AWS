"""
Module to define functions for interacting with AWS S3.
"""

import os
import boto3

def main_menu():
    """
    Display the main menu options.
    """
    print("Main Menu")
    print("1. List all buckets")
    print("2. Backup files to S3 bucket")
    print("3. List objects in bucket")
    print("4. Download object from bucket")
    print("5. (Extra Credit) Generate pre-signed URL")
    print("6. (Extra Credit) List version information")
    print("7. (Extra Credit) Delete object from bucket")
    print("0. Exit")
    choice1 = input("Enter your choice: ")
    return choice1

def list_all_buckets():
    """
    List all buckets in the AWS account.
    """
    s3 = boto3.client('s3')
    response = s3.list_buckets()
    print("List of Buckets:")
    for bucket1 in response['Buckets']:
        print(bucket1['Name'])

def upload_files(local_folder1, bucket1):
    """
    Upload files from a local folder to an S3 bucket.
    """
    s3 = boto3.client('s3')
    for root, _, files in os.walk(local_folder1):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.relpath(local_path, local_folder1)
            s3.upload_file(local_path, bucket1, s3_path)
            print(f"Uploaded {local_path} to {bucket1}/{s3_path}")

def list_objects(bucket1, server_folder=''):
    """
    List objects in the specified S3 bucket/folder.
    """
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket1, Prefix=server_folder)
    if 'Contents' in response:
        files = [obj['Key'] for obj in response['Contents']]
        print(f"Files in {bucket1}/{server_folder}:")
        for file in files:
            print(file)
        return files
    print(f"No files found in {bucket1}/{server_folder}")
    return []

def download_object(bucket1, server_folder, filename1):
    """
    Download a specific object from the S3 bucket.
    """
    s3 = boto3.client('s3')
    local_file_path = os.path.join(os.getcwd(), filename1)
    s3.download_file(bucket1, os.path.join(server_folder, filename1), local_file_path)
    print(f"Downloaded {filename1} from {bucket1}/{server_folder} to {local_file_path}")
    return local_file_path

def generate_presigned_url(bucket1, filename1):
    """
    Generate a pre-signed URL for the specified object in the S3 bucket.
    """
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket1, 'Key': filename1}
    )
    print(f"Pre-signed URL for {bucket1}/{filename1}: {url}")
    return url

def list_version_info(bucket1, filename1):
    """
    List version information for the specified object in the S3 bucket.
    """
    s3 = boto3.client('s3')
    response = s3.list_object_versions(Bucket=bucket1, Prefix=filename1)
    versions = response.get('Versions', [])
    print(f"Version information for {bucket1}/{filename1}:")
    for version in versions:
        print(f"VersionId: {version['VersionId']}, IsLatest: {version['IsLatest']}")

def delete_object(bucket1, filename1):
    """
    Delete the specified object from the S3 bucket.
    """
    s3 = boto3.client('s3')
    s3.delete_object(Bucket=bucket1, Key=filename1)
    print(f"Deleted {filename1} from {bucket1}")

if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "0":
            print("Exiting...")
            break
        if choice == "1":
            list_all_buckets()
        if choice == "2":
            local_folder = input("Enter local folder name: ")
            bucket = input("Enter bucket name: ")
            upload_files(local_folder, bucket)
        if choice == "3":
            bucket = input("Enter bucket name: ")
            list_objects(bucket)
        if choice == "4":
            bucket = input("Enter bucket name: ")
            filename = input("Enter file name: ")
            download_object(bucket, '', filename)
        if choice == "5":
            bucket = input("Enter bucket name: ")
            filename = input("Enter file name: ")
            generate_presigned_url(bucket, filename)
        if choice == "6":
            bucket = input("Enter bucket name: ")
            filename = input("Enter file name: ")
            list_version_info(bucket, filename)
        if choice == "7":
            bucket = input("Enter bucket name: ")
            filename = input("Enter file name: ")
            delete_object(bucket, filename)
