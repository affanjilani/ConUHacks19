# Create your custom classifier with positive or negative examples.
# Include at least two sets of examples,
# either two positive example files or one positive and one negative file.


import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2019-01-26',
    iam_apikey='t5c1sjiz8FCLAYyG8E5A8G3KYkk45Y3dalXMu8H1oNrP')

# THIS IS WHERE YOU DELETE THE CLASSIFIER
# visual_recognition.delete_classifier('PUT ID HERE')


#THIS IS WHERE YOU INITIALIZE YOUR CLASSIFIER, STEP ONE
# with open('/Users/abdulrahim23/Desktop/Hackathon/SEDANCARS.zip', 'rb') as Sedan_Cars, \
#         open('/Users/abdulrahim23/Desktop/Hackathon/SUVCARS.zip', 'rb') as Suv_Cars, \
#         open('/Users/abdulrahim23/Desktop/Hackathon/MONSTERTRUCKS.zip', 'rb') as Monster_Trucks:
#          model = visual_recognition.create_classifier(
#         'Cars',
#          sedancars_positive_examples=Sedan_Cars,
#          suvcarscars_positive_examples=Suv_Cars,
#          monstertrucks_negative_examples=Monster_Trucks).get_result()
# print(json.dumps(model, indent=3))


#
# # THIS IS HOW YOU LIST ALL THE CLASSIFIERS
# classifiers = visual_recognition.list_classifiers(verbose=True).get_result()
# print(json.dumps(classifiers, indent=2))


# # THIS IS HOW YOU CHECK A PHOTO(S)  ONTO OUR CLASSIFIER AND PUT OUTPUT INTO A TEXT FILE
file = open('/Users/abdulrahim23/Desktop/data.txt','w')
with open('/Users/abdulrahim23/Desktop/Hackathon/truck8.jpg', 'rb') as images_file:
    classes = visual_recognition.classify(
        images_file,
        classifier_ids=["Cars_1711990083"]).get_result()

    file.write(str(json.dumps(classes, indent=2)))
    file.close()
print(json.dumps(classes, indent=2))


#WHERE THE EDITS HAPPENED***** HERE********
file1 = open('/Users/abdulrahim23/Desktop/data.txt','r')
counter = 0
for line in file1:
    str = line.strip(' ')
    str = str.split(':')
    if (str[0] == '\"score\"'):
        x = str[1]
        print x
        if(x>=0.60):
             counter+=1
        else:
              counter+=0
print counter







#ORIGINAL DATA TEXT FILE
# # #open a file to read
# file1 = open('/Users/abdulrahim23/Desktop/data.txt','r')
# counter = 0
# for line in file1:
#     str = line.strip(' ')
#     str = str.split(':')
#     print str
#     if (str[0] == '\"class\"'):
#         if(str[1].strip(' ') == '\"sedancars\"\n' or str[1].strip(' ') == '\"suvcarscars\"\n'):
#             counter +=1
#
# print counter


