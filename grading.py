import imp
import os
import json
import subprocess

grades = {
  "marks": []
}

listOfCommands = ["ip addr", "ip -4 addr", "ifconfig", "ping", "ssh", "version", "uptime", "cpuinfo", "cat", "proc"]

listOfOutputs = ['ls' ,'/mnt/remote/myApps/' ,'cd /mnt/remote/myApps/','./mount-nfs.sh','Hello embedded world, from ','Your reaction time is', 'Your reaction time was' , 'best so far in game is', 'ls /mnt/remote/myApps' ,'best so far in the game is', 'When LED3 lights up, press the USER button!', 'New best time!', 'No input within 5000ms; quitting!', './mountNFS.sh']

listOfSubmissions = "zdurani, tka74,akopylov,llagerwe,hlebumfa,sukhal,bla135,tla152,liyuyul,jml44,rmakita,asm18,cma107,jmateo,bmckeen,jmerkl,jmix,kmokaya,amontede,smoradkh,mmsaki,tnookut,zosmond,epa25,tpa35,sraisudd,drashid,drowsell,dss17,hssekhon,wshami,divyams,jkshergi,nss11,ksa170,ssa365,alons,aspeers,athapa,ktoering,ezt,dumpherv,jvanloo,swa263,cwa230,cya110,ruoyiz,jcz3"
listOfSubmissions = listOfSubmissions.split(',')

subfolders = [ f.path for f in os.scandir('./submissions/myGrading/') if f.is_dir() if f.name in listOfSubmissions ]
# print(subfolders, "\n\n\n")

subfolders = sorted(subfolders)

def gradeEstablishConnectionSection():
  for subfolder in subfolders:
    templateGrade = {
    "userid": "",
    "establish-communication": {"mark": 5.00, "comment": "Covers all/most"},
    # "nfs-and-custom-login-message": {"mark": 12.00, "comment": "Covers all"},
    # "hello": {"mark": 48.00, "comment": "Works"},
    # "good-quality-code": {"mark": 0.00, "comment": "..."}
    }
    count = 0
    print(subfolder)
    templateGrade['userid'] = subfolder.split('/')[-1]
    for command in listOfCommands:
      try:
        if command in open('{}/as1-hostViaIP.txt'.format(subfolder)).read():
          count+=1
      except FileExistsError:
        if command in open('{}/as1-hostViaIP'.format(subfolder)).read():
          count+=1
      # if 'ip addr' in open('{}/as1-hostViaIP.txt'.format(subfolder)).read():
      #   print("ip addr")
      except Exception:
        print("EXCEPTION: {}".format(subfolder.split('/')[-1]))
        templateGrade["establish-communication"]['comment'] = 'EXCEPTION'
        break
    if count >= 7:
      templateGrade["establish-communication"]['mark'] = 5
    elif count == 6:
      templateGrade["establish-communication"]['mark'] = 4.5
      templateGrade["establish-communication"]['comment'] = 'missing command'
    elif count == 5:
      templateGrade["establish-communication"]['mark'] = 4
      templateGrade["establish-communication"]['comment'] = 'missing commands'
    grades["marks"].append(templateGrade)
    
  # Serializing json
  json_object = json.dumps(grades, indent=4)
  
  # Writing to sample.json
  with open("output.json", "w") as outfile:
      outfile.write(json_object)
      
      
def gradeNFSLogin():
  for subfolder in subfolders:
    templateGrade = {
    "userid": "",
    # "establish-communication": {"mark": 5.00, "comment": "Covers all/most"},
    "nfs-and-custom-login-message": {"mark": 12.00, "comment": ""},
    # "hello": {"mark": 48.00, "comment": "Works"},
    # "good-quality-code": {"mark": 0.00, "comment": "..."}
    }
    count = 0
    templateGrade['userid'] = subfolder.split('/')[-1]
    for output in listOfOutputs:
      try:
        if output.lower() in open('{}/as1-bootTrace.txt'.format(subfolder)).read().lower():
          count+=1
        # else:
          # print("Missing {}".format(output))
      except FileExistsError:
        if output in open('{}/as1-bootTrace'.format(subfolder)).read():
          count+=1
      # if 'ip addr' in open('{}/as1-hostViaIP.txt'.format(subfolder)).read():
      #   print("ip addr")
      except Exception:
        print("EXCEPTION: {}".format(subfolder.split('/')[-1]))
        templateGrade["nfs-and-custom-login-message"]['comment'] = 'EXCEPTION'
        break
    averageOutput = count/len(listOfOutputs)
    print(subfolder, '\t' , averageOutput)
    if averageOutput >= 0.62:
      templateGrade["nfs-and-custom-login-message"]['mark'] = 12
    elif averageOutput >= 0.5:
      templateGrade["nfs-and-custom-login-message"]['mark'] = 11
      templateGrade["nfs-and-custom-login-message"]['comment'] = ''
    elif averageOutput >= 0.4:
      templateGrade["nfs-and-custom-login-message"]['mark'] = 8
      templateGrade["nfs-and-custom-login-message"]['comment'] = ''
    elif averageOutput >= 0.3:
      templateGrade["nfs-and-custom-login-message"]['mark'] = 7
      templateGrade["nfs-and-custom-login-message"]['comment'] = ''
    else:
      templateGrade["nfs-and-custom-login-message"]['mark'] = 0.0
      templateGrade["nfs-and-custom-login-message"]['comment'] = 'EXCEPTION'
    grades["marks"].append(templateGrade)
    
  # Serializing json
  json_object = json.dumps(grades, indent=4)
  
  # Writing to sample.json
  with open("output.json", "w") as outfile:
      outfile.write(json_object)

