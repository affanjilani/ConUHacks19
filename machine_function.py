

def machine_function(filepath):
    import json
    import os.path
    from watson_developer_cloud import VisualRecognitionV3
    visual_recognition = VisualRecognitionV3(
        '2019-01-26',
        iam_apikey='t5c1sjiz8FCLAYyG8E5A8G3KYkk45Y3dalXMu8H1oNrP')
    #replace with pathways to where these zipfiles are stored
    with open('/Users/abdulrahim23/Desktop/Hackathon/SEDANCARS.zip', 'rb') as Sedan_Cars, \
         open('/Users/abdulrahim23/Desktop/Hackathon/SUVCARS.zip', 'rb') as Suv_Cars, \
         open('/Users/abdulrahim23/Desktop/Hackathon/MONSTERTRUCKS.zip', 'rb') as Monster_Trucks:
         model = visual_recognition.create_classifier(
         'Cars',
            sedancars_positive_examples=Sedan_Cars,
            suvcarscars_positive_examples=Suv_Cars,
            monstertrucks_negative_examples=Monster_Trucks).get_result()
    print(json.dumps(model, indent=3))

# THIS IS HOW YOU CHECK A PHOTO(S)  ONTO OUR CLASSIFIER AND PUT OUTPUT INTO A TEXT FILE
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path,'./data.txt')
    file = open(path) ##replace with file path
    with open(filepath, 'rb') as images_file:
     classes = visual_recognition.classify(
        images_file,
        classifier_ids=["Cars_1711990083"]).get_result()

    file.write(str(json.dumps(classes, indent=2)))
    file.close()

    # open a file to read and keep counter to count cars, so it has to read the absolute path of the file
    #and then "r" so it could read
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path,'./data.txt')
    file1 = open(path)
    #file1 = open(os.path.abspath(os.path.dirname(__file__)))
    counter = 0
    for line in file1:
        str = line.strip(' ')
        str = str.split(':')
        if (str[0] == '\"class\"'):
            if (str[1].strip(' ') == '\"sedancars\"\n' or str[1].strip(' ') == '\"suvcarscars\"\n'):
                counter += 1

    print counter


