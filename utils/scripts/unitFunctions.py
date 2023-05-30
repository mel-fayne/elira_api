import json

# from student.models.academicModels import SchoolUnit

UNIT_TAGS = {
    'cs01 : Mathematics and Statistics': ['statistics', 'mathematics', 'calculus', 'algebra', 'probability', 'equations', 'vector', 'numerical'],
    'cs02 : Hardware and Electronics': ['electronics', 'physics', 'chemistry', 'mechanics', 'quantum', 'logic', 'semiconductor', 'embedded', 'hardware'],
    'cs03 : Skills and Ethics': ['communication', 'ethics', 'critical', 'skills', 'society', 'legal', 'ethical', 'law'],
    'cs04 : Systems and Architecture': ['assembly', 'architecture', 'parallel', 'compiler', 'operating', 'distributed', 'hardware', 'computing', 'complex', 'analysis'],
    'cs05 : Programming and Software Development': ['programming', 'algorithms', 'structures', 'development', 'software', 'quality', 'cam'],
    'cs06 : Database Administration': ['database', 'modeling', 'distributed', 'warehouse'],
    'cs07 : Web and Mobile App Development': ['web', 'mobile'],
    'cs08 : Networking': ['network', 'communications', 'signal', 'networks', 'networking', 'multimedia', 'media'],
    'cs09 : Cyber Security': ['cryptography', 'security', 'encryption', ],
    'cs10 : Artificial Intelligence and Data Science': ['knowledge', 'robotics', 'artificial', 'mining', 'intelligence', 'learning', 'neural', 'automata', 'natural'],
    'cs11 : Information Systems': ['information', 'business', 'processes', 'transaction', 'enterprise', 'decision'],
    'cs12 : Industrial Attachment': ['attachment'],
    'cs13 : Final Project': ['project'],
    'cs14 : Research Methodology': ['research', 'thesis'],
    'cs15 : Business and Management': ['business', 'commerce', 'management', 'finance', 'entrepreneurship', 'marketing', 'accounts', 'accounting', 'economics', 'governance'],
    'cs16 : Computer Graphics': ['image', 'graphics', 'simulation', 'compression', 'modelling'],
    'cs17 : User Design': ['interface', 'user', 'human'],
    'cs18 : Gaming Development': ['game', 'games', 'gaming', 'unity']
}

UNIT_GROUPS = [
    'cs01 : Mathematics and Statistics',
    'cs02 : Hardware and Electronics',
    'cs03 : Skills and Ethics',
    'cs04 : Systems and Architecture',
    'cs05 : Programming and Software Development',
    'cs06 : Database Administration',
    'cs07 : Web and Mobile App Development',
    'cs08 : Networking',
    'cs09 : Cyber Security',
    'cs10 : Artificial Intelligence and Data Science',
    'cs11 : Information Systems',
    'cs12 : Industrial Attachment',
    'cs13 : Final Project',
    'cs14 : Research Methodology',
    'cs15 : Business and Management',
    'cs16 : Computer Graphics',
    'cs17 : User Design',
    'cs18 : Gaming Development'
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


jkuatUnits_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/jkuat_units.json'
uonUnits_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/uon_units.json'
strathUnits_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/units/strath_units.json'

jkuatGroups_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/unitGroups/jkuatGroups.json'
uonGroups_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/unitGroups/uonGroups.json'
strathGroups_path = '/home/mel/Desktop/code-lab/api/elira_api/utils/unitGroups/strathGroups.json'

with open(strathUnits_path, 'r') as file:
    unitsData = json.load(file)

with open(strathGroups_path, 'r') as file:
    groupsData = json.load(file)

# # Load School Units to db

# school_units = []

# for item in unitsData:
#     school_unit = SchoolUnit(
#         school=item.get('school', ''),
#         semsester=item.get('semsester', 1.1),
#         name=item.get('name', ''),
#         elective=item.get('elective', False),
#         elective_group=item.get('elective_group', ''),
#         grouping_name=item.get('grouping_name', []),
#         grouping_code=item.get('grouping_code', []),
#         unit_percentages=item.get('unit_percentages', []),
#         grade=item.get('grade', None),
#         mark=item.get('mark', 0.0),
#     )
#     school_units.append(school_unit)

# SchoolUnit.objects.bulk_create(school_units)

# print(f"SchoolUnit Objects Created: {len(school_units)}")


# # Load School Groupings to db

# school_groups = []

# for item in groupsData:
#     school_group = SchoolGrouping(
#         school=item.get('school', ''),
#         name=item.get('name', ''),
#         unit_percentage=item.get('unit_percentages', ''),
#         code=item.get('code', ''),
#     )
#     school_units.append(school_group)

# SchoolGrouping.objects.bulk_create(school_groups)

# print(f"SchoolGroup Objects Created: {len(school_groups)}")


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
    
# # Get Documentation Formatting
# for group in UNIT_GROUPS:
#     print(f"### {group}")
#     print(f"- Code : {group[0:4]}")
#     print(f"- Name : {group[4:len(group)+1]}")
    
#     group_units = []
#     for item in unitsData:
#         if group in item['grouping_name']:
#             group_units.append(item)
            
#     print(f"- Unit Count : {len(group_units)}")
#     if len(group_units) == 0:
#         print("- Unit_perc : 0")
#     else:
#         print(f"- Unit_perc : {round(100 / len(group_units), 2)}")
#     print(" ")
#     print("<br/>")
#     print(" ")
    
#     for item in group_units:
#         print(f"- {item['name']} - {item['semester']}")

#     print(' ')

# # Create Unit Percentages List in Json
for unitItem in unitsData:
    unitPercs = []

    for groupItem in groupsData:
        if groupItem['code'] in unitItem['grouping_code']:
            unitPercs.append(groupItem['unit_percentage'])
    
    print(' ')
    print(unitItem['name'])
    print(unitPercs)
    print(' ')

# # ---------- Get Particular Units ------------
# for item in data:
#     if item['semester'] == '4.1' and item['elective'] == 'True:
#         print(item['unit'])
