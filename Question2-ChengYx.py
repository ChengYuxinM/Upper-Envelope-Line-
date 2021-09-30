# ---------------------------- Divide and Conqure without Sort -----------------------------------
# @Time    : 2021/9/27
# @Author  : CHENG,Yuxin
# @File    : upperEnvelope.py

import numpy as np
import math
import matplotlib.pyplot as plt

# Imply to draw up to 10 different color lines in draw step
colors = ['orange', 'blue', 'black', 'm', 'green', 'purple', 'yellow', 'cyan', 'violet', 'sienna']


def find_cross(line1, line2):  # Find the instersection of two line and merge them with standard format
    # if slopes of line1 and line2 are equal
    if line1[0] == line2[0]:
        if line1[1] > line2[1]:
            return np.array([[float('-inf'), line1[0], line1[1], float('inf')]])
        else:
            return np.array([[float('-inf'), line2[0], line2[1], float('inf')]])
    # Compute intersection of two line and merge the two line with format [[left side, k, b, right side]]
    x = (line2[1] - line1[1]) / (line1[0] - line2[0])
    if line1[0] > line2[0]:
        return np.array([[float('-inf'), line2[0], line2[1], x],
                         [x, line1[0], line1[1], float('inf')]])
    else:
        return np.array([[float('-inf'), line1[0], line1[1], x],
                         [x, line2[0], line2[1], float('inf')]])


def find_cross_x(line1, line2):  # Find the intersection of two line in x dimension
    return (line2[1] - line1[1]) / (line1[0] - line2[0])


def slide_the_window(left_lim, right_lim, i, j, section_left_x, section_right_x):
    left_lim = right_lim
    if section_left_x[i] >= section_right_x[j]:
        if section_left_x[i] == math.inf and section_right_x[j] == math.inf:
            return left_lim, right_lim, i, j
        if section_left_x[i] > section_right_x[j + 1]:
            right_lim = section_right_x[j + 1]
            j += 1
        else:
            right_lim = section_left_x[i]
            j += 1
    elif section_right_x[j] > section_left_x[i]:
        if section_right_x[j] > section_left_x[i + 1]:
            right_lim = section_left_x[i + 1]
            i += 1
        else:
            right_lim = section_right_x[j]
            i += 1
    return left_lim, right_lim, i, j


def merge(section_left, section_right):
    # Initial data structure
    merge_answer = np.array([[]]).reshape(-1, 4)

    # Initial the first window
    if section_left[0][3] <= section_right[0][3]:
        left_lim = section_left[0][0]
        right_lim = section_left[0][3]
    else:
        left_lim = section_right[0][0]
        right_lim = section_right[0][3]

    # Extract the intersections in two partial upper envelopes
    section_left_x = section_left[:, 3]
    section_right_x = section_right[:, 3]

    # Merge two partial upper envelopes
    i, j = 0, 0
    while True:
        # Jump out when the window arrives the far right section
        if left_lim == float('inf') and right_lim == float('inf'):
            break

        # Deal with parallel condition
        if section_left[i][1] == section_right[j][1] and section_left[i][2] > section_right[j][2]:

            # If the the same line in the adjacent two section is remaining, extend it
            if merge_answer.shape[0] != 0:
                if section_left[i][1] == merge_answer[merge_answer.shape[0] - 1][1] and section_left[i][2] == \
                        merge_answer[merge_answer.shape[0] - 1][2]:
                    merge_answer[merge_answer.shape[0] - 1][3] = right_lim

                    # Slide the next window
                    left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x,
                                                                 section_right_x)
                    continue

            # Insert the proper line
            merge_answer = np.append(merge_answer, [section_left[i]], axis=0)
            merge_answer[merge_answer.shape[0] - 1][3] = right_lim
            merge_answer[merge_answer.shape[0] - 1][0] = left_lim

            # Slide the next window
            left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x, section_right_x)
            continue

        # Deal with another parallel condition
        if section_left[i][1] == section_right[j][1] and section_left[i][2] <= section_right[j][2]:

            # If the the same line in the adjacent two section is remaining, extend it
            if merge_answer.shape[0] != 0:
                if section_right[j][1] == merge_answer[merge_answer.shape[0] - 1][1] and section_right[j][2] == \
                        merge_answer[merge_answer.shape[0] - 1][2]:
                    merge_answer[merge_answer.shape[0] - 1][3] = right_lim

                    # Slide the next window
                    left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x,
                                                                 section_right_x)
                    continue

            # Insert the proper line
            merge_answer = np.append(merge_answer, [section_right[j]], axis=0)
            merge_answer[merge_answer.shape[0] - 1][3] = right_lim
            merge_answer[merge_answer.shape[0] - 1][0] = left_lim

            # Slide the next window
            left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x, section_right_x)
            continue

        # Deal with unparallel condition, the two line must have an intersection
        cross = find_cross_x(section_left[i, 1:3], section_right[j, 1:3])
        # The intersection falls into the window
        if cross < right_lim and cross > left_lim:

            #Judge which line is the left upper envelope and right upper envelope
            if section_left[i][1] < section_right[j][1]:
                left = section_left[i]
                right = section_right[j]
            else:
                left = section_right[j]
                right = section_left[i]

            # If the the same line in the adjacent two section is remaining, extend it
            if merge_answer.shape[0] != 0:
                if left[1] == merge_answer[merge_answer.shape[0] - 1][1] and left[2] == \
                        merge_answer[merge_answer.shape[0] - 1][2]:
                    merge_answer[merge_answer.shape[0] - 1][3] = cross
                    merge_answer = np.append(merge_answer, [right], axis=0)
                    merge_answer[merge_answer.shape[0] - 1][0] = cross
                    merge_answer[merge_answer.shape[0] - 1][3] = right_lim

                    # Slide the next window
                    left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x,
                                                                 section_right_x)
                    continue
            # Insert the proper lines
            merge_answer = np.append(merge_answer, [left], axis=0)
            merge_answer[merge_answer.shape[0] - 1][0] = left_lim
            merge_answer[merge_answer.shape[0] - 1][3] = cross
            merge_answer = np.append(merge_answer, [right], axis=0)
            merge_answer[merge_answer.shape[0] - 1][0] = cross
            merge_answer[merge_answer.shape[0] - 1][3] = right_lim

            # Slide the next window
            left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x, section_right_x)
            continue

        else:

            # If the intersection falls in the right of the window
            if cross >= right_lim:

                # Store the line with smaller k
                if section_left[i][1] < section_right[j][1]:
                    left = section_left[i]
                else:
                    left = section_right[j]

            # If the intersection falls in the left of the window
            else:
                # Store the line with smaller k
                if section_left[i][1] > section_right[j][1]:
                    left = section_left[i]
                else:
                    left = section_right[j]

            # If the the same line in the adjacent two section is remaining, extend it
            if merge_answer.shape[0] != 0:
                if left[1] == merge_answer[merge_answer.shape[0] - 1][1] and left[2] == \
                        merge_answer[merge_answer.shape[0] - 1][2]:
                    merge_answer[merge_answer.shape[0] - 1][3] = right_lim

                    # Slide the next windows
                    left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x,
                                                                 section_right_x)
                    continue

            # Insert the proper lines
            merge_answer = np.append(merge_answer, [left], axis=0)
            merge_answer[merge_answer.shape[0] - 1][0] = left_lim
            merge_answer[merge_answer.shape[0] - 1][3] = right_lim

            # Slide the next windows
            left_lim, right_lim, i, j = slide_the_window(left_lim, right_lim, i, j, section_left_x, section_right_x)
            continue

    return merge_answer


