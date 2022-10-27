import os
from tkinter import EXCEPTION
import json

grades = {
  "marks": []
}

listOfCommands = ["ip addr", "ip -4 addr", "ifconfig", "ping", "ssh", "version", "uptime", "cpuinfo", "cat", "proc"]

listOfOutputs = ['ls' ,'/mnt/remote/myApps/' ,'cd /mnt/remote/myApps/','./mount-nfs.sh','Hello embedded world, from ','Your reaction time is', 'Your reaction time was' , 'best so far in game is', 'ls /mnt/remote/myApps' ,'best so far in the game is', 'When LED3 lights up, press the USER button!', 'New best time!', 'No input within 5000ms; quitting!', './mountNFS.sh']

listOfSubmissions = "zdurani, tka74,akopylov,llagerwe,hlebumfa,sukhal,bla135,tla152,liyuyul,jml44,rmakita,asm18,cma107,jmateo,bmckeen,jmerkl,jmix,kmokaya,amontede,smoradkh,mmsaki,tnookut,zosmond,epa25,tpa35,sraisudd,drashid,drowsell,dss17,hssekhon,wshami,divyams,jkshergi,nss11,ksa170,ssa365,alons,aspeers,athapa,ktoering,ezt,dumpherv,jvanloo,swa263,cwa230,cya110,ruoyiz,jcz3"
listOfSubmissions = listOfSubmissions.split(',')

subfolders = [ f.path for f in os.scandir('./submissions/') if f.is_dir() if f.name in listOfSubmissions ]
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
      
gradeNFSLogin()