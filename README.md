# alan ai

Born: 02/18/16

A smart chat bot and soon to be ai assistant written in python. The goal is to create a solid language processing unit at the core and allow users to hack alan and add "actions" for alan to complete based on verbs. 


# actions

Alan has actions that can be automatically called by imperative sentences. If you tell alan to "show me Jimi Hendrix" he will open up a picture of jimi hendrix in a web browser, "show" is the verb in this imperative. Another example is "send an email" where send is the verb.

You can easily add an action in actions/actions.py all you have to do is write a self contained python function that does something and put and entry in to the "actions dictionary" and the "pick action" dispatcher will call it if alan hears the verb. The entry needs the verb as the key and the function as the value. At the end of your function return a string as Alan's response and he will speak the string out loud. In the code below he would say "Email sent" after sending an email.

For Example:
If this is the original actions.py

***
```python

def send_email(sentence):
  #Logic to send an email
  return "Email sent."

actions_dictionary = {
  "send": send_an_email
}
  
```
***

You can add your own action by adding your function and updating the actions dictionary.
The new file would look like so:

***
```python

def send_email(sentence):
  #Logic to send an email
  return "Email sent."

def new_action_think(sentence):
  import some_stuff
  #New amazing logic
  return "I just figured out the meaning of life"
  
actions_dictionary = {
  "send": send_an_email,
  "think": new_action_think,
}
```
***
