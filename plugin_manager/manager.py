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

run_commands = {
    # word used
  "time": "time.rb",
  "echo": "echo.sh",
  "count": "count.pl",
  "stocks": "stocks.sh",
  "music": "music.osa",
  "roku": "roku.sh"
}


system_call = {
  "rb": "ruby",
  "sh": "bash",
  "py": "python",
  "pl": "perl",
  "osa": "osascript",
}


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
      plugin (subprocess.Popen): The process running the plugin.
    Returns:
      (String) : status of the plugin

    # TODO add timeout to stop plugin if it is non responsive.
    # TODO I remember reading that stdin.write() and stdout.readline() are not ideal so they will need to be replaced.
  """
  while True:
    line = plugin.stdout.readline()
    if line != '':
      # the real code does filtering here

      if ':listen:' in line:
        try:
          plugin.stdin.write(alan.listen() + "\n")
        except:
          return "Exiting plugin"
      if ':speak:' in line:
        line = line.replace(":speak:", "")
        line = line.replace(":listen:", "")
        alan.speak(line)
      else:
        print line.rstrip()
    else:
      break
  return "Finished running plugin."


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
  directory = split_filename[0]
  print "The file extension of the plugin is " + extension
  plugin_path = "plugins/" + directory
  relative_path = plugin_path + "/" + filename
  file_path = os.path.join(os.path.abspath(sys.path[0]), relative_path)
  plugin = environment.system.run_service([system_call[extension], file_path])
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