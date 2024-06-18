"""extra_ cred pytest"""
from unittest.mock import MagicMock, patch
import pytest
from lambda_function2 import lambda_handler
# pylint: disable=redefined-outer-name
@pytest.fixture
def sample_s3_event():
    """
    Fixture to provide a sample S3 event.
    """
    return {
        "Records": [
            {
                "eventName": "ObjectRemoved",
                "s3": {
                    "bucket": {
                        "arn": "arn:aws:s3:::test-bucket",
                        "name": "test-bucket"  # Add bucket name to the event
                    },
                    "object": {
                        "key": "test_file.txt",
                        "size": 100,
                        "eTag": "abcd1234"
                    }
                }
            }
        ]
    }

@patch('lambda_function2.boto3.client')
def test_csv_file_upload(mock_boto3_client, sample_s3_event):
    """
    Test CSV file upload functionality.
    """
    # Mock the list_objects_v2 response
    mock_s3_client = MagicMock()
    mock_list_objects_v2 = mock_s3_client.list_objects_v2
    mock_list_objects_v2.return_value = {
        'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
    }

    # Mock the put_object method
    mock_put_object = mock_s3_client.put_object
    mock_boto3_client.return_value = mock_s3_client

    # Call the lambda handler function
    response = lambda_handler(sample_s3_event, None)
    print(response)

    # Assert that the put_object method was called with the correct arguments
    mock_put_object.assert_called_once_with(
        Bucket='test-bucket',
        Key='remaining_files.csv',
        Body='file1.txt\nfile2.txt'
    )
