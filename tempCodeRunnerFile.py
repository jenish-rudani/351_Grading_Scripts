
# Assignment_Max_Grade_Template = {
#     "group": "g-grouptwo",
#     "debug-noworky-2": {"mark": 0.00, "comment": ""},
#     "designstyle-2": {"mark": 0.00, "comment": ""},
#     "joystick-and-8x8-matrix": {"mark": 0.00, "comment": ""},
#     "sampling-2": {"mark": 0.00, "comment": ""},
#     "dip-detection-2": {"mark": 0.00, "comment": ""},
#     "output-terminal-matrix": {"mark": 0.00, "comment": ""},
#     "other": {"mark": .00, "comment": ""},
#     "late_percent": 0.0,
#     "mark_penalty": 0.0,
#     "mark_penalty_reason": "",
#     "overall_comment": ""
# }


# ROOT_PATH = os.getcwd()
# ROOT_PATH = "/home/debian/A2_Script/submissions"
# submissionPath = "{}/submissions/".format(ROOT_PATH)
# print(submissionPath)
# listOfSumbissions = sorted([f.path for f in os.scandir(submissionPath) if f.is_dir()])
# # os.getcwd()
# print("\n"*3)

# try:
#   for i in range(len(listOfSumbissions)):
#     groupId = listOfSumbissions[i].split('/')[-1]

#     Assignment_Max_Grade = {
#         "group": "g-grouptwo",
#         "debug-noworky-2": {"mark": 0.00, "comment": ""},
#         "designstyle-2": {"mark": 0.00, "comment": ""},
#         "joystick-and-8x8-matrix": {"mark": 0.00, "comment": ""},
#         "sampling-2": {"mark": 0.00, "comment": ""},
#         "dip-detection-2": {"mark": 0.00, "comment": ""},
#         "output-terminal-matrix": {"mark": 0.00, "comment": ""},
#         "other": {"mark": .00, "comment": ""},
#         "late_percent": 0.0,
#         "mark_penalty": 0.0,
#         "mark_penalty_reason": "",
#         "overall_comment": ""
#     }
#     os.chdir(listOfSumbissions[i])
#     currentDir = (os.getcwd())
#     # print(currentDir)

#     getFiles = "grep -irn '' --include '*.tgz'"
#     outputOfGetFiles = subprocess.Popen(getFiles, shell=True, stdout=subprocess.PIPE,
#                                         stderr=subprocess.STDOUT).stdout.read()
#     grepedFolder = outputOfGetFiles.decode('utf-8').split()[2]
#     # print(outputOfGetFiles.decode('utf-8').split())
#     # print("Output Folder: {}".format(grepedFolder))

#     cmd = "tar -zxvf {}".format(grepedFolder)
#     output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
#                               stderr=subprocess.STDOUT).stdout.read()
#     extractedFolder = output.decode('utf-8').split()[0]
#     # print(output.decode('utf-8').split())
#     print("Output Folder: {}".format(extractedFolder))

#     while True:
#       try:
#         print("\ncd /mnt/c/Users/jruda/OneDrive/Documents/School/TA/CMPT300/A2_Grading/submissions/{}/{}".format(groupId, extractedFolder))
#         print("\n\n\tGrading GROUP: [ {} ]".format(groupId))
#         grades = int(
#             input("\n\tGrade [ Debug noworky ] part of Code. Input [0 - 10] : "))
#         Assignment_Max_Grade["debug-noworky-2"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["debug-noworky-2"]['comment'] = inputComment

#         grades = int(input("\n\tGrade [ Design/Style ] part of Code. Input [0 - 10] : "))
#         Assignment_Max_Grade["designstyle-2"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["designstyle-2"]['comment'] = inputComment

#         grades = int(input("\n\tGrade [ joystick-and-8x8-matrix ] part of Code. Input [0 - 30] : "))
#         Assignment_Max_Grade["joystick-and-8x8-matrix"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["joystick-and-8x8-matrix"]['comment'] = inputComment

#         grades = int(input("\n\tGrade [ Sampling ] part of Code. Input [0 - 10] : "))
#         Assignment_Max_Grade["sampling-2"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["sampling-2"]['comment'] = inputComment

#         grades = int(input("\n\tGrade [ DIP DETECTION ] part of Code. Input [0 - 10] : "))
#         Assignment_Max_Grade["dip-detection-2"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["dip-detection-2"]['comment'] = inputComment

#         grades = int(
#             input("\n\tGrade [ Output (terminal & 8x8 LED Matrix) ] part of Code. Input [0 - 50] : "))
#         Assignment_Max_Grade["output-terminal-matrix"]['mark'] = grades
#         inputComment = input("\tComments? [string]: ")
#         Assignment_Max_Grade["output-terminal-matrix"]['comment'] = inputComment

#         inputComment = input("\n\nADD OVERALL COMMENT. Input [STRING] : ")
#         Assignment_Max_Grade["overall_comment"] = inputComment
#         print('\n--> ', Assignment_Max_Grade, '\n')
#         print("*"*120, '\n\n')
#         gradesDict["marks"].append(Assignment_Max_Grade)
#         break

#       except ValueError:
#         print("\n\n\t\t\t!!!!!!!!   TRY AGAIN !!!!!!!!")
#         continue

#   # print(os.getcwd())
#   # output = subprocess.Popen("make", shell=True, stdout=subprocess.PIPE,
#   #                           stderr=subprocess.STDOUT).stdout.read()
#   # print(output.decode('utf-8'))

#   # os.chdir(currentDir)
#   # print(os.getcwd())
# except Exception:
#   saveGradesToJson(gradesDict)
#   os.chdir(ROOT_PATH)
#   traceback.print_exc()
# finally:
#   saveGradesToJson(gradesDict)

# saveGradesToJson(gradesDict)
