import time
import paramiko
import base64
import json
import os
import subprocess
import traceback
import sys
import signal
from gradingDictTemplate import Assignment_Max_Grade_Template


def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  print("\n"*4, "Exiting\n", finalGradesDictionary)
  saveGradesToJson(finalGradesDictionary)
  sys.exit(0)


def saveGradesToJson(gradesDictionary):
  a = input("\n\n\t\t***************  Do you want to Save Grades??? [Y/N] : ")
  if a.lower() == 'n':
    sys.exit(0)
  print(gradesDictionary)
  with open('{}/firstGrading.json'.format(ROOT_PATH), 'w') as f:
    f.write(json.dumps(gradesDictionary, indent=4))


signal.signal(signal.SIGINT, signal_handler)


def setupPinsOnBeagleBone():
  configurePinsCommand = "ssh -i ~/.ssh/beagleBoneGreen -t debian@192.168.7.2 << pinConfigCommands.txt"
  output = subprocess.Popen(configurePinsCommand, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.read()
  print("CONFIG PIN COMMAND OUTPUT : {}".format(output.decode('utf-8')))


###################################! GLOBAL VARIABLES !###################################

finalGradesDictionary = {'marks': []}
ROOT_PATH = os.getcwd()
beagleBoneSSHClient = None

###################################! CONFIGURATIONS (NEEDS TO BE CHANGED) !###################################
# YOU NEED TO CHANGE USER NAME IN BELOW VARIABLE
pathToRSAKey = "/home/<....>/.ssh/beagleBoneGreen"  # REPLACE <....> with your username on WSL (READ README.md FILE TO KNOW MORE)
pathToRSAKey = "/home/jenish/.ssh/beagleBoneGreen"  # This is a sample of what it would look like with username

beagleBoneHostName = '192.168.7.2'
beagleBoneUserName = 'debian'
beagleBonePassword = 'temppwd'

# You need to specify where have you extracted all submissions (THIS PATH IS ON BEAGLEBONE)
remoteSubmissionDirectory = "~/A2_Script/submissions"


def connectToBeagleBone():
  global beagleBoneSSHClient
  ###################################! Connecting Through SSH !###################################
  # Replace "SSHpublicKeyForBeagleBone" with your publicKey

  key = paramiko.RSAKey.from_private_key_file(pathToRSAKey)

  beagleBoneSSHClient = paramiko.SSHClient()

  host_keys = beagleBoneSSHClient.get_host_keys()
  host_keys.add('ssh.example.com', 'ssh-rsa', key)

  beagleBoneSSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  beagleBoneSSHClient.connect(hostname=beagleBoneHostName, username=beagleBoneUserName, password=beagleBonePassword)


def runCommandOnBeagleBone(mySSHClient, command):
  # Returns stdin, stdout, stderr
  return mySSHClient.exec_command(command)


###################################!  Getting All Submission Directory Paths !###################################

connectToBeagleBone()


allSubmissionsWithFullPathSorted = []
totalNumberOfsubmissionCount = 0

commandToGetAllFilesStrtingWithG = 'find {} -name "g-*"'.format(remoteSubmissionDirectory)
stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, commandToGetAllFilesStrtingWithG)

for line in stdout:
  totalNumberOfsubmissionCount += 1
  allSubmissionsWithFullPathSorted.append(line.strip('\n'))
allSubmissionsWithFullPathSorted = sorted(allSubmissionsWithFullPathSorted)

print("Total Submissions in: '{}' is '{}'".format(remoteSubmissionDirectory, totalNumberOfsubmissionCount))

print("\n"*3)

beagleBoneSSHClient.close()

