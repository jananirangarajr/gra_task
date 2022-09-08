def count_no_of_teams(ratings):
    """
    Find the smallest missing positive number by creating a hash.
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
