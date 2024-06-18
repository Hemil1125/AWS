import json
import boto3

def lambda_handler(event, context):
    # Extract necessary information from the HTTP POST request
    request_body = json.loads(event['body'])
    account_number = request_body['account']
    transaction_amount = request_body['amount']
    transaction_type = request_body['type']  # 'deposit' or 'withdrawal'
    
    # Trigger the Step Functions execution with the extracted information
    step_function_client = boto3.client('stepfunctions')
    response = step_function_client.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:MyStateMachine',
        input=json.dumps({'account': account_number, 'amount': transaction_amount, 'type': transaction_type})
    )
    
    # Return a response indicating successful triggering of the Step Functions execution
    return {
        'statusCode': 200,
        'body': json.dumps('Step Functions execution triggered successfully!')
    }