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

run_commands = {
    # word used
    "time": "time.rb",
    "example": "bash_plugin.sh"
}


system_call = {
    "rb": "ruby",
    "sh": "bash",
    "py": "python",
}



def start_plugin(filename):
  """
    In charge of starting plugins Plugins are implemented as services.
  """
  extension = filename.split(".")[-1]
  print "The file extension of the plugin is " + extension
  relative_path = "plugins/" + filename
  file_path = os.path.join(os.path.abspath(sys.path[0]), relative_path)
  plugin = environment.system.run_service([system_call[extension], file_path])
  output = plugin.communicate()[0]
  # TODO add a plugin manager function that interfaces with the plugin through stdin and stdout.
  return str(output)


def open_plugin(noun):
  """
    Fetches filename to and passes it to start_plugin().
  """
  if noun in run_commands.keys():
    return start_plugin(run_commands[noun])
  else:
    return "I can't find a plugin for " + noun