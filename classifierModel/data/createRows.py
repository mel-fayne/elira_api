import random

# ------- Generate Academic Rows ---------------

# def create_value_tuple(numbers):
#     numbers = sorted(numbers, reverse=True)
#     values = [(numbers[i], numbers[i+1]) for i in range(len(numbers)-1)]
#     values.append((numbers[-1], 0))
#     return tuple(values)


# def generate_random_numbers(range_tuple, make_low):
#     low, high = range_tuple
#     median_value = (low + high) / 2

#     if make_low:
#         upper_limit = median_value
#         lower_limit = low
#     else:
#         upper_limit = high
#         lower_limit = median_value

#     random_numbers = []
#     for _ in range(3):
#         number = round(random.uniform(lower_limit, upper_limit), 1)
#         random_numbers.append(number)

#     return random_numbers


# unitsMakeLow = {
#     'CS01': (
#         ('AI', False),
#         ('CS', True),
#         ('DA', True),
#         ('GD', True),
#         ('HO', False),
#         ('IS', True),
#         ('NA', True),
#         ('SD', False)
#     ),
#     'CS02': (
#             ('AI', True),
#             ('CS', True),
#             ('DA', True),
#             ('GD', True),
#             ('HO', False),
#             ('IS', True),
#             ('NA', True),
#             ('SD', True)
#     ),
#     'CS04': (
#             ('AI', True),
#             ('CS', False),
#             ('DA', False),
#             ('GD', True),
#             ('HO', True),
#             ('IS', True),
#             ('NA', False),
#             ('SD', True)
#     ),
#     'CS05': (
#         ('AI', False),
#         ('CS', True),
#         ('DA', True),
#         ('GD', True),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', False)

#     ),
#     'CS06': (
#         ('AI', False),
#         ('CS', True),
#         ('DA', False),
#         ('GD', True),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
#     'CS07': (
#         ('AI', True),
#         ('CS', True),
#         ('DA', True),
#         ('GD', True),
#         ('HO', True),
#         ('IS', False),
#         ('NA', True),
#         ('SD', False),
#     ),
#     'CS08': (
#         ('AI', True),
#         ('CS', True),
#         ('DA', True),
#         ('GD', True),
#         ('HO', True),
#         ('IS', True),
#         ('NA', False),
#         ('SD', True),
#     ),
#     'CS09': (
#         ('AI', True),
#         ('CS', False),
#         ('DA', True),
#         ('GD', True),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
#     'CS10': (

#         ('AI', False),
#         ('CS', True),
#         ('DA', True),
#         ('GD', True),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
#     'CS11': (
#             ('AI', True),
#             ('CS', True),
#             ('DA', True),
#             ('GD', True),
#             ('HO', True),
#             ('IS', False),
#             ('NA', True),
#             ('SD', True)
#     ),
#     'CS16': (

#         ('AI', True),
#         ('CS', True),
#         ('DA', True),
#         ('GD', False),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
#     'CS17': (

#         ('AI', True),
#         ('CS', True),
#         ('DA', True),
#         ('GD', False),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
#     'CS18': (

#         ('AI', True),
#         ('CS', True),
#         ('DA', True),
#         ('GD', False),
#         ('HO', True),
#         ('IS', True),
#         ('NA', True),
#         ('SD', True)
#     ),
# }

# cs01 = [
#     [66.68, 53.34, 40.0, 26.66, 13.32],
#     [100, 80.0, 60.0, 40.0, 20.0],
#     [100, 80.0, 60.0, 40.0, 20.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs02 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [33.33, 26.66, 19.99, 13.32, 6.65],
#     [66.66, 53.33, 40.0, 26.67, 13.34],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs04 = [
#     [14.29, 11.43, 8.57, 5.71, 2.85],
#     [57.16, 45.73, 34.3, 22.87, 11.44],
#     [85.74, 68.59, 51.44, 34.29, 17.14],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs05 = [
#     [28.58, 22.86, 17.14, 11.42, 5.7],
#     [85.74, 68.59, 51.44, 34.29, 17.14],
#     [100, 80.0, 60.0, 40.0, 20.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs06 = [
#     [25, 20.0, 15.0, 10.0, 5.0],
#     [20, 16.0, 12.0, 8.0, 4.0],
#     [75, 60.0, 45.0, 30.0, 15.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs07 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [50, 40.0, 30.0, 20.0, 10.0],
#     [100, 80.0, 60.0, 40.0, 20.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs08 = [
#     [33.33, 26.66, 19.99, 13.32, 6.65],
#     [66.66, 53.33, 40.0, 26.67, 13.34],
#     [66.66, 53.33, 40.0, 26.67, 13.34],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs09 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [50, 40.0, 30.0, 20.0, 10.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs10 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [33.33, 26.66, 19.99, 13.32, 6.65],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs11 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs16 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [50, 40.0, 30.0, 20.0, 10.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs17 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [100, 80.0, 60.0, 40.0, 20.0],
#     [100, 80.0, 60.0, 40.0, 20.0]
# ]

