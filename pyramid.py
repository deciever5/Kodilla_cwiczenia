def longest_slide_down(pyramid):
    answer1, previous_max_idx = [0], int(0)
    for idx, num in enumerate(pyramid[1::]):
        nums_considered = [num[previous_max_idx], num[previous_max_idx + 1]]
        answer1[0] += max(nums_considered)
        previous_max_idx = num.index(max(nums_considered))
    return answer1[0]


def longest_slide_up(pyramid):
    allchains = []
    for num_in_last_row in pyramid[-1::]:

        for index_in_last_row, starting_number in enumerate(num_in_last_row):
            allchains.append(answer[0])
            answer[0] = starting_number
            previous_max_idx = index_in_last_row
            for idx_of_current_row, current_row in reversed(list(enumerate(pyramid[:-1:]))):
                if previous_max_idx == len(current_row):
                    nums_considered = [current_row[len(current_row) - 1]]
                elif previous_max_idx == 0:
                    nums_considered = [current_row[0]]
                else:
                    nums_considered = [current_row[previous_max_idx], current_row[previous_max_idx - 1]]
                answer[0] += max(nums_considered)
                if current_row.index(max(nums_considered)) in (previous_max_idx, (previous_max_idx - 1)):
                    previous_max_idx = current_row.index(max(nums_considered))
                else:
                    while True:
                        if current_row[(current_row.index(max(nums_considered)) + 1)::].index(max(nums_considered)) in (
                                previous_max_idx, (previous_max_idx - 1)):
                            previous_max_idx = current_row.index(max(nums_considered))
                            break

                print(f'start= {starting_number} row{idx_of_current_row} = {answer[0]} {allchains}')


lista = [[75],
         [95, 64],
         [17, 47, 82],
         [18, 35, 87, 10],
         [20, 4, 82, 47, 65],
         [19, 1, 23, 75, 3, 34],
         [88, 2, 77, 73, 7, 63, 67],
         [99, 65, 4, 28, 6, 16, 70, 92],
         [41, 41, 26, 56, 83, 40, 80, 70, 33],
         [41, 48, 72, 33, 47, 32, 37, 16, 94, 29],
         [53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14],
         [70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57],
         [91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48],
         [63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31],
         [4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23]
         ]
answer = [0]
longest_slide_down(lista)
longest_slide_up(lista)
