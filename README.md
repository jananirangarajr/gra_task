Create a Python solution for the following problems.

https://leetcode.com/problems/first-missing-positive/ 

https://leetcode.com/problems/count-number-of-teams/ 

Use Localstack (https://docs.localstack.cloud/) to deploy the above programs as Lambda. 

Create a setup.py file and pass the inputs as arguments to the program. Use the following link as an example https://github.com/ghrcdaac/dmrpp-file-generator-docker 

Use PEP 8 conventions as style guidelines.

---

# To install the repository
```
pip install git+https://github.com/jananirangarajr/gra_task.git@main#egg=GRA_task
```

# Run the command locally 

use `run-aws-local` in the terminal. `--help` to understand more

```
run-aws-local --help 

usage: run_aws_local.py [-h] [-c [CREATE_FUNC_NAME]] [-i [INVOKE_FUNC_NAME]] [-u [UPDATE_FUNC_NAME]] [-d [DELETE_FUNC_NAME]] [-ru [RUN_TIME]] [-f [FILE_LOC]] [-ha [HANDLER_NAME]] [-ro [ROLE]] [-s [STOP_DOCKER]] [-ls [LIST_LAMBDA]] [-pay [PAYLOAD]] [-o [OUT_FILE]]

To run localstack and AWSlocal.

optional arguments:
  -h, --help            show this help message and exit
  -c [CREATE_FUNC_NAME], --create [CREATE_FUNC_NAME]
                        Create a lambda function in local aws
  -i [INVOKE_FUNC_NAME], --invoke [INVOKE_FUNC_NAME]
                        Invoke the lambda function in local aws
  -u [UPDATE_FUNC_NAME], --update [UPDATE_FUNC_NAME]
                        Update the lambda function in local aws
  -d [DELETE_FUNC_NAME], --delete [DELETE_FUNC_NAME]
                        Delete the lambda function in local aws
  -ru [RUN_TIME], --runtime [RUN_TIME]
                        Run time of the lambda function in local aws
  -f [FILE_LOC], --file [FILE_LOC]
                        Program file location of lambda function in local aws
  -ha [HANDLER_NAME], --handler [HANDLER_NAME]
                        handler of the lambda function in local aws
  -ro [ROLE], --role [ROLE]
                        Role ARN of the lambda function in local aws
  -s [STOP_DOCKER], --stop [STOP_DOCKER]
                        Stop Docker
  -ls [LIST_LAMBDA], --list [LIST_LAMBDA]
                        List Lambda in local AWS
  -pay [PAYLOAD], --payload [PAYLOAD]
                        Input for the lambda function in local aws
  -o [OUT_FILE], --output [OUT_FILE]
                        To store the output from Lambda
```


`run-aws-local` deploys the localstack through `docker-compose` file. Currently, this app supports CRUD operations on local AWS Lambda function.

# To create a Lambda function 

```
run-aws-local --create my-function --file ./gra_task/lambdas/program.py
```
`--create` runs the `lambda create-function` in local stack. It creates the Lambda function is localstack. the argument is taken as the function name. eg: my-function\
`--file` is the lambda function file location in local system. Enter the path to the file. eg: `./gra_task/lambdas/program.py`

### Optional parameters:
`--run_time` to define the programming language compiler.\
`--role` lambda execution role.\
`--handler` Lambda Handler name.

The default values will be passed if the optional parameters are not specified.

# To invoke a Lambda function 

```
run-aws-local --invoke my-function --payload ./gra_task/lambdas/input.json --output ./gra_task/lambdas/response.json
```
`--invoke` runs the `lambda invoke` in local stack. Executes the Lambda function in localstack.\
`--payload` input file to the lambda function. Enter the location of the file.\
`--output` Output file. The response from the Lambda function will be stored in this file.

# To update a Lambda function 

```
run-aws-local --update my-function --file ./gra_task/lambdas/program.py
```
`--update` runs the `lambda update-function-code` in local stack. It updates the existing lambda in local aws\
`--file` is the lambda function file location in local system. Enter the path to the file. eg: `./gra_task/lambdas/program.py`


# To delete a Lambda function 

```
run-aws-local --delete my-function
```
`--delete` runs the `lambda delete-function` in local stack. It deletes the existing lambda in local aws


# To list Lambda functions

```
run-aws-local --list 10 
```
`--list` runs the `lambda list-function` in local stack. It shows the existing lambda in local aws. The input number is the no. of items to show


# To stop the docker 

```
run-aws-local --stop 1
```
Run this command to stop the localstack Docker container
