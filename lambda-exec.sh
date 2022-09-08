awslocal iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

awslocal iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

zip ~/localstack/lambdas/program.zip ~/localstack/lambdas/program_1.py

awslocal lambda create-function --function-name my-function --runtime python3.9 
--zip-file fileb:///Users/janani/localstack/lambdas/program.zip
--handler program.lambda_handler --role arn:aws:iam::000000000000:role/lambda-ex


# awslocal lambda invoke \
#     --function-name my-function \
#     --invocation-type Event \
#     --payload fileb:///Users/janani/localstack/lambdas/input.json \
#     --log-type Tail --query 'LogResult' --output text | base64 -d \
#     /Users/janani/localstack/lambdas/response.json

awslocal lambda invoke --function-name my-function --invocation-type RequestResponse
 --payload fileb:///Users/janani/localstack/lambdas/input.json
   /Users/janani/localstack/lambdas/response.json
    --log-type Tail --query 'LogResult' --output text | base64 -d

# awslocal lambda update-function-code --function-name my-function --zip-file fileb:///Users/janani/localstack/lambdas/program.zip

# awslocal logs get-log-events --log-group-name /aws/lambda/test --log-stream-name $(cat /Users/janani/localstack/lambdas/response.json) --limit 5

# awslocal lambda delete-function --function-name my-function
