#REMEMBER TO DO DOCUMENTATION
from collections import defaultdict
from itertools import product
import copy 

class DFA():

	def __init__(self, states=set(), alphabet=set(), transition=dict(), start_state= None, accept_states=set()):

		self.states = set(states)
		self.alphabet = set(alphabet)
		self.transition = transition
		self.start_state = start_state
		self.accept_states = set(accept_states)


	def _str_transition_(self):

		string = "Transitions: state, symbol -> state"
		for state in self.transition:
			state_transitions = self.transition[state]
			for symbol in state_transitions:
				string += "\n\t" + str(state) + " , " + symbol + " -> " + str(state_transitions[symbol])
		return string

	def __repr__(self):
		return "Deterministic Finite Automata (DFA)" + f" at {hex(id(self))}"

	def __str__(self):
		str_self = (
			self.__repr__() + "\n"
			+ "States: " + f"{self.states}\n"
			+ "Symbols: " + f"{self.alphabet}\n"
			+ "Start State: " + f"{self.start_state}\n"
			+ "Accept States: " + f"{self.accept_states}\n"
			+ self._str_transition_()
			)
		return str_self

	def accepts(self, input_string):

		current_state = self.start_state
		for idx in range(len(input_string)):
			current_symbol = input_string[idx]
			current_state = self.transition[current_state][current_symbol]
		if current_state in self.accept_states:
			return True
		else:
			return False

	def DFA_Strip(self):
		ReachableStates = {self.start_state}
		NewStates = {self.start_state}

		while len(NewStates) > 0:
			TempStates = set() 
			for r in NewStates:
				for a in self.alphabet:
					TempStates = TempStates.union({self.transition[r][a]})
			NewStates = TempStates.difference(ReachableStates)
			ReachableStates = ReachableStates.union(NewStates)
		Q_Prime = ReachableStates
		F_Prime = self.accept_states.intersection(ReachableStates)
		D_Prime = self.transition

		for q in self.states.difference(Q_Prime):
			for a in self.alphabet:
				D_Prime[q].pop(a)

		return DFA(Q_Prime, self.alphabet, D_Prime, self.start_state, F_Prime)

	def DFA_Intersection(self, m2):
		Q = [(q1, q2) for q1 in self.states for q2 in m2.states]
		alphabet = self.alphabet.intersection(m2.alphabet)
		delta = dict()
		for (q1, q2) in Q:
			temp = dict()
			for a in alphabet:
				temp[a] = (self.transition[q1][a], m2.transition[q2][a])
			delta[(q1, q2)] = temp
		q0 = (self.start_state, m2.start_state)
		F = [(f1, f2) for f1 in self.accept_states for f2 in m2.accept_states]
		return DFA(Q, alphabet, delta, q0, F)

	def DFA_Complement(self):
		return DFA(self.states, self.alphabet, self.transition, self.start_state, self.states.difference(self.accept_states))

	def DFA_Minimize(self):

		"""
		Minimizes a given Deterministic Finite Automata(DFA)

		Attributes:
			states : set
				Collection of states
			alphabet : set
				Collection of symbols
			transition : dict
				Transition function of the form transition[state][symbol] = state
			start_state : str
				Initial state and an element of states
			accept_states : set
				Accepting or final states which is a subset of states
		"""

		#Removes all unreachable states from the given DFA
		self = self.DFA_Strip()

		"""
		G : defaultdict
			Contains information regarding pairwise distinguishability between
			the cartesian product of self.states with itself. A pair of states
			(q, r) are distinguishable if G[q][r] == 1

		D_Prime : defaultdict
			Transition function for the minimized DFA
		"""
		G = defaultdict(lambda: 0)
		for state in self.states:
			G[state] = defaultdict(lambda: 0)


		D_Prime = defaultdict(dict)
		for state in self.states:
			D_Prime[state] = defaultdict(str)

		"""
		We initially mark all pairs of states (q, r) = (r, q) as distinguishiable (set to 1) such that q is an element of the set of accept states and r is the set of non-accepting states.
		"""
		for (q, r) in product(self.accept_states, self.states.difference(self.accept_states)):
			G[q][r] = 1
			G[r][q] = 1

		"""
		Temp : defaultdict
			Copy of the defaultdict G to be used for the updating part of the algorithm
		"""
		Temp = copy.deepcopy(G)

		"""
		update() : function
			checks all pairs of states from the cartesian product of self.states with itself such that given two states (q, r) and q != r, mark G[q][r] = 1 (distinguishable) if the pair (self.transition[q][a], self.transition[r][a]) is distinguishable. That is, if the pair of transition states given some symbol "a" in the alphabet is distinguishable 
		"""

		def update():
			for (q, r) in product(self.states, self.states):
				if q == r: 
					continue
				for a in self.alphabet:
					if G[self.transition[q][a]][self.transition[r][a]] == 1:
						G[q][r] = 1
						G[r][q] = 1

		"""
		Initial update
		"""
		update()

		"""
		Repeatedly apply the update() function as long as a change in G occurs in the previous iteration
		"""
		while Temp != G:
			Temp = copy.deepcopy(G)
			update()
						

		"""
		Q_Prime : set
			contains the set of all states for the minimized DFA
		
		F_Prime : set
			contains the set of all accept states for the minimized DFA
		
		q0_Prime : str
			Initial state of the minimized DFA and an element of Q_Prime
		
		equiv_class : defaultdict
			Stores the equivalence class of each state q in self.states. That is, [q] is the set of states that are indistinguishable from q
		"""
		Q_Prime = set()
		F_Prime = set()
		q0_Prime = ""

		equiv_class = defaultdict(str)
		for a in self.alphabet:
			D_Prime[a] = dict()
		
		for q in self.states:
			
			"""
			qe : str
				equivalence class of q casted as a string since it needs to be used as a key for dictionaries. A state q is always indistinguishable from itself. 
			"""
			qe = "[" + ' '.join(["(" + " ".join(r) + ")" for r in self.states if G[q][r] == 0]) + "]"  #[q]
			"""
			Maps each state to its equivalence class
			"""
			equiv_class[q] = qe
			"""
			Adds qe to the set of states of the minimized DFA
			"""
			Q_Prime.add(qe)

			"""
			If the equivalence class of q contains the start state then set it to be the initial state of the minimized DFA 
			"""
			if q == self.start_state:
				q0_Prime = qe

			"""
			If the equivalence class of q contains an accept state then add it to the set of accept states of the minimized DFA 
			"""
			if q in self.accept_states:
				F_Prime.add(qe)

		"""
		retrieve_key(d, value) : function

		Parameters:
			d : defaultdict
			value : str

		Given the set of k-v pairs in d such that value == v, returns the first instance of the key of v if it exists
		"""
		def retrieve_key(d, value):
			keys = [k for k, v in d.items() if v == value]
			if keys:
				return keys[0]
			return None

		"""
		Iterate over the cartesian product of the set of states of the minimized DFA and the alphabet
		"""
		for (qq, a) in product(Q_Prime, self.alphabet):
		"""
		Retrieve the key of the equivalence class of qq 
		"""
				q = retrieve_key(equiv_class, qq)
		"""
		Builds the transition function for the minimized DFA. Maps 
		D_Prime[qq][a] to the equivalence class of self.transition[q][a] for each state in Q_Prime 
		"""
				D_Prime[qq].update({a : equiv_class[self.transition[q][a]]})

		"""
		Returns the minimized dfa
		"""
		return DFA(Q_Prime, self.alphabet, D_Prime, q0_Prime, F_Prime)