try:
  for i in range(len(allSubmissionsWithFullPathSorted)):

    connectToBeagleBone()
    setupPinsOnBeagleBone()
    groupId = allSubmissionsWithFullPathSorted[i].split('/')[-1]
    print("\n"*3, "\tGroup ID: {}\n\n".format(groupId))
    Assignment_Max_Grade = {
        "group": "g-grouptwo",
        "debug-noworky-2": {"mark": 0.00, "comment": ""},
        "designstyle-2": {"mark": 0.00, "comment": ""},
        "joystick-and-8x8-matrix": {"mark": 0.00, "comment": ""},
        "sampling-2": {"mark": 0.00, "comment": ""},
        "dip-detection-2": {"mark": 0.00, "comment": ""},
        "output-terminal-matrix": {"mark": 0.00, "comment": ""},
        "other": {"mark": .00, "comment": ""},
        "late_percent": 0.0,
        "mark_penalty": 0.0,
        "mark_penalty_reason": "",
        "overall_comment": ""
    }
    Assignment_Max_Grade["group"] = groupId
    deleteAllFilesFrommyAppsDirectoryCommand = "rm -rf ~/cmpt433/public/myApps/*"
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, deleteAllFilesFrommyAppsDirectoryCommand)
    stdout = stdout.read()
    deleteAllFilesFrommyAppsDirectoryCommandOutput = stdout.decode('utf-8')

    getFiles = "find {} -maxdepth 1 -name '*.tgz'".format(allSubmissionsWithFullPathSorted[i])
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, getFiles)
    grepedFolder = stdout.read().decode('utf-8')
    print("\tTar Folder: ", grepedFolder)

    extractTGZCommand = "cd {} && tar -zxvf {}".format(allSubmissionsWithFullPathSorted[i], grepedFolder)
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, extractTGZCommand)
    stdout = stdout.read()
    # print("Extracted File: ", stdout.decode('utf-8'))
    extractedFolder = stdout.decode('utf-8').split()[0].strip()
    finalSubmissionDirectory = "{}/{}".format(allSubmissionsWithFullPathSorted[i], extractedFolder)
    print("\tSubmission Directory: {}".format(finalSubmissionDirectory))

    cleanCommand = "cd {} && make clean".format(finalSubmissionDirectory)
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, cleanCommand)
    stdout = stdout.read()
    cleanCommandOutput = stdout.decode('utf-8')
    print("\tClean-Command Output: {}".format(cleanCommandOutput))

    makeCommand = "cd {} && make".format(finalSubmissionDirectory)
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, makeCommand)
    stdout = stdout.read()
    makeCommandOutput = stdout.decode('utf-8')
    print("\tMake-Command Output: {}".format(makeCommandOutput))

    checkIfExecutableIsPresentOrNotCommand = "ls -l ~/cmpt433/public/myApps | egrep -c '^-'"
    stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, checkIfExecutableIsPresentOrNotCommand)
    stdout = stdout.read()
    checkIfExecutableIsPresentOrNotCommandOutput = stdout.decode('utf-8')
    print("\tNumber of files in '~/cmpt433/public/myApps' : {}".format(checkIfExecutableIsPresentOrNotCommandOutput))
    if(checkIfExecutableIsPresentOrNotCommandOutput != 1):
      print("\tExecutable in Proper Place | ", end='')
      getExecutableFileNameCommand = "basename -a ~/cmpt433/public/myApps/*"
      stdin, stdout, stderr = runCommandOnBeagleBone(beagleBoneSSHClient, getExecutableFileNameCommand)
      stdout = stdout.read()
      getExecutableFileNameCommandOutput = stdout.decode('utf-8')
      print("\tExecutable Filename in '~/cmpt433/public/myApps' : {}".format(getExecutableFileNameCommandOutput))
    else:
      print("!!!! Deduct Point for not placing Executable in '~/cmpt433/public/myApps' !!!!")
      inputCommand = ''
      while(inputCommand.lower() != 'y'):
        inputCommand = input(
            "!!DO NOT PROCEED WIHOUT RUNNING EXECUTABLE!! \n\tDid you manually run executable for: {}? [Y/N]".format(finalSubmissionDirectory)).lower()

    while True:
      try:
        print("\n\n\tGrading GROUP: [ {} ]".format(groupId))
        grades = int(input("\n\tGrade [ Debug noworky ] part of Code. Input [0 - 10] : "))
        Assignment_Max_Grade["debug-noworky-2"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["debug-noworky-2"]['comment'] = inputComment

        grades = int(input("\n\tGrade [ Design/Style ] part of Code. Input [0 - 10] : "))
        Assignment_Max_Grade["designstyle-2"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["designstyle-2"]['comment'] = inputComment

        grades = int(input("\n\tGrade [ joystick-and-8x8-matrix ] part of Code. Input [0 - 30] : "))
        Assignment_Max_Grade["joystick-and-8x8-matrix"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["joystick-and-8x8-matrix"]['comment'] = inputComment

        grades = int(input("\n\tGrade [ Sampling ] part of Code. Input [0 - 10] : "))
        Assignment_Max_Grade["sampling-2"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["sampling-2"]['comment'] = inputComment

        grades = int(input("\n\tGrade [ DIP DETECTION ] part of Code. Input [0 - 10] : "))
        Assignment_Max_Grade["dip-detection-2"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["dip-detection-2"]['comment'] = inputComment

        grades = int(input("\n\tGrade [ Output (terminal & 8x8 LED Matrix) ] part of Code. Input [0 - 50] : "))
        Assignment_Max_Grade["output-terminal-matrix"]['mark'] = grades
        inputComment = input("\tComments? [string]: ")
        Assignment_Max_Grade["output-terminal-matrix"]['comment'] = inputComment

        inputComment = input("\n\nADD OVERALL COMMENT. Input [STRING] : ")
        Assignment_Max_Grade["overall_comment"] = inputComment
        print('\n--> ', Assignment_Max_Grade, '\n')
        print("*"*120, '\n\n')
        finalGradesDictionary["marks"].append(Assignment_Max_Grade)
        break

      except ValueError:
        print("\n\n\t\t\t!!!!!!!!   TRY AGAIN   !!!!!!!!")
        continue
    beagleBoneSSHClient.close()
    rebootCommand = "ssh -t debian@192.168.7.2 'sudo reboot now'"
    os.system(rebootCommand)
    # print(output.decode('utf-8'))
    inputCommand = ''
    while(inputCommand.lower() != 'y'):
      inputCommand = input(
          "LAST Submission was: {}\n\t!!WAIT FOR BEAGLEBONE TO REBOOT!! \n\tDid beaglebone rebooted?: [Y/N]".format(finalSubmissionDirectory)).lower()
      time.sleep(2)
except Exception:
  saveGradesToJson(finalGradesDictionary)
  traceback.print_exc()
finally:
  beagleBoneSSHClient.close()


saveGradesToJson(finalGradesDictionary)
