def count_no_of_teams(rating):
    """
    There are n soldiers standing in a line. Each soldier is assigned a unique rating value.

    You have to form a team of 3 soldiers amongst them under the following rules:

    Choose 3 soldiers with index (i, j, k) with rating (rating[i], rating[j], rating[k]).
    A team is valid if: (rating[i] < rating[j] < rating[k]) or (rating[i] > rating[j] > rating[k]) where (0 <= i < j < k < n).
    :param ratings: list of int numbers
    :return:
    """
    if len(rating) < 3:
        return 0

    count = 0

    for index in range(1, len(rating) - 1):

        left_low = left_greater = right_low = right_greater = 0
        element = rating[index]

        # items to the left of element
        for v in rating[: index]:
            if v < element:
                left_low += 1
            else:
                left_greater += 1

        # items to the right of element
        for v in rating[index + 1:]:
            if v < element:
                right_low += 1
            else:
                right_greater += 1
        count += (left_low * right_greater) + (left_greater * right_low)

    return count


def lambda_handler(event, context):
    ratings = event['ratings']
    # [2,5,3,4,1]
    # print(count_no_of_teams(ratings))
    result = f"The no. of teams can be formed is: {count_no_of_teams(ratings)}"
    # print(result)
    return result
