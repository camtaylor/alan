import subprocess
import memory
import threading

"""
  This file holds helper functions for accessing system calls. One of which is starting services that run on the os.
  The functions should create or communicate with system services.
"""



try:
    from subprocess import DEVNULL # py3k
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def run_service(command):
  """
    This function can be used to start a command as a service and add it to the services list in the memory context.
    TODO add communication through piping.

    Use this or run_callback_service when you want to execute a command in the background.
   Args:
     command (String) : command you want to run for the service.
  """
  try:
    service = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # TODO give the service a name so it can be referenced later. Tuple
    memory.context.services.append(service)
    return service
  except:
    return False


def run_callback_service(callback, command):
  """
    This function is similar to run_service except for the fact that
    it can execute a function open completion of the service subprocess.

    Args:
      command (String) : command you want to run for the service
      callback (function) : function you want to execute after the service completes.


  """
  def runInThread(callback, command):
    service = subprocess.Popen(command, shell=False)
    memory.context.services.append(service)
    service.wait()
    callback(service)
    return

  thread = threading.Thread(target=runInThread, args=(callback, command))
  thread.start()
  # returns immediately after the thread starts
  return thread

def run_osa_service(app_name, command_string, params):
  """
    This function is used to run Mac Applescripts.

    Args:
     String: app_name
     String: command_string
     List: params
    
    For simple scripts where you are returning a value, use without args:
      Ex: 'tell application "Contacts" to return value of "phone" ...'

    For more complicated scripts, use params:
      Ex: 'on run {arg1, arg2} tell application "Messages" ...'

  """
  def close_application(app_name):
    osa = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
    osa.communicate('quit app "'+app_name+'"')[0]

  if len(params) < 1:
    command = str('tell application "{}" to return value of {}'.format(app_name, command_string))
    try:
      osa = subprocess.Popen(['osascript', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
      result = osa.communicate(command)[0]
      close_application(app_name)
    except:
      result=""
    return str(result)
  else:
    try:
      osa = subprocess.Popen(['osascript', '-'] +[str(arg) for arg in params], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
      result = osa.communicate(command_string)
      close_application(app_name)
    except:
      result = ""
    return str(result)

    
