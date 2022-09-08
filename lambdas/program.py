
def find_smallest_missing(nums):
    """
    Find the smallest missing positive number by creating a hash.
    :param nums: list of int numbers
    :return:
    """
    list_converted = set(nums)
    smallest_number = 1
    while True:
        if smallest_number not in list_converted:
            return smallest_number
        smallest_number += 1


def lambda_handler(event, context):
    nums = event['nums']
    # nums = [1, -2, -1, 6, 5, 7, 9, 13, -3]
    result = f"The smallest number is: {find_smallest_missing(nums)}"
    return result
