import paramiko
import base64
import json
import os
import subprocess
import traceback
import sys
import signal
from gradingDictTemplate import Assignment_Max_Grade_Template

finalGradesDictionary = {'marks': []}

ROOT_PATH = os.getcwd()


def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  print("\n"*4, "Exiting\n", finalGradesDictionary)
  saveGradesToJson(finalGradesDictionary)
  sys.exit(0)


def saveGradesToJsonTest(gradesDictionary):
  a = input("\n\n\t\t***************  Do you want to Save Grades??? [Y/N] : ")
  if a.lower() == 'n':
    sys.exit(0)
  print(gradesDictionary)
  with open('{}/firstGrading.json'.format(ROOT_PATH), 'a') as f:
    f.write(json.dumps(gradesDictionary, indent=4))


def saveGradesToJson(gradesDictionary):
  a = input("\n\n\t\t***************  Do you want to Save Grades??? [Y/N] : ")
  if a.lower() == 'n':
    sys.exit(0)
  print(gradesDictionary)
  with open('{}/firstGrading.json'.format(ROOT_PATH), 'w') as f:
    f.write(json.dumps(gradesDictionary, indent=4))


signal.signal(signal.SIGINT, signal_handler)

beagleBoneSSHClient = None


def setupPinsOnBeagleBone():
  configurePinsCommand = "ssh -i ~/.ssh/beagle -t debian@192.168.7.2 << pinConfigCommands.txt"
  output = subprocess.Popen(configurePinsCommand, shell=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.read()
  print("CONFIG PIN COMMAND OUTPUT : {}".format(output.decode('utf-8')))


setupPinsOnBeagleBone()


def connectToBeagleBone():
  global beagleBoneSSHClient
  ###################################! Connecting Through SSH !###################################
  # Replace "SSHpublicKeyForBeagleBone" with your publicKey
  SSHpublicKeyForBeagleBone = b'AAAAB3NzaC1yc2EAAAADAQABAAACAQDrIp1zwciNWp4XblCjtCs1Kfkz0O61Jo7T5kU37n65+s9fNcxf5va1/is94w9khBlA5QEZyIIF5Av+qWeTjjdonk/+xYrOMHOF0q5aand8DwJkdMNE08CfF9ga+aaEvFp8BFPZR90fuuUjbL7BuVuulipWce9LVYxo6cVPQ9YpOG2Q+G68fOZFcEc4xg1WCmoLs+cC49v8JWxYojUlW0hI1LrZ85fCOXbOr/SLnDpnJUpS7IPDuKKBI3AM7PLDbO2mKbnh0CTN0c+rLQVsOV0vHs0pcW3Vq5JGG+6svTEG5RxZVVOkjxTVsXIE6lwC0TpJ86JTzf0Ez3cEY0HYkiVZivOubDcrQ2AJMoCj53zG3FQpdePF4GMQwMBIPQup5ImQCP4xETY6w1PexYUuKFsjLULCA/5IDMFZIaPnRYwcFuR9XlRWCK/Lk7P7k8IHoVDE7zX7u70DoWZ5+X1JZO0HiAYaj8MT9KmR3nkza+cNepQGOFnxWg+eOzK72A7cx5Q8J9oGox0jxP984HhxElDLYAaTiIcP9N4peI9kBSTAm7UaYP6ugTEB/nzRsZL/TikEfjKLlvfVl5Ge3I6WT0Dpc5LQyYP5EzCdNS/GIapGoqRI14Rk3HmU45/Q8dMnn0cvyhZRJPWlBq+ywFBXNcLQYWA5mg5AAdKnfUmKY3CTgQ=='

  key = paramiko.RSAKey(data=base64.b64decode(SSHpublicKeyForBeagleBone))

  beagleBoneSSHClient = paramiko.SSHClient()

  host_keys = beagleBoneSSHClient.get_host_keys()
  host_keys.add('ssh.example.com', 'ssh-rsa', key)

  beagleBoneSSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  beagleBoneSSHClient.connect(hostname='192.168.7.2', username='debian', password='temppwd')


def runThisCommandOnBeagleBone(mySSHClient, command):
  # Returns stdin, stdout, stderr
  return mySSHClient.exec_command(command)


###################################!  Getting All Submission Directory Paths !###################################

connectToBeagleBone()
remoteSubmissionDirectory = "~/A2_Script/submissions"
allSubmissionsWithFullPathSorted = []
totalNumberOfsubmissionCount = 0

commandToGetAllFilesStrtingWithG = 'find {} -name "g-*"'.format(remoteSubmissionDirectory)
stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, commandToGetAllFilesStrtingWithG)

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

    deleteAllFilesFrommyAppsDirectoryCommand = "rm -rf ~/cmpt433/public/myApps/*"
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, deleteAllFilesFrommyAppsDirectoryCommand)
    stdout = stdout.read()
    deleteAllFilesFrommyAppsDirectoryCommandOutput = stdout.decode('utf-8')

    getFiles = "find {} -maxdepth 1 -name '*.tgz'".format(allSubmissionsWithFullPathSorted[i])
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, getFiles)
    grepedFolder = stdout.read().decode('utf-8')

    extractTGZCommand = "tar -zxvf {}".format(grepedFolder)
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, extractTGZCommand)
    stdout = stdout.read()
    extractedFolder = stdout.decode('utf-8').split()[0].strip()
    finalSubmissionDirectory = "{}/{}".format(allSubmissionsWithFullPathSorted[i], extractedFolder)
    print("\tSubmission Directory: \n\t{}".format(finalSubmissionDirectory))

    cleanCommand = "cd {} && make clean".format(finalSubmissionDirectory)
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, cleanCommand)
    stdout = stdout.read()
    cleanCommandOutput = stdout.decode('utf-8')
    print("\tClean-Command Output: {}".format(cleanCommandOutput))

    makeCommand = "cd {} && make".format(finalSubmissionDirectory)
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, makeCommand)
    stdout = stdout.read()
    makeCommandOutput = stdout.decode('utf-8')
    print("\tMake-Command Output: {}".format(makeCommandOutput))

    checkIfExecutableIsPresentOrNotCommand = "ls -l ~/cmpt433/public/myApps | egrep -c '^-'"
    stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, checkIfExecutableIsPresentOrNotCommand)
    stdout = stdout.read()
    checkIfExecutableIsPresentOrNotCommandOutput = stdout.decode('utf-8')
    print("\tNumber of files in '~/cmpt433/public/myApps' : {}".format(checkIfExecutableIsPresentOrNotCommandOutput))
    if(checkIfExecutableIsPresentOrNotCommandOutput != 1):
      print("\tExecutable in Proper Place | ", end='')
      getExecutableFileNameCommand = "basename -a ~/cmpt433/public/myApps/*"
      stdin, stdout, stderr = runThisCommandOnBeagleBone(beagleBoneSSHClient, getExecutableFileNameCommand)
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
        saveGradesToJsonTest(finalGradesDictionary)
        break

      except ValueError:
        print("\n\n\t\t\t!!!!!!!!   TRY AGAIN   !!!!!!!!")
        continue
    beagleBoneSSHClient.close()
    rebootCommand = "ssh -t debian@192.168.7.2 'sudo reboot'"
    output = subprocess.Popen(rebootCommand, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT).stdout.read()
    print(output.decode('utf-8'))
    inputCommand = ''
    while(inputCommand.lower() != 'y'):
      inputCommand = input(
          "LAST Submission: {}\n\t!!WAIT FOR BEAGLEBONE TO REBOOT!! \n\tDid beaglebone rebooted?:? [Y/N]".format(finalSubmissionDirectory)).lower()
except Exception:
  saveGradesToJson(finalGradesDictionary)
  traceback.print_exc()
finally:
  saveGradesToJson(finalGradesDictionary)
  beagleBoneSSHClient.close()


saveGradesToJson(finalGradesDictionary)
