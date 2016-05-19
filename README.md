Jatayu is a framework for building chatbots. It is built on top of a modified version of the python-transitions state machine package hosted at https://github.com/tyarkoni/transitions.

Our philosophy for designing chat bots is this: all conversational modelling for chat bots should begin as a state machine diagrams on a whiteboard. For example:

![Alt text](chat-transitions/stateexample.png?raw=true "State Diagram")

Once a state transition diagram has been drawn, the developer needs to write certain function definitions to take care of validations, RPC, data base queries etc in the file Model.py. Something like this:


```python

def needsfood(self, text=None, reply=[]):
    if 'food' in text.lower():
        return True
    else:
        return False

```

The state machine diagram causes an intermediate json output as show below. This project parses this json, takes the function definitions written by a developer, and creates a chatbot.

```json
{
  "variables": ["name"],

  "states": [
    {
      "name":"begin",
      "on_enter_say": "Hi %name%, welcome to my shop."
    },
    {
      "name":"serve_food",
      "on_enter_say": "Here is your food."
    },
    {
      "name": "serve_drinks",
      "on_enter_say": "Here is your drink."
    }

  ],
  "transitions": [
    ["begin", "serve_food", ["needsfood", "!needsdrink"]],
    ["begin", "serve_drinks", ["!needsfood", "needsdrinks"]]
  ]
}
```


The above json has 3 states, each has a name. On entering each state something is said to the user as mentioned in the "on_enter_say" field.  
The transitions array mentions two possible transitions. The first field in a transition array member is the beginning state, the second field is the final state, and the third field is an array of function names which must conditionally be true (or false, if there is a ! at the beginning) for the transition to happen.



INSTALL
-------

sudo apt-get update  
sudo apt-get install git python-setuptools  
git clone https://github.com/debayan/transitions.git  
cd transitions/  
sudo python setup.py install  
cd ../  
git clone https://github.com/debayan/jatayu.git  


USAGE
-----

cd jatayu/chat-transitions  
./parse.py recipe1.json    -> This command currently allows you tot chat with your bot on the command line. No internet hookups have been done yet.  
A working example can be understood by looking at recipe1.json and Model.py.  
You may also look at parse.py to look at the framework details.

