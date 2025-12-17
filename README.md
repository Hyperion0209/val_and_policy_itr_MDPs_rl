# val_and_policy_itr_MDPs_rl
Value Iteration and Howard’s Policy Iteration of Markov Decision Problems 
Based on the setup as defined on [https://www.cse.iitb.ac.in/~shivaram/teaching/old/cs747-a2023/pa-2/pa-2.html]

# Adversarial MDP Planning Toolkit

A compact research-oriented toolkit for generating Markov Decision Processes (MDPs), solving them with multiple planning algorithms, and encoding/decoding structured game-like environments into the MDP interface.

The codebase is designed for experimentation with dynamic programming and linear programming formulations of planning, and for integrating external “opponent models” into MDP-based decision making. [file:11][file:14]

---

## Project Overview

This repository provides:

- **MDP Generator** – Random episodic and continuing MDPs with configurable state/action counts and discount factor, output in the standard `numStates/numActions/transition/...` text format. [file:14]  
- **Generic MDP Planner** – A unified solver supporting **Value Iteration (VI)**, **Howard’s Policy Iteration (HPI)**, and **LP-based planning**, all exposed via a single CLI. [file:11]  
- **Environment Encoder** – Translates a structured opponent/environment description into an MDP by constructing state mappings, transition kernels, and rewards using controllable parameters \(p, q\). [file:13]  
- **Policy Decoder** – Maps a value/policy file back into human-readable state–action–next-state triples given an opponent description. [file:12]  

This makes it easy to (1) synthesize MDPs, (2) solve them with classical algorithms, and (3) interpret policies in the original task’s symbolic state space.

---

## File Structure
```
.
├── generateMDP.py # Random MDP generator (episodic or continuing)​
├── planner.py # LP, Value Iteration, Howard Policy Iteration solvers​
├── encoder.py # Opponent/environment → MDP encoder​
├── decoder.py # Policy/value → interpretable transitions decoder​
├── create_venv.sh # Helper to create a Python 3.8 virtualenv​
└── requirements.txt # Python dependencies (pulp, numpy, etc.)
```


---

## Installation

From the project root:

1. Create and activate a virtual environment (Python 3.8 recommended)
bash create_venv.sh
source env747/bin/activate # or the name you entered in the script

2. Install dependencies
pip install -r requirements.txt

text

`requirements.txt` includes `numpy` and `pulp` for numerical computation and linear programming. [file:11][file:13][file:15]

---

## Usage

### 1. Generate an MDP

Create either a **continuing** or **episodic** MDP with configurable size:

Continuing MDP with 50 states, 20 actions, gamma=0.9, seed=42
python generateMDP.py --S 50 --A 20 --gamma 0.9 --mdptype continuing --rseed 42 > mdp-50-20.txt

Episodic MDP with 30 states, 10 actions
python generateMDP.py --S 30 --A 10 --gamma 0.99 --mdptype episodic --rseed 7 > episodic-mdp.txt

The generator prints an MDP in the standard textual format with `numStates`, `numActions`, `transition`, `end`, `mdptype`, and `discount` entries. [file:14]

---

### 2. Solve an MDP

Run **Value Iteration**, **LP**, or **Howard Policy Iteration** on a given MDP file:

Value Iteration (default)
```
python planner.py --mdp mdp-50-20.txt --algorithm vi
```
Linear Programming formulation
```
python planner.py --mdp mdp-50-20.txt --algorithm lp
```
Howard Policy Iteration
```
python planner.py --mdp mdp-50-20.txt --algorithm hpi
```

Output format: each line is
```
<value> <action>
```

where `<value>` is the optimal value of the state and `<action>` is the optimal action index. [file:11]

#### Evaluating a Fixed Policy

Given an MDP and a policy file, compute the value function of that policy:
```
python planner.py --mdp mdp-50-20.txt --algorithm vi --policy policy.txt
```

`policy.txt` should contain one action index per line (one per state). The planner solves the linear system \(V^\pi = R^\pi + \gamma P^\pi V^\pi\) and prints the corresponding values and actions. [file:11]

---

### 3. Encode a Structured Environment as an MDP

`encoder.py` reads an **opponent description** (e.g., a structured game state file) and converts it into an MDP specification with transition probabilities derived from parameters \(p\) and \(q\). [file:13]
```
python encoder.py --opponent opponent-spec.txt --p 0.4 --q 0.6 > encoded-mdp.txt
```

- `--opponent`: path to the environment/opponent text file. [file:13]  
- `--p`, `--q`: control success/failure probabilities of key actions (e.g., moving with/without ball in a grid game). [file:13]

The encoder builds a state index mapping, iterates over all states and actions, and emits transitions consistent with the dynamics implied by the opponent probabilities. 

You can then directly feed `encoded-mdp.txt` into `planner.py`:
```
python planner.py --mdp encoded-mdp.txt --algorithm vi > encoded-policy.txt
```

---

### 4. Decode a Policy Back to Human-Readable Form

`decoder.py` takes a **value/policy output** and the original opponent description and prints interpretable `(state, action, next_state)` tuples. [file:12]
```
python decoder.py
--value-policy encoded-policy.txt
--opponent opponent-spec.txt
```

For each original symbolic state, the decoder uses the state mapping and the chosen actions to print which next-state distribution or specific transition corresponds to the policy. [file:12]

---

## Algorithms and Methods

- **Value Iteration:** Fixed-point iteration on the Bellman optimality operator, with a tight convergence tolerance and hard iteration cap for numerical stability.  
- **Howard Policy Iteration:** Alternates policy evaluation (solving linear equations) and greedy policy improvement until convergence.
- **LP-based Planning:** Solves the primal linear program for discounted MDPs using `pulp`/CBC, enforcing Bellman inequalities as constraints.  
- **Random MDP Construction:** Ensures well-formed MDPs with proper normalization of transition probabilities and non-trivial terminal structure (for episodic cases).  
Please refer to report.pdf for more detailed analysis of this project.

---

## Reproducibility Tips

- All generators accept a random seed (`--rseed` on `generateMDP.py`) for exact reproducibility. [file:14]  
- The solvers are deterministic given a fixed MDP file and algorithm flag. [file:11]  

Feel free to extend the encoder/decoder to richer domains (e.g., multi-agent games, gridworlds with additional structure) or to plug in approximate solvers (e.g., function approximation or deep RL) on top of the generated MDP interfaces.
