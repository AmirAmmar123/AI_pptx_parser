import subprocess
import time

#TODO add cleaner.py, clean the directories every 10 minutes 
def start_process(command):
    return subprocess.Popen(command, shell=True)

if __name__ == "__main__":

    api_process = start_process("python app.py")
    explainer_process = start_process("python ../explainer/explainer.py")
  

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        api_process.terminate()
        explainer_process.terminate()
