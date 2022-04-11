import pickle
import sys
import pprint
pp = pprint.PrettyPrinter()


with open('./data/mutation_table.pickle', 'rb') as f:
    data = pickle.load(f)

pp.pprint(data)
