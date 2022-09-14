import os
import subprocess
import shutil
import datetime

apps = "apps"
config1 = "configs/fuzzer1.properties"
config2 = "configs/fuzzer2.properties"
config3 = "configs/fuzzer3.properties"

jacocoReport = "gradlew jacocoTestReport"

command1_monkey = "gradlew clean startMonkey --events=\"500\" --throttle=\"200\" --epochs=\"3\" --config=\"" + config1 + "\""
command2_monkey = "gradlew.bat clean startMonkey --events=\"2500\" --throttle=\"200\" --epochs=\"3\" --config=\"" + config2 + "\""
command3_monkey = "gradlew.bat clean startMonkey --events=\"2500\" --throttle=\"200\" --epochs=\"100\" --config=\"" + config3 + "\""

command1 = "gradlew clean startBaristaFuzzer --events=\"500\" --throttle=\"200\" --epochs=\"3\" --config=\"" + config1 + "\""
command2 = "gradlew.bat clean startBaristaFuzzer --events=\"2500\" --throttle=\"200\" --epochs=\"3\" --config=\"" + config2 + "\""
command3 = "gradlew.bat clean startBaristaFuzzer --events=\"2500\" --throttle=\"200\" --epochs=\"100\" --config=\"" + config3 + "\""

commands = [command1, command1_monkey, command1_monkey]

logfile = open("logfile.log", "w")

logfile.write("Walked to apps\n")
logfile.flush()
dirs = os.listdir('.')

if not (os.path.isdir('reports')):
    os.mkdir("reports")
    os.mkdir("reports/ctx-30")
    os.mkdir("reports/ctx-100")
    os.mkdir("reports/mnk-30")
    os.mkdir("reports/mnk-100")

path = os.getcwd() + '/reports'
#print(pathToCopy)

t = 18

for y in commands:
    #p = subprocess.Popen(installDebug, shell=True, universal_newlines=True, stdout=logfile)
    #ret_code = p.wait()
    print("Executing command " +  y + " for app \n")
    logfile.write("Executing command " + y + " for app \n")
    logfile.flush()
    p = subprocess.Popen(y, shell=True, universal_newlines=True, stdout=logfile)
    ret_code = p.wait()
    logfile.flush()

    print(os.getcwd())

    p = subprocess.Popen(jacocoReport, shell=True, universal_newlines=True, stdout=logfile)
    ret_code = p.wait()
    logfile.flush()

    for root, dirs, files in os.walk('.', topdown = True):
        for name in list(set(dirs)):

            if name == 'build':
                print(os.getcwd())
                os.chdir(os.path.join(root, name))
                nested = os.listdir()
                if 'reports' in nested:
                    os.chdir('reports')
                    os.chdir('jacoco')
                    os.chdir('jacocoTestReport')
                    fname = ""
                    if t <= 10:
                        number = t % 10
                        fname = "run" + str(number)
                        pathToCopy = path + '/ctx-30'
#                         os.mkdir(os.path.join(pathToCopy, fname))
                    elif 10 < t <= 20:
                        number = t % 10
                        fname = "run" + str(number)
                        pathToCopy = path + '/mnk-30'
#                         os.mkdir(os.path.join(pathToCopy, fname))
                    elif 20 < t <= 25:
                        number = t % 5
                        fname = "run" + str(number)
                        pathToCopy = path + '/ctx-100'
                    else:
                        number = t % 5
                        fname = "run" + str(number)
                        pathToCopy = path + '/mnk-100'
                    t += 1
#                     time = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + fname
                    os.mkdir(os.path.join(pathToCopy, fname))
                    for item in os.listdir(os.getcwd()):
                        s = os.path.join(os.getcwd(), item)
                        d = os.path.join(pathToCopy + "/" + fname, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d, False, None)
                        else:
                            shutil.copy2(s, d)
                
    os.chdir('../../../../..')
        