def divide_iteration(lines, left, right):  # Divide and Conqure: lines->data set; left, right->indices in data set
    # Jump out the recursion when left == right or left+1 == right and return the partial upper envelope
    if left == right:
        return np.array([[float('-inf'), lines[left][0], lines[left][1], float('inf')]])
    if left + 1 == right:
        section = find_cross(lines[left], lines[right])
        return section
    # Recursion
    mid = int((left + right) / 2)  # Divide
    section_left = divide_iteration(lines, left, mid - 1)
    section_right = divide_iteration(lines, mid, right)
    # Merge the two partial upper envelope
    return merge(section_left, section_right)  # Conqure


def draw_plot(lines):  # lines->dataset
    color = 0
    for line in lines:
        x = np.linspace(-10, 10, 500)
        y = line[0] * x + line[1]
        plt.plot(x, y, c=colors[color % 10])
        color += 1
    plt.show()


def draw_answer(lines, high):  # lines->dataset; high->upper envelope
    color = 0
    # Draw all lines
    for line in lines:
        x = np.linspace(-8, 8, 500)
        y = line[0] * x + line[1]
        plt.plot(x, y, c=colors[color % 10])
        color += 1
    # Draw Upper Envelope with red bold line in the same plot
    for line in high:
        if line[0] == float('-inf'):
            if line[3] == float('inf'):
                x = np.linspace(-8, 8, 500)
            else:
                x = np.linspace(-8, line[3], 500)
        elif line[3] == float('inf'):
            x = np.linspace(line[0], 8, 500)
        else:
            x = np.linspace(line[0], line[3], 500)
        y = line[1] * x + line[2]
        plt.plot(x, y, c='red', linewidth=2.5)
    plt.show()


if __name__ == '__main__':
    # Initial data structure
    lines = np.asarray([[]]).reshape(-1, 2)
    # Input data with k == inf or b == inf ends
    while True:
        k, b = input().split()
        if float(k) == float('inf') or float(b) == float('inf'):
            break
        lines = np.append(lines, [[float(k), float(b)]], axis=0)
    # Draw the input dataset
    draw_plot(lines)
    # Divide and conqure to compute upper envelope
    high = divide_iteration(lines, 0, lines.shape[
        0] - 1)  # high->upper envelope with format stacking [[left side, k, b, right side]]
    # Print upper envelope
    print(high)
    # Draw upper envelope in dataset to inspect the answer
    draw_answer(lines, high)

'''
0 0
-4 -5
-4 -7
-2 3
0 -5
0 1
1 4
1 -3
3 -4
3 5
inf inf
'''
'''
0 0
0 -5
0 -5
0 2
inf inf
'''
'''
1 -1
2 -2
-1 -1
-2 -2
0 0
0 -5
inf inf
'''
'''
-2 -6
2 -6
-2 -8
2 -8
0 0
0 -3
inf inf
'''
