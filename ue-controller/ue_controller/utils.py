import subprocess

def start_subprocess(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def kill_subprocess(process):
    process.terminate()  # Graceful termination
    try:
        process.wait(timeout=5) 
    except subprocess.TimeoutExpired:
        process.kill()  # Forceful termination
    process.communicate()
