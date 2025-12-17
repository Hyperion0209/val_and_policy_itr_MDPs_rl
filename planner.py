import numpy as np
import pulp as p
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--mdp",type = str, help = 'path here', default = r"C:\Users\Aryan Bhosale\code\data\mdp\episodic-mdp-50-20.txt")
parser.add_argument("--algorithm",type = str,help = 'solver here', default= "vi")
parser.add_argument("--policy",type = str,help = 'calc val fn for policy', default="nothing")

args = parser.parse_args()

def bellman_rhs(mdp, val, stat, act):
    return mdp['transitions'][stat, act]*(mdp['rewards'][stat, act] + mdp['discount']*val)

def bellman_rhs_arr(mdp, val_arr):
    return mdp['transitions']*(mdp['rewards'] + mdp['discount']*val_arr)

def diff_tol(val_t, val_t1, n_iters):
    if n_iters == 0:
        return True
    
    return np.max(np.abs(val_t1-val_t)) > 1e-9

def output_format(values, policy):

    for j in range(len(values)):
        val= str(values[j])
        pol = str(policy[j])
        print(val+" "+pol)
    
    return

def find_val_fn(mdp, pol):
    t = np.zeros((mdp['n_states'], mdp['n_states']))
    r = np.zeros((mdp['n_states'], mdp['n_states']))

    for state in range(mdp['n_states']):
        action = int(pol[state])
        
        t[state] = mdp['transitions'][state, action]
        r[state] = mdp['rewards'][state, action]

    mul = np.sum(np.multiply(t, r), axis = 1)

    calc_val_fn = np.linalg.solve(np.identity(mdp['n_states'])-mdp['discount'] *t, mul)
    return calc_val_fn


class solver():
    def __init__(self, mdp, which_one):
        self.mdp = mdp
        if which_one == "lp":
            self.val_fn, self.policy = self.lp_solve(self.mdp)

        elif which_one == "vi":
            self.val_fn, self.policy = self.val_iter(self.mdp)
        
        elif which_one == "hpi":
            self.val_fn, self.policy = self.howrd_iter(self.mdp)
        
        output_format(values=self.val_fn, policy=self.policy)
        
    def lp_solve(self, mdp):
        self.mdp = mdp
        self.problem = p.LpProblem("MDP_Problem", p.LpMinimize)
        val = np.array(list(p.LpVariable.dicts("val", [i for i in range(self.mdp['n_states'])]).values()))
        self.problem += p.lpSum(val)
        for state in range(self.mdp['n_states']):
            for action in range(self.mdp['n_acts']):
                self.problem += val[state] >= p.lpSum(bellman_rhs(self.mdp, val, stat=state , act=action))

        self.problem.solve(p.apis.PULP_CBC_CMD(msg=0))

        vals_list = list(map(p.value, val))
        vals_arr = np.array(vals_list)
        sum_vals = np.sum(bellman_rhs_arr(self.mdp, val_arr=vals_arr), axis = -1)
    
        policy = np.argmax(sum_vals, axis = -1)

        return vals_arr, policy
    
    def howrd_iter(self, mdp):
        self.mdp = mdp
        pol_pi = np.zeros(self.mdp['n_states'])
        pol_pi_1 = np.zeros(self.mdp['n_states'])
        val_fn = np.zeros(self.mdp['n_states'])

        while (1):
            val_fn = find_val_fn(self.mdp, pol=pol_pi)
            sum_vals = np.sum(bellman_rhs_arr(self.mdp, val_arr=val_fn), axis = -1)
            pol_pi_1 = np.argmax(sum_vals, axis = -1)

            if np.array_equal(pol_pi, pol_pi_1):
                break

            else:
                pol_pi = pol_pi_1

        # print(pol_pi_1)
        # print(val_fn)
        return val_fn, pol_pi_1

        


    def val_iter(self, mdp):
        self.mdp = mdp
        val_t = np.zeros(self.mdp['n_states'])
        val_t1 = np.zeros(self.mdp['n_states'])
        n_iters = 0
        while diff_tol(val_t, val_t1, n_iters) and n_iters<5000000:
            n_iters += 1
            val_t = val_t1
            val_t1 = np.max(np.sum(bellman_rhs_arr(self.mdp, val_arr=val_t), axis = -1), axis = -1)

        val_pol = np.argmax(np.sum(bellman_rhs_arr(self.mdp, val_arr=val_t1), axis = -1), axis = -1)

        return val_t1, val_pol










if __name__ == "__main__":
    

    file_path = args.mdp
    #initialize an empty dictionary to store contents of the read file
    trnsn_fn = {}
    rew_fn = {}

    with open(file_path, 'r') as file:
        #reading the file line-by-line 
        for line in file:
            #split at line break
            line_components = line.strip().split()
            keywrd = line_components[0]
            if keywrd == "numStates":
                n_states = int(line_components[1])
            elif keywrd == "numActions":
                n_acts = int(line_components[1])
            elif keywrd == "end":
                sink = line_components[1]
                trnsn_fn = np.zeros((n_states, n_acts, n_states))
                rew_fn = np.zeros((n_states, n_acts, n_states))

            elif keywrd == "transition":
                s, a, s_next, r, prob = map(float, line_components[1:])
                trnsn_fn[int(s),int(a),int(s_next)] = prob
                rew_fn[int(s),int(a),int(s_next)] = r
            elif keywrd == "mdptype":
                mdptype = line_components[1]
            elif keywrd == "discount":
                discount = float(line_components[1])




    mdp = {
    'n_states': n_states,
    'n_acts': n_acts,
    'sink': sink,
    'transitions': trnsn_fn,
    'rewards': rew_fn,
    'mdptype': mdptype,
    'discount': discount,
    }
    if args.policy == "nothing":
        start = time.time()
        solver(mdp, args.algorithm)
        end = time.time()
        # print(end-start)
        elapsed_time = end-start

        # print(f"Execution time: {elapsed_time:.4f} seconds")
    else:
        pol_file = args.policy
        # print(args.policy)
        policy = np.zeros(mdp['n_states'])
        with open(pol_file, 'r') as file:
        #reading the file line-by-line 
            for i, line in enumerate(file):
                line_components = line.strip().split()
                # print(line_components)
                action = line_components[0]
                # print(action)
                policy[i] = int(action)
        #print(policy)
        values = find_val_fn(mdp=mdp, pol=policy)
        output_format(values=values, policy=policy)

    

    # problem = pulp.LpProblem("pron_ex", pulp.LpMinimize)
    # problem+= x+y>=1
    # problem += y-x
    # status = problem.solve()  
    # print(pulp.value(y))