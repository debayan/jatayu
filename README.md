Jatayu is a framework for building chatbots. 

It is our view that you should start building chatbots by first drawing a state diagram (or a flowchart) on a whiteboard. Something like this:  

![Alt text](diagrams/stateexample.png?raw=true "State Diagram")  

In future versions we shall have a web UI tool where drawing the above diagram will automatically generate the following JSON:  

```json
{
	"variables": ["name"],
	"states": [
	{
		"name": "begin",
		"on_enter_say": "Hi {{name}}, welcome to my shop."
	}, 
	{
		"name": "serve_food ",
		"on_enter_say": "Here is your food."
	}, 
	{
		"name": "serve_drinks",
		"on_enter_say": "Here is your drink."
	}
	],
	"transitions": [
		["begin", "serve_food", ["needs_food", "!needs_drinks"]],
		["begin", "serve_drinks", ["needs_drinks", "!needs_food"]]
	]
}
```  

The json file above needs to be saved as a "recipe" in **recipes/** folder.

Once the recipe file above has been written, you need to write certain function definitions to take care of validations, RPC, data base queries, string matching etc in a file in botmodule/ directory. Something like this:

```python

def needs_food(self, text=None, reply=[]):
    if 'food' in text.lower():
        return True
    else:
        return False

```
You need to save the above code in a file in the **botmodules/** folder. Look at the existing sample code, or read the **Sample Usage** section below to find out more about this.  
We currently only support python, but have plans of including node.js and golang.

Essentially, this is all you need to do to create a chatbot with jatayu.  We currently support telegram and facebook out of the box.

INSTALL
-------

*sudo apt-get update*  
*sudo apt-get install git python-setuptools*  
*git clone https://github.com/debayan/transitions.git*  
*cd transitions/*  
*sudo python setup.py install*  
*cd ../*  
*git clone https://github.com/debayan/jatayu.git*  


SAMPLE USAGE
------------  

The repository contains a fairly complicated working example for a bot that does mobile topups for you.  Look at **recipes/topuprecipe.json**. Also look at the model file in **botmodules/TopupModel.py**. To see this sample in action run the following command:  

**python serve.py telegram config/config.ini recipes/topuprecipe.json TopupModel --cli**  

This will allow you to chat with the bot on the command line. When the flag **--cli** is used, the options **telegram** and **config/config.ini** are ignored.

The first option of serve.py can either be **telegram** or **facebook**.  
The second option is a path to a config file of the following format:  

```python
[facebook]
access_token=<token>
[telegram]
access_token=<token>
```
It contains access tokens to the chat network.  
The third option is the path to the json recipe file.  
The fourth option is the name of the bot module python definition file/class. Both the file and the class names must be the same.

COPYRIGHT
---------

This code is being distributed under GPLv3 license, and the copyright holders are Debayan Banerjee and Shreyank Gupta.