# cs18 = [
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0],
#     [0, 0.0, 0.0, 0.0, 0.0]
# ]

# numbers = []
# for spec in unitsMakeLow['CS18']:
#     for data in cs18:
#         # iterate through each semester creating tuples for each group of 3 performing students
#         values = create_value_tuple(data)
#         for value in values:
#             numbers.extend(generate_random_numbers(value, spec[1]))

# for num in numbers:
#     print(num)

# --------------------------------------
# # function to create semester variation rows
# marks = [
#     0,
#     0,
#     0,s
#     0
# ]

# for mark in marks:
#     data = []
#     gap = round((mark / 5), 2)
#     startVal = mark
#     data.append(startVal)
#     i = 0
#     while i < 4:
#         startVal = round((startVal - gap), 2)
#         data.append(startVal)
#         i = i + 1
#     print(f"{data},")

# --------------------------------------

# generate values for the other columns
# onedata = [
#    25,
#    20,
#    15,
#    10,
#    5
# ]
# twodata = [
#    75,
#    60,
#    45,
#    30,
#    15
# ]
# fourdata = [
#     100,
#     80,
#     60,
#     40,
#     20
# ]

# onevalues = create_value_tuple(onedata)
# twovalues = create_value_tuple(twodata)
# fourvalues = create_value_tuple(fourdata)
# random_numbers = generate_random_numbers(onevalues)
# for num in random_numbers:
#         print(num)
# random_numbers = generate_random_numbers(twovalues)
# for num in random_numbers:
#         print(num)
# random_numbers = generate_random_numbers(fourvalues)
# for num in random_numbers:
#         print(num)

# ------- Generate Github Rows -----------------
# SPECIALIZATIONS = {
#     'Network Administration': ['c', 'c++', 'python'],
#     'Database Administration': ['sql', 'python', 'php'],
#     'A.I & Data Science': ['python', 'jupyter', 'r', 'sql'],
#     'Cyber Security': ['c', 'c++', 'python', 'javascript'],
#     'Software Development': ['java', 'dart', 'kotlin', 'go', 'sql','typescript', 'html', 'css', 'javascript', 'python', 'swift', 'objective-c', 'c#'],
#     'Information Systems': ['java', 'html', 'javascript', 'python', 'sql'],
#     'Hardware & Operating Systems': ['c', 'c++', 'Rust'],
#     'Graphics & Design': ['html', 'css', 'javascript', 'c#']
# }

# # Generate 80 random numbers between 0 and 50
# low_numbers = [round(random.uniform(0, 50), 1) for _ in range(80)]

# # Generate 25 random numbers between 50 and 100
# high_numbers = [round(random.uniform(50, 100), 1) for _ in range(25)]

# # Shuffle the numbers and combine them
# numbers = low_numbers + high_numbers
# random.shuffle(numbers)
# #               0   1       2       3     4     5     6       7
# ifprints = [False, False, False, False, True, False, False, False]

# # ifprints = [False, False, False, False, False, False, False, False]

# print('c#')
# for generate in ifprints:
#     if generate:
#         for i in range(15):
#             print(0)
#         for num in numbers:
#             print(num)
#     else:
#         for i in range(120):
#             print(0)


# def get21():
#     lists = []
#     for _ in range(6):
#         total = 9
#         lst = []
#         for _ in range(1):
#             num = random.randint(0, total)
#             lst.append(num)
#             total -= num
#         lst.append(total)
#         lst.sort(reverse=True)
#         lists.append(lst)
#     return lists

# lists = get21()

# for j in range(45):
#     print(0)
# for lst in lists:
#     print(lst[1])

# ------- Generate Internship Rows -----------------

# Generate 25 zeroes and 5 ones
# zeros = [0] * 25
# ones = [1] * 5
# secondYrs = zeros + ones
# random.shuffle(secondYrs)

# zeros = [0] * 15
# ones = [1] * 15
# thirdYrs = zeros + ones
# random.shuffle(thirdYrs)

# zeros = [0] * 5
# ones = [1] * 25
# fourthYrs = zeros + ones
# random.shuffle(fourthYrs)

# for num in secondYrs:
#     print(num)

# print('time')

# for num in secondYrs:
#     if num == 1:
#         print(round(random.uniform(1, 6)))
#     else:
#         print(0)
