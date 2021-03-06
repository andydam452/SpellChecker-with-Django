from collections import defaultdict 

def levenshtein_distance(source, target):
    tmp_source = ' ' + source
    tmp_target = ' ' + target

    distance_matrix = [[None] * len(tmp_source) for _ in range(len(tmp_target))]
    distance_matrix[0] = [i for i in range(len(tmp_source))]

    for i in range(len(tmp_target)):
        distance_matrix[i][0] = i

    for i in range(1, len(tmp_target)):
        for j in range(1, len(tmp_source)):
            substitution_cost = 0 if tmp_target[i] == tmp_source[j] else 1
            distance_matrix[i][j] = min(distance_matrix[i-1][j] + 1,
                                        distance_matrix[i][j-1] + 1,
                                        distance_matrix[i-1][j-1] + substitution_cost)

    return distance_matrix[-1][-1]

def damerau_levenshtein_distance(s1, s2):

    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2

    # character array
    da = defaultdict(int)

    # distance matrix
    score = [[0] * (len2 + 2) for x in range(len1 + 2)]

    score[0][0] = infinite
    for i in range(0, len1 + 1):
        score[i + 1][0] = infinite
        score[i + 1][1] = i
    for i in range(0, len2 + 1):
        score[0][i + 1] = infinite
        score[1][i + 1] = i

    for i in range(1, len1 + 1):
        db = 0
        for j in range(1, len2 + 1):
            i1 = da[s2[j - 1]]
            j1 = db
            cost = 1
            if s1[i - 1] == s2[j - 1]:
                cost = 0
                db = j

            score[i + 1][j + 1] = min(
                score[i][j] + cost,
                score[i + 1][j] + 1,
                score[i][j + 1] + 1,
                score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1),
            )
        da[s1[i - 1]] = i

    return score[len1 + 1][len2 + 1]