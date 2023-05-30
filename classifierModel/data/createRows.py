import random

# ------- Generate Academic Rows ---------------

def create_value_tuple(numbers):
    numbers = sorted(numbers, reverse=True)
    values = [(numbers[i], numbers[i+1]) for i in range(len(numbers)-1)]
    values.append((numbers[-1], 0))
    return tuple(values)


def generate_numbers(row, makeLow):
    median = (row[0] + row[1]) / 2

    if makeLow:
        numbers = [random.uniform(median, row[1]) for i in range(24)]
    else:
        numbers = [random.uniform(row[0], median) for i in range(24)]

    return numbers


unitsMakeLow = {
    'CS01': (
            ('NA', True),
            ('DA', True),
            ('SD', False),
            ('AI', False),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', False)
    ),
    'CS02': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', False)
    ),
    'CS04': (
            ('NA', False),
            ('DA', False),
            ('SD', True),
            ('AI', True),
            ('CS', False),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS05': (
            ('NA', True),
            ('DA', True),
            ('SD', False),
            ('AI', False),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS06': (
            ('NA', True),
            ('DA', False),
            ('SD', True),
            ('AI', False),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS07': (
            ('NA', True),
            ('DA', True),
            ('SD', False),
            ('AI', True),
            ('CS', True),
            ('GD', True),
            ('IS', False),
            ('HO', True)
    ),
    'CS08': (
            ('NA', False),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS09': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', False),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS10': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', False),
            ('CS', True),
            ('GD', True),
            ('IS', True),
            ('HO', True)
    ),
    'CS11': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', True),
            ('IS', False),
            ('HO', True)
    ),
    'CS16': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', False),
            ('IS', True),
            ('HO', True)
    ),
    'CS17': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', False),
            ('IS', True),
            ('HO', True)
    ),
    'CS18': (
            ('NA', True),
            ('DA', True),
            ('SD', True),
            ('AI', True),
            ('CS', True),
            ('GD', False),
            ('IS', True),
            ('HO', True)
    ),
}

data = [
    100,
    80,
    60,
    40,
    20
]

values = create_value_tuple(data)

for value in values:
    for spec in unitsMakeLow['CS01']:
        numbers = generate_numbers(value, spec[1])
    for num in numbers:
        print(round(num))

# ------- Generate Github Rows -----------------

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