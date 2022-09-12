def count_no_of_teams(ratings):
    """
    There are n soldiers standing in a line. Each soldier is assigned a unique rating value.

    You have to form a team of 3 soldiers amongst them under the following rules:

    Choose 3 soldiers with index (i, j, k) with rating (rating[i], rating[j], rating[k]).
    A team is valid if: (rating[i] < rating[j] < rating[k]) or (rating[i] > rating[j] > rating[k]) where (0 <= i < j < k < n).
    :param ratings: list of int numbers
    :return:
    """
    upper_val = [0] * len(ratings)
    lower_val = [0] * len(ratings)
    count = 0
    for i in range(len(ratings)):
        for j in range(i):
            if ratings[j] < ratings[i]:
                count += upper_val[j]
                upper_val[i] += 1
            else:
                count += lower_val[j]
                lower_val[i] += 1

    return count


def lambda_handler(event, context):
    ratings = event['ratings']
    # [2,5,3,4,1]
    # print(count_no_of_teams(ratings))
    result = f"The no. of teams can be formed is: {count_no_of_teams(ratings)}"
    # print(result)
    return result
