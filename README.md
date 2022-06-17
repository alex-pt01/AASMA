

### Instructions

Our project needs python packages numpy, pygame, matplotlib and pandas to run. Packages can be installed with following command:
pip install -r requirements.txt

Our game starts running with command:
python environment.py 
or
python3 environment.py

When game starts it asks you that which agents plays the game. Options are 1. Random agent vs Q-Learning agent, 2. SARSA agent vs Q-Learning agent and 3. Random agent vs SARSA agent. You can choose which agent play by giving input 1-3. Before giving input I suggest to move the pygame window little bit up right so that when the game screen opens it is fully visible.

After giving input the game runs 100 episodes (this can be changed from variable number_of_rounds in environment.py). After two episodes, the graph begins to show how the number of steps change over time.


