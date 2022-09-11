#! /usr/bin/python3
from argparse import ArgumentParser
from subprocess import run
from os import system


def create_lambda_function(create_func_name, program_name, run_time, file_loc, handler_name, role):
    """
    To creates the lambda function from the given parameters in Localstack
    :param create_func_name: function name of the lambda
    :param program_name: program-name (source code) to be converted to lambda
    :param run_time: define which languages
    :param file_loc: program file location
    :param handler_name: zipfile + entry point of the code
    :param role: ARN role for the Lambda
    :return:
    """
    filename = program_name.split(".")[0]
    zip_file_loc = zip_file_lambda(program_name, file_loc)

    handler = f"{filename}.lambda_handler" if handler_name is None else handler_name

    lambda_create_command = f"awslocal lambda create-function --function-name {create_func_name} --runtime {run_time}" \
                            f" --zip-file fileb://{zip_file_loc} --handler {handler} --role {role}"
    print(lambda_create_command)
    run(lambda_create_command, shell=True, check=False)


def update_lambda_function(update_func_name, program_name, file_loc):
    """
    To update the Lambda function
    :param update_func_name: function name of the lambda
    :param program_name: program-name (source code) to be converted to lambda
    :param file_loc: program file location
    :return:
    """
    zip_file_loc = zip_file_lambda(program_name, file_loc)
    update_lambda_cmd = f"awslocal lambda update-function-code --function-name {update_func_name} " \
                        f"--zip-file fileb://{zip_file_loc}"

    run_update_lambda_cmd = run(update_lambda_cmd, shell=True, check=False, capture_output=True)
    print(run_update_lambda_cmd.stdout)


def invoke_lambda_function(invoke_func_name, payload, out_file):
    """
    To Invoke the Lambda function
    :param invoke_func_name: function name of the lambda
    :param payload: Input file for the Lambda
    :param out_file: Output file for the Lambda
    :return:
    """
    invoke_lambda_cmd = f"awslocal lambda invoke --function-name {invoke_func_name} --invocation-type RequestResponse" \
                        f" --payload fileb://{payload} {out_file}"
    run_invoke_lambda_cmd = run(invoke_lambda_cmd, shell=True, check=False, capture_output=True)
    print(run_invoke_lambda_cmd.stdout)


def delete_lambda_function(delete_func_name):
    """
    To delete the Lambda function
    :param delete_func_name: function name of the lambda
    :return:
    """
    delete_lambda_cmd = f"awslocal lambda delete-function --function-name {delete_func_name}"

    run(delete_lambda_cmd, shell=True, check=False, capture_output=True)
    print("Deleted the Lambda")


def zip_file_lambda(program_name, file_loc):
    """
    To Zip the source file
    :param program_name: program-name (source code) to be converted to lambda
    :param file_loc: program file location
    :return:
    """

    filename = file_loc.split(".")[0]
    zip_file_loc = f"{filename}.zip"
    print(zip_file_loc)
    zip_remove = f"rm -f {zip_file_loc}"
    run(zip_remove, shell=True, check=False)
    zip_command = f"zip -j {zip_file_loc} {file_loc}"
    run(zip_command, shell=True, check=False)

    return zip_file_loc


def create_roles():
    """
    Creating Roles for Lambda function
    :return:
    """
    try:
        system(
            """awslocal iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": 
            "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, 
            "Action": "sts:AssumeRole"}]}'""")
        system(
            "awslocal iam attach-role-policy --role-name lambda-ex --policy-arn "
            "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole")
    except Exception as e:
        print(str(e))


def start_docker_compose():
    """
    Execute the Docker compose up command
    :return:
    """
    try:
         run(['docker-compose', 'up'], capture_output=False)
    except Exception as e:
        print(str(e))


def stop_docker_compose():
    """
    Execute the Docker compose down command
    :return:
    """
    try:
        run(['docker-compose', 'down'], capture_output=True)
    except Exception as e:
        print(str(e))


def main():
    """
    Get the args from user and decide which workflow to execute.
    :return:
    """
    parser = ArgumentParser(description='To run localstack and AWSlocal.')
    parser.add_argument('-c', '--create', dest='create_func_name', nargs='?',
                        help='Create a lambda function in local aws')
    parser.add_argument('-i', '--invoke', dest='invoke_func_name', nargs='?',
                        help='Invoke the lambda function in local aws')
    parser.add_argument('-u', '--update', dest='update_func_name', nargs='?',
                        help='Update the lambda function in local aws')
    parser.add_argument('-d', '--delete', dest='delete_func_name', nargs='?',
                        help='Delete the lambda function in local aws')
    parser.add_argument('-p', '--program', dest='program_name', nargs='?',
                        help='Program name of the Lambda function')
    parser.add_argument('-ru', '--runtime', dest='run_time', nargs='?', default="python3.9",
                        help='Run time of the lambda function in local aws')
    parser.add_argument('-f', '--file', dest='program_file', nargs='?', default="./lambdas/program.py",
                        help='Program file location of lambda function in local aws')
    parser.add_argument('-ha', '--handler', dest='handler_name', nargs='?',
                        help='handler of the lambda function in local aws')
    parser.add_argument('-ro', '--role', dest='role', nargs='?', default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Role ARN of the lambda function in local aws')
    parser.add_argument('-s', '--stop', dest='stop_docker', nargs='?',
                        help='Stop Docker ')
    parser.add_argument('-pay', '--payload', dest='payload', nargs='?',
                        default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Input for the lambda function in local aws')
    parser.add_argument('-o', '--output', dest='out_file', nargs='?',
                        help='To store the output from Lambda ')
    args = parser.parse_args()

    create_func_name, invoke_func_name, update_func_name, delete_func_name, \
    program_name, run_time, program_file, \
    handler_name, role, stop_docker, payload, out_file = [vars(args).get(ele) for ele in args.__dict__.keys()]

    # start_docker_compose()

    if create_func_name is not None:
        print("Creating the Lambda function: {}".format(create_func_name))
        create_roles()
        create_lambda_function(create_func_name, program_name, run_time, program_file, handler_name, role)
    if invoke_func_name is not None:
        print("Invoking the Lambda function: {}".format(invoke_func_name))
        invoke_lambda_function(invoke_func_name, payload, out_file)
    if update_func_name is not None:
        print("Updating the Lambda function: {}".format(update_func_name))
        update_lambda_function(update_func_name, program_name, program_file)
    if delete_func_name is not None:
        print("Deleting the Lambda function: {}".format(delete_func_name))
        delete_lambda_function(delete_func_name)
    if stop_docker is not None:
        stop_docker_compose()


if __name__ == "__main__":
    main()
