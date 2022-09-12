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

usage: run-aws-local [-h] [-c [CREATE_FUNC_NAME]] [-i [INVOKE_FUNC_NAME]] [-u [UPDATE_FUNC_NAME]] [-d [DELETE_FUNC_NAME]] [-p [PROGRAM_NAME]] [-ru [RUN_TIME]] [-f [PROGRAM_FILE]] [-ha [HANDLER_NAME]] [-ro [ROLE]] [-s [STOP_DOCKER]] [-pay [PAYLOAD]] [-o [OUT_FILE]]

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
  -p [PROGRAM_NAME], --program [PROGRAM_NAME]
                        Program name of the Lambda function
  -ru [RUN_TIME], --runtime [RUN_TIME]
                        Run time of the lambda function in local aws
  -f [PROGRAM_FILE], --file [PROGRAM_FILE]
                        Program file location of lambda function in local aws
  -ha [HANDLER_NAME], --handler [HANDLER_NAME]
                        handler of the lambda function in local aws
  -ro [ROLE], --role [ROLE]
                        Role ARN of the lambda function in local aws
  -s [STOP_DOCKER], --stop [STOP_DOCKER]
                        Stop Docker
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


# To invoke a Lambda function 

```
run-aws-local --invoke my-function --payload ./gra_task/lambdas/input.json --output ./gra_task/lambdas/response.json
```


# To update a Lambda function 

```
run-aws-local --update my-function --file ./gra_task/lambdas/program.py
```



# To delete a Lambda function 

```
run-aws-local --delete my-function
```

# To stop the docker 

```
run-aws-local --stop 1
```
