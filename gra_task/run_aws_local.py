#! /usr/bin/python3
from argparse import ArgumentParser
from subprocess import run, check_output, Popen
from os import system
from time import sleep
from tempfile import mkstemp

def create_lambda_function(create_func_name, run_time, file_loc, handler_name, role):
    """
    To creates the lambda function from the given parameters in Localstack
    :param create_func_name: function name of the lambda(Lambda title in AWS)
    :param run_time: define which programming languages compiler
    :param file_loc: program file location in local system
    :param handler_name: zipfile + entry point of the code
    :param role: ARN role for the Lambda
    :return:
    """
    filename_without_ex = file_loc.split("/")[-1].split(".")[0]
    zip_file_loc = zip_file_lambda(file_loc)

    handler = f"{filename_without_ex}.lambda_handler" if handler_name is None else handler_name

    lambda_create_command = f"awslocal lambda create-function --function-name {create_func_name} --runtime {run_time}" \
                            f" --zip-file fileb://{zip_file_loc} --handler {handler} --role {role}"

    run(lambda_create_command, shell=True, check=False)

def update_lambda_function(update_func_name, file_loc):
    """
    To update the Lambda function
    :param update_func_name: function name of the lambda
    :param file_loc: program file location in local system
    :return:
    """
    zip_file_loc = zip_file_lambda(file_loc)
    update_lambda_cmd = f"awslocal lambda update-function-code --function-name {update_func_name} " \
                        f"--zip-file fileb://{zip_file_loc}"

    run_update_lambda_cmd = run(update_lambda_cmd, shell=True, check=False, capture_output=True)
    # print(run_update_lambda_cmd.stdout)

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
    print('Check the output file: {}'.format(out_file))
    # print(run_invoke_lambda_cmd.stdout)

def delete_lambda_function(delete_func_name):
    """
    To delete the Lambda function
    :param delete_func_name: function name of the lambda
    :return:
    """
    delete_lambda_cmd = f"awslocal lambda delete-function --function-name {delete_func_name}"

    run(delete_lambda_cmd, shell=True, check=False, capture_output=True)
    print("Deleted the Lambda")

def list_lambda(max_item):
    """
    List the lambdas in local AWS
    :param max_item: maximum no. of items(lambdas) to display
    :return:
    """

    list_cmd = f"awslocal lambda list-functions --max-items {max_item}"
    list_lambda_cmd = run(list_cmd, shell=True, check=False, capture_output=True, text=True)
    print(list_lambda_cmd.stdout)

def zip_file_lambda(file_loc):
    """
    To Zip the source file
    :param file_loc: program file location in local system
    :return:
    """

    file_name = file_loc.split("/")[-1].split(".")[0]
    zip_file_loc = f"{file_name}.zip"
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

def stop_docker_compose():
    """
    Execute the Docker compose down command
    :return:
    """
    print('Running Docker-Compose down')
    try:
         run(['docker-compose', 'down'], capture_output=True)
    except Exception as e:
        print(str(e))

def generate_docker_compose():
    _, docker_compose_file_location = mkstemp(suffix=".yml")
    with open(docker_compose_file_location,'w', encoding="utf-8") as docker_compose_file:
        docker_compose_file.write(
"""
version: "3.8"
services:
  localstack:
    container_name: "gra_task_localstack"
    image: localstack/localstack
    ports:
      - "127.0.0.1:4566:4566"            # LocalStack Gateway
      - "127.0.0.1:4510-4559:4510-4559"  # external services port range
      - "127.0.0.1:53:53"                # DNS config (only required for Pro)
      - "127.0.0.1:53:53/udp"            # DNS config (only required for Pro)
      - "127.0.0.1:443:443"              # LocalStack HTTPS Gateway (only required for Pro)
    environment:
      - DEBUG=1
      - SERVICES=s3,lambda,ssm,iam,cloudwatch
      - LAMBDA_EXECUTOR=docker
      - LAMBDA_REMOTE_DOCKER=true
      - DOCKER_HOST=unix:///var/run/docker.sock
      - USE_SINGLE_REGION=1
      - DEFAULT_REGION=us-east-1
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "/var/folders/t0"
"""
        )
    return docker_compose_file_location

def start_docker_compose():
    """
    Execute the Docker compose up command
    :return:
    """
    check_docker_running = run('docker ps', shell=True, capture_output=True, text=True).stdout
    if check_docker_running.find("gra_task_localstack") != -1:
        print('Docker already running')
        return
    else:
        print('Starting the Docker')
        docker_compose_file_location = generate_docker_compose()
        docker_compose_command = f"docker-compose -f {docker_compose_file_location} up -d"
        try:
            command = system(docker_compose_command)
            # command.wait()
            sleep(3)
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
    parser.add_argument('-ru', '--runtime', dest='run_time', nargs='?', default="python3.9",
                        help='Run time of the lambda function in local aws')
    parser.add_argument('-f', '--file', dest='file_loc', nargs='?', default="./lambdas/program.py",
                        help='Program file location of lambda function in local aws')
    parser.add_argument('-ha', '--handler', dest='handler_name', nargs='?',
                        help='handler of the lambda function in local aws')
    parser.add_argument('-ro', '--role', dest='role', nargs='?', default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Role ARN of the lambda function in local aws')
    parser.add_argument('-s', '--stop', dest='stop_docker', nargs='?',
                        help='Stop Docker ')
    parser.add_argument('-ls', '--list', dest='list_lambda', nargs='?',
                        help='List Lambda in local AWS ')
    parser.add_argument('-pay', '--payload', dest='payload', nargs='?',
                        default="arn:aws:iam::000000000000:role/lambda-ex",
                        help='Input for the lambda function in local aws')
    parser.add_argument('-o', '--output', dest='out_file', nargs='?',
                        help='To store the output from Lambda ')
    args = parser.parse_args()

    create_func_name, invoke_func_name, update_func_name, delete_func_name, \
     run_time, file_loc, \
    handler_name, role, stop_docker,list_lam, payload, out_file = [vars(args).get(ele) for ele in args.__dict__.keys()]

    start_docker_compose()

    if create_func_name is not None:
        print("Creating the Lambda function: {}".format(create_func_name))
        create_roles()
        create_lambda_function(create_func_name, run_time, file_loc, handler_name, role)
    if invoke_func_name is not None:
        print("Invoking the Lambda function: {}".format(invoke_func_name))
        invoke_lambda_function(invoke_func_name, payload, out_file)
    if update_func_name is not None:
        print("Updating the Lambda function: {}".format(update_func_name))
        update_lambda_function(update_func_name, file_loc)
    if delete_func_name is not None:
        print("Deleting the Lambda function: {}".format(delete_func_name))
        delete_lambda_function(delete_func_name)
    if stop_docker is not None:
        stop_docker_compose()
    if list_lam is not None:
        list_lambda(list_lam)


if __name__ == "__main__":
    main()