# print(subfolders)

def gradeHello():
  try:
    currentRootDir = os.getcwd()
    for subfolder in subfolders:
      os.chdir(currentRootDir)
      templateGrade = {
      "userid": "",
      # "establish-communication": {"mark": 5.00, "comment": "Covers all/most"},
      # "nfs-and-custom-login-message": {"mark": 12.00, "comment": ""},
      "hello": {"mark": 48.00, "comment": ""},
      # "good-quality-code": {"mark": 0.00, "comment": "..."}
      }
      count = 0
      templateGrade['userid'] = subfolder.split('/')[-1]
      commentForGrade = ""
      tempGradMarks = 0
      
      # Run this first time
      # command = 'cp -R {} {}'.format(subfolder,"./submissions/myGrading/")
      # os.system(command)
      
      removeHelloCommand = 'rm /home/debian/cmpt433/public/myApps/hello'
      os.system(removeHelloCommand)

      os.chdir(subfolder)
      cmd = "tar -xvf as1-helloWorld.tar.gz"
      output = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
      print(output.decode('utf-8').split())
      extractedFolder = output.decode('utf-8').split()[0]
      os.chdir(extractedFolder)
      print(os.getcwd())
      output = subprocess.Popen("make",shell=True, stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
      print(output.decode('utf-8'))
      
      # # [5]  Makefile which builds 'hello' and puts executable in public folder
      c = input("Did makefile generate hello? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+5] | "
        tempGradMarks += 5
        print("Hello -> Yes")
      else:
        commentForGrade += "hello not in myApps | "
      
      # # [3]  Displays welcome message
      c = input("Did welcome message appear? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+3] | "
        tempGradMarks += 3
        print("Hello -> Yes")
      else:
        commentForGrade += "No welcome Message | "
      
      # [5]  Light up LED 0 and wait 0.5 - 3.0s
      c = input("Did LED0 Light up? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+5] | "
        tempGradMarks += 5
        print("Hello -> Yes")
      else:
        commentForGrade += "LED0 didn't lightup | "
        
      # [10] Test user response time (turn on LED 3, start time, stop when button pressed)
      c = input("Test user response time (turn on LED 3, start time, stop when button pressed)? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+10] | "
        tempGradMarks += 10
        print("Hello -> Yes")
      else:
        commentForGrade += "Issues in User Response | "
        
      # [5]  Display summary showing current response time and best so far this run
      c = input("Display summary? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+5] | "
        tempGradMarks += 5
        print("Hello -> Yes")
      else:
        commentForGrade += "Issues in Summary | "
        
      # [5]  Repeat playing game until user exits
      c = input("Did Game Repeat? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+5] | "
        tempGradMarks += 5
        print("Hello -> Yes")
      else:
        commentForGrade += "Didn;t repeat | "
      
      # [10] Exit game if no button press within 5s
      c = input("Exited on no press in 5Seconds? Y/n").lower()
      if(c=='y'):
        commentForGrade += "[+10] | "
        tempGradMarks += 10
        print("Hello -> Yes")
      else:
        commentForGrade += "Didn't Exit | "
      
      tempGradMarks += 5
      commentForGrade += "[+5]"
      templateGrade['hello']['mark'] = tempGradMarks
      templateGrade['hello']['comment'] = commentForGrade
      grades["marks"].append(templateGrade) 
      
  except Exception as e:
    import traceback
    traceback.print_exc()
    print(e)
    # Serializing json
    json_object = json.dumps(grades, indent=4)
    
    # Writing to sample.json
    with open("hello.json", "w") as outfile:
        outfile.write(json_object)


         
      
print(len(subfolders))
gradeHello()


#     - Optional: seed random number generator (srand) by timer