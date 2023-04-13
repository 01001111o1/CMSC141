from dfa import DFA as DFA_141
from automathon import DFA as DFA_Automathon
from PySimpleAutomata import DFA, automata_IO
from graphviz import Source

M = DFA_Automathon(Q = {"a", "b", "c", "d", "e", "f"}, sigma = {"0", "1"},
delta = {
	"a": { "0": "b", "1": "c" },
	"b": { "0": "a", "1": "d" },
	"c": { "0": "e", "1": "f" },
	"d": { "0": "e", "1": "f" },
	"e": { "0": "e", "1": "f" },
	"f": { "0": "f", "1": "f" },
	},
initialState = "a", F = {"c", "d", "e"})

#dfa = automata_IO.dfa_dot_importer("C:/Users/Sean/Desktop/CMSC141/test.dot")
#automata_IO.dfa_to_dot(dfa, "test", "C:/Users/Sean/Desktop/CMSC141/")

path = "C:/Users/Sean/Desktop/CMSC141/test.dot"
s = Source.from_file(path)
#s.render("test.dot", format = "svg", view = True)
s.render(format = "svg", view = True)

#Z = M.DFA_Intersection(A)
#Z.DFA_Strip()
#print(Z)
#Z = M.DFA_Minimize()
#print(Z)
# for input_string in ["bbbbab"]:
# 	print(M.__repr__() + " accepts " + input_string + "? " + str(M.accepts(input_string)))	

A = DFA_141(
	states={"q0","q1","q2"}, 
	alphabet={"0","1"}, 
	transition={
    "q0": {"0": "q1", "1": "q2"},
    "q1": {"0": "q1", "1": "q1"},
    "q2": {"0": "q2", "1": "q2"}}, 
    start_state="q0", 
    accept_states={"q1"}
)

B = DFA_141(
	states={"r0","r1","r2", "r3"}, 
	alphabet={"0","1"}, 
	transition={
    "r0": {"0": "r1", "1": "r2"},
    "r1": {"0": "r1", "1": "r2"},
    "r2": {"0": "r2", "1": "r3"}, 
    "r3": {"0": "r3", "1": "r3"}}, 
    start_state="r0", 
    accept_states={"r2"}
)

Z = A.DFA_Intersection(B).DFA_Minimize()
print(Z)

C = DFA_141(
	states={"q0","q1","q2"}, 
	alphabet={"0","1"}, 
	transition={
    "q0": {"0": "q1", "1": "q1"},
    "q1": {"0": "q2", "1": "q2"},
    "q2": {"0": "q1", "1": "q1"}}, 
    start_state="q0", 
    accept_states={"q0", "q2"}
)

D = DFA_141(
	states={"r0","r1","r2"}, 
	alphabet={"0","1"}, 
	transition={
    "r0": {"0": "r0", "1": "r1"},
    "r1": {"0": "r2", "1": "r2"},
    "r2": {"0": "r2", "1": "r1"}}, 
    start_state="r0", 
    accept_states={"r1"}
)

# E = C.DFA_Intersection(D).DFA_Minimize()
# print(E)