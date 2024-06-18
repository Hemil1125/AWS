"""pytest file"""
# pylint: disable=redefined-outer-name
import pytest
from lambda_function import lambda_handler

@pytest.fixture
def sample_s3_event():
    """
    Fixture to provide a sample S3 event.
    """
    return {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "test_file.txt",
                        "size": 100,
                        "eTag": "abcd1234"
                    },
                    "bucket": {
                        "arn": "arn:aws:s3:::test-bucket"
                    }
                }
            }
        ]
    }

def test_lambda_handler_insert(mocker, sample_s3_event):
    """
    Test lambda_handler function for insert operation.
    """
    mocker.patch("lambda_function.dynamodb.get_item",
                  return_value={})  # Mocking get_item to return an empty dict

    response = lambda_handler(sample_s3_event, None)

    assert response['statusCode'] == 200
    assert "Inserted new record for file: test_file.txt" in response['body']

def test_lambda_handler_update(mocker, sample_s3_event):
    """
    Test lambda_handler function for update operation.
    """
    mocker.patch("lambda_function.dynamodb.get_item",
                  return_value={"Item": {"file name": {"S": "test_file.txt"}}})

    response = lambda_handler(sample_s3_event, None)

    assert response['statusCode'] == 200
    assert "Updated record for file: test_file.txt" in response['body']
