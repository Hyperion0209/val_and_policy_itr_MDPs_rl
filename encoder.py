import numpy as np
import pulp as p
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--opponent",type = str, help = 'path here', default = r"C:\Users\Aryan Bhosale\code\data\football\test-1.txt")
parser.add_argument("--p",type = str,help = 'p val', default= "0.5")
parser.add_argument("--q",type = str,help = 'q val', default="0.5")

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

        # print(state['0101011'])
        # print(inv_mapping)
        num_actions = 11
        p = float(args.p)
        q = float(args.q)
        success_mov_w_ball = 1 - 2*p 
        success_mov_w_o_ball = 1 - p

        for j, init_state in enumerate(states_list):
            print(j)
            # print(init_state)

            b1_pos = init_state[0:1]
            print(b1_pos)
            b2_pos = init_state[2:4]
            print(b2_pos)
            r_pos = init_state[4:6]
            print(r_pos)
            for action in range(num_actions):
                if action <4:
                    # movement
                    # with ball
                    if action == 0:
                        pass
                    
                    elif action == 1:
                        pass

                    elif action == 2:
                        pass

                    elif action == 3:
                        pass

                    # successful
                    # fail

                    # w/o ball
                elif action<8:
                    pass

                elif action == 8:
                    pass

                elif action == 9:
                    pass







    # mdp = {
    # 'n_states': n_states,
    # 'n_acts': n_acts,
    # 'sink': sink,
    # 'transitions': trnsn_fn,
    # 'rewards': rew_fn,
    # 'mdptype': mdptype,
    # 'discount': discount,
    # }