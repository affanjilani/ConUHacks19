import os
path = os.path.abspath(os.path.dirname(__file__))
def machine_function(filepath):
    import json
    import os.path
    from watson_developer_cloud import VisualRecognitionV3
    visual_recognition = VisualRecognitionV3(
        '2019-01-26',
        iam_apikey='t5c1sjiz8FCLAYyG8E5A8G3KYkk45Y3dalXMu8H1oNrP')
    #replace with pathways to where these zipfiles are stored


    # DELETE CLASSIFIER
    # visual_recognition.delete_classifier("Cars_735159945")
    # visual_recognition.delete_classifier("Cars_589670035")
    # visual_recognition.delete_classifier("Cars_1634596858")


    #List classifiers
    classifiers = visual_recognition.list_classifiers(verbose=True).get_result()
    print(json.dumps(classifiers,indent=2))
    print path

    # with open(os.path.join(path,'.\\SEDANCARS.zip'), 'rb') as Sedan_Cars, \
    #      open(os.path.join(path,'.\\SUVCARS.zip'), 'rb') as Suv_Cars, \
    #      open(os.path.join(path,'.\\MONSTERTRUCKS.zip'), 'rb') as Monster_Trucks:
    #      model = visual_recognition.create_classifier(
    #      'Cars',
    #         sedancars_positive_examples=Sedan_Cars,
    #         suvcarscars_positive_examples=Suv_Cars,
    #         monstertrucks_negative_examples=Monster_Trucks).get_result()
    # print(json.dumps(model, indent=3))

# # THIS IS HOW YOU CHECK A PHOTO(S)  ONTO OUR CLASSIFIER AND PUT OUTPUT INTO A TEXT FILE
    path1 = os.path.join(path,'.\\data.txt')
    print path1
    file = open(path1, 'w') ##replace with file path
    with open(filepath, 'rb') as images_file:
     classes = visual_recognition.classify(
        images_file,
        classifier_ids=["Cars_1711990083"]).get_result()

    file.write(str(json.dumps(classes, indent=2)))
    file.close()

    # open a file to read and keep counter to count cars, so it has to read the absolute path of the file
    #and then "r" so it could read
    path1 = os.path.join(path,'.\\data.txt')
    file1 = open(path1,'r')
    #file1 = open(os.path.abspath(os.path.dirname(__file__)))
    counter = 0
    for line in file1:
        string = line.strip(' ')
        string = string.split(':')
        if (string[0] == '\"class\"'):
            if (string[1].strip(' ') == '\"sedancars\"\n' or string[1].strip(' ') == '\"suvcarscars\"\n'):
                counter += 1

    print counter

machine_function(os.path.join(path, '.\\pics\\cars.jpg'))


