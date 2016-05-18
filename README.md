A json parser which builds a python-transitions based chat bot

A quick example. See the json below

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

![Alt text](stateexample.png?raw=true "State Diagram")


INSTALL
-------

sudo apt-get update  
sudo apt-get install git python-setuptools  
git clone https://github.com/debayan/transitions.git  
cd transitions/  
sudo python setup.py install  
cd ../  
git clone https://github.com/debayan/jatayu.git  
cd jatayu/chat-transitions  
./parse.py doc.json  

