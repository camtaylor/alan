"""
  This file manages the plugins and runs them in evironment.system services.
  Plugins are simply programs that communicate to alan through stdin and stdout.
  Plugins can be written in any language

  To add a plugin there are 2 steps.

  1. Add your plugin file to the plugins directory.
  2. Make an entry for it in the run commands dictionary.
    - Key is noun used to refer to the program
    - Value is the filename of the program

  Alan will spawn a service to run your plugin by saying "run **some noun"

  Example: "run time" will run the ruby code and return a time.

"""

import environment.system
import os
import sys
import alan
import threading

run_commands = {
    # word used
  "time": "time.rb",
  "echo": "echo.sh",
  "count": "count.pl",
  "stocks": "stocks.sh",
  "music": "music.osa",
  "roku": "roku.sh",
  "fibonacci": "fibonacci.cpp",
  "translator": "translator.py",
  "hello": "HelloWorld.java",
  "background": "background.sh",
  "server": "server.js"
}


system_call = {
  "rb": "ruby",
  "sh": "bash",
  "py": "python",
  "pl": "perl",
  "osa": "osascript",
  "cpp": "compile",
  "java": "compile",
  "js": "node"
}


def attach_notification_listener(plugin):
  """

  """
  while True:
    line = plugin.stdout.readline()
    if line != '':
      if ":notify:" in line:
        alan.speak(line.replace(":notify:", ""))
    else:
      break

def attach_sphinx(plugin, plugin_directory):
  """
    Function that attaches pocketsphinx_continous to a plugin and uses its keyphrase.list.
  """
  # TODO finish function and write docs. Currently works but breaks pipe if alan input is used.
  import subprocess
  import memory.context
  keyphrase_list_path = plugin_directory + "keyphrase.list"
  if os.path.isfile(keyphrase_list_path):
    print "Keyword list found. Starting pocket sphinx."
    sphinx_string = "pocketsphinx_continuous -kws " + keyphrase_list_path + " -kws_threshold 1e-1 -inmic yes -logfn /dev/null"
    print sphinx_string
    sphinx_command = sphinx_string.split()
    sphinx = subprocess.Popen(sphinx_command, stdout=plugin.stdin)
    memory.context.services.append(sphinx)


def interpret(plugin):
  """
    Function that interprets plugin data from stdin and writes to stdout.

    Args:
      plugin (subprocess.Popen object): The process running the plugin.
    Returns:
      (String) : status of the plugin

    # TODO add timeout to stop plugin if it is non responsive.
    # TODO I remember reading that stdin.write() and stdout.readline() are not ideal so they will need to be replaced.
  """
  #TODO should be migrated to a class. Also it will eventually handle many commands other than :speak: and :listen:
  while True:
    line = plugin.stdout.readline()
    if line != '':

      if ':listen:' in line:
        try:
          plugin.stdin.write(str(alan.listen()) + "\n")
        except:
          return "Exiting plugin"

      if ':speak:' in line:
        line = line.replace(":speak:", "")
        line = line.replace(":listen:", "")
        alan.speak(line)

      if ':release:' in line:
        # The plugin goes into background mode and spawns a notification_listener thread.
        background_listener = threading.Thread(target=attach_notification_listener, args=[plugin])
        background_listener.start()
        return "Plugin is now running in the background."

      else:
        print line.rstrip()

    else:
      break
  return "Finished running plugin."


def compile_and_run(file_path, filename, extension):
  """
    Function to compile and run plugins that are not interpretted languages.
  """
  # TODO replace os.system with some other call to system like subprocess.
  import os
  import time

  if extension == "cpp":
    plugin_path = file_path.replace(filename, "plugin")
    os.system("g++ {} -o {}".format(file_path, plugin_path))
    plugin = environment.system.run_service(plugin_path)
    return plugin
  elif extension == "java":
    os.system("javac {}".format(file_path))
    plugin = environment.system.run_service(["java", "-cp", file_path.replace(filename, ""), filename.split(".")[0]])
    print filename.split(".")[0]
    return plugin



def start_plugin(filename):
  """
    In charge of starting plugins Plugins are implemented as services.

    Args:
      filename (String): The filename of the plugin.
    Returns:
      (String) : Status of the plugin.
  """
  split_filename = filename.split(".")
  extension = split_filename[-1]
  directory = split_filename[0].lower()
  print "The file extension of the plugin is " + extension
  plugin_path = "plugins/" + directory
  relative_path = plugin_path + "/" + filename
  file_path = os.path.join(os.path.abspath(sys.path[0]), relative_path)
  if system_call[extension] != "compile":
    if extension == "py":
      plugin = environment.system.run_service([system_call[extension], "-u", file_path])
    else:
      plugin = environment.system.run_service([system_call[extension], file_path])
  else:
    plugin = compile_and_run(file_path, filename, extension)
  # Test if the plugin is exists.
  if plugin:
    attach_sphinx(plugin, file_path.replace(filename, ""))
    interpreter_message = interpret(plugin)
    return interpreter_message
  else:
    print file_path
    return "Plugin was not run."


def open_plugin(noun):
  """
    Fetches filename to and passes it to start_plugin().

     Args:
      noun(String): The noun used to call the plugin
      Example: "Run the time" where "time" is the noun
    Returns:
      (String) : Status of the plugin.
  """
  noun = noun.lower()
  if noun in run_commands.keys():
    return start_plugin(run_commands[noun])
  else:
    return "I can't find a plugin for " + noun

def reconnect_plugin():
  """
    Function to reconnect a plugin to the interpreter after it has been running in the background.
  """
  # TODO actually find a certain service by name rather than grabbing the 0 index from services.
  import memory.context
  if len(memory.context.services) == 0:
    return
  interpret(memory.context.services[0])