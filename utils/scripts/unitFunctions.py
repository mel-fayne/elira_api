import json
UNIT_TAGS = {
    'CS01 : Mathematics and Statistics': ['statistics', 'mathematics', 'calculus', 'algebra', 'probability', 'equations', 'vector', 'numerical'],
    'CS02 : Hardware and Electronics': ['electronics', 'physics', 'chemistry', 'mechanics', 'quantum', 'logic', 'semiconductor', 'embedded', 'hardware'],
    'CS03 : Skills and Ethics': ['communication', 'ethics', 'critical', 'skills', 'society', 'legal', 'ethical', 'law'],
    'CS04 : Systems and Architecture': ['assembly', 'architecture', 'parallel', 'compiler', 'operating', 'distributed', 'hardware', 'computing', 'complex', 'analysis'],
    'CS05 : Programming and Software Development': ['programming', 'algorithms', 'structures', 'development', 'software', 'quality', 'cam'],
    'CS06 : Database Administration': ['database', 'modeling', 'distributed', 'warehouse'],
    'CS07 : Web and Mobile App Development': ['web', 'mobile'],
    'CS08 : Networking': ['network', 'communications', 'signal', 'networks', 'networking', 'multimedia', 'media'],
    'CS09 : Cyber Security': ['cryptography', 'security', 'encryption', ],
    'CS10 : Artificial Intelligence and Data Science': ['knowledge', 'robotics', 'artificial', 'mining', 'intelligence', 'learning', 'neural', 'automata', 'natural'],
    'CS11 : Information Systems': ['information', 'business', 'processes', 'transaction', 'enterprise', 'decision'],
    'CS12 : Industrial Attachment': ['attachment'],
    'CS13 : Final Project': ['project'],
    'CS14 : Research Methodology': ['research', 'thesis'],
    'CS15 : Business and Management': ['business', 'commerce', 'management', 'finance', 'entrepreneurship', 'marketing', 'accounts', 'accounting', 'economics', 'governance'],
    'CS16 : Computer Graphics': ['image', 'graphics', 'simulation', 'compression', 'modelling'],
    'CS17 : User Design': ['interface', 'user', 'human'],
    'CS18 : Gaming Development': ['game', 'games', 'gaming', 'unity']
}

UNIT_GROUPS = [
    'CS01 : Mathematics and Statistics',
    'CS02 : Hardware and Electronics',
    'CS03 : Skills and Ethics',
    'CS04 : Systems and Architecture',
    'CS05 : Programming and Software Development',
    'CS06 : Database Administration',
    'CS07 : Web and Mobile App Development',
    'CS08 : Networking',
    'CS09 : Cyber Security',
    'CS10 : Artificial Intelligence and Data Science',
    'CS11 : Information Systems',
    'CS12 : Industrial Attachment',
    'CS13 : Final Project',
    'CS14 : Research Methodology',
    'CS15 : Business and Management',
    'CS16 : Computer Graphics',
    'CS17 : User Design',
    'CS18 : Gaming Development'
]

SEMESTERS = [
    '1.0',
    '1.1',
    '1.2',
    '2.0',
    '2.1',
    '2.2',
    '3.0',
    '3.1',
    '3.2',
    '4.0',
    '4.1',
    '4.2']


jkuat_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/jkuat_units.json'
uon_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/uon_units.json'
ku_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/ku_units.json'
cuea_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/cuea_units.json'
strath_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/strath_units.json'

with open(jkuat_path, 'r') as file:
    data = json.load(file)

# # ---------- Group Units ------------
# for item in data:
#     title = item['unit']
#     keywords = [word for word in title.lower().split()]

#     name_matches = []
#     code_matches = []

#     for group, group_keywords in UNIT_TAGS.items():
#         for keyword in keywords:
#             if keyword in group_keywords:
#                 if group not in name_matches:
#                     name_matches.append(group)
#                     code_matches.append(group[0:4])

#     item['grouping_names'] =  name_matches
#     item['grouping_codes'] = code_matches

#     print(item)
#     print(',')

# # ---------- Get Group Units ------------
# for sem in SEMESTERS:
#     print('______________________________________')
#     print(sem)

#     units = []
#     for item in data:
#         if item['semester'] == sem:
#             units.append(item)
    
for group in UNIT_GROUPS:
    print('______________________________________')
    print(f"### {group}")
    print(f"- Code : {group[0:4]}")
    print(f"- Name : {group[4:len(group)+1]}")
    print("- Unit_perc : ")
    print(" ")
    print("<br/>")
    print(" ")
    group_units = []
    for item in data:
        if group in item['grouping_names']:
            group_units.append(item)
            print(f"        - {item['unit']} - {item['semester']}")
    
    print(f"Unit Count : {len(group_units)}")
    # if group_units != []:
    #     print(' ')
    #     print(group)
    #     print(' ')
    #     for item in group_units:
    #         print(item['unit'])

    print('______________________________________')
    

# # ---------- Get Particular Units ------------
# for item in data:
#     if item['semester'] == '4.1' and item['elective'] == 'True:
#         print(item['unit'])
