import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--value-policy",type = str, help = 'path here', default = r"C:\Users\Aryan Bhosale\code\data\mdp\sol-continuing-mdp-50-20.txt")
parser.add_argument("--opponent",type = str,help = 'path', default= r"C:\Users\Aryan Bhosale\code\data\football\test-1.txt")

args = parser.parse_args()

if __name__ == "__main__":

    opponent_path = args.opponent
    #initialize an empty dictionary to store contents of the read file
    state = {}
    states_list = []
    states_mapping_dict = {}
    inv_mapping = {}
    counter = 0
    with open(opponent_path, 'r') as file:
        #reading the file line-by-line 
        for line in file:
            #split at line break
            line_components = line.strip().split()
            keywrd = line_components[0]
            if keywrd == "state":
                continue
            else:
                opp_probs = np.zeros(4)
                for i in range(1, 5):
                    opp_probs[i-1] = line_components[i]
                
                this_state = keywrd
                states_list.append(this_state)
                state[this_state] = opp_probs
                states_mapping_dict[this_state] = counter
                inv_mapping[counter] = this_state
                counter += 1

    policy_path = args.value-policy
    trnsn_fn = {}
    action = {}
    count = 0
    with open(policy_path, 'r') as file:
        #reading the file line-by-line 
        for line in file:
            #split at line break
            count+= 1
            line_components = line.strip().split()
            trnsn_fn[count] = line_components[0]
            action[count] = line_components[1]
    
    for j, t in enumerate(trnsn_fn):
        state = str(inv_mapping[j])
        transition = str(t)
        act = str(action[j]) 
        
        print(state+" "+act+" "+transition)

