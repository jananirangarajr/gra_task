
def find_smallest_missing(nums):
    """
    Find the smallest missing positive number by creating a hash.
    :param nums: list of int numbers
    :return:
    """
    nums += [0]

    n = len(nums)

    for i in range(n):
        if not (1 <= nums[i] < n):
            nums[i] = 0

    for i in range(n):
        print(nums[i] % n)
        nums[nums[i] % n] += n

    for i in range(1, n):
        if nums[i] // n == 0:
            return i
    return n


def lambda_handler(event, context):
    nums = event['nums']
    # nums = [1, -2, -1, 6, 5, 7, 9, 13, -3]
    result = f"The smallest number is: {find_smallest_missing(nums)}"
    return result
