

def euclidean_distance(point_A,point_B):
    result=0
    for i in range(len(point_A)):
        result+=(point_A[i] - point_B[i]) ** 2

    return result

def manhattan_distance(point_A,point_B):
    result = 0
    for i in range(len(point_A)):
        result += abs(point_A[i] - point_B[i])

    return result


if __name__ == "__main__":
    print('puzzle_sate class')
