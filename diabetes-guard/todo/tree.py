import graphviz

# Load the di.dot file
dot = graphviz.Digraph()
dot.source = open('di.dot').read()

# Define the extracted rules
rules = [
    {'test': 'hypotonic urine > 1.006', 'result': 'di'},
    {'test': 'polyuria > 302.0', 'result': 'di'},
    {'test': 'thirst <= 0.5', 'result': 'di'},
    {'test': 'hypotonic urine <= 1.006', 'result': 'osm_diur'},
    {'test': 'thirst > 0.5', 'result': 'osm_diur'},
    {'test': 'hypotonic urine > 1.006', 'result': 'adi'},
    {'test': 'polyuria <= 302.0', 'result': 'adi'},
    {'test': 'hypotonic urine <= 1.006', 'result': 'fluid_ov'},
    {'test': 'thirst <= 0.5', 'result': 'fluid_ov'},
    {'test': 'hypotonic urine > 1.006', 'result': 'healthy'},
    {'test': 'polyuria > 302.0', 'result': 'healthy'},
    {'test': 'thirst > 0.5', 'result': 'healthy'},
]

# Traverse the decision tree based on the extracted rules to identify the path that corresponds to the diagnosis
path = []
for rule in rules:
    if rule['result'] == 'di':
        path.append(rule['test'])
        break
for rule in rules:
    if rule['result'] == 'di' and rule['test'] != path[-1]:
        path.append(rule['test'])
        break
for rule in rules:
    if rule['result'] == 'di' and rule['test'] != path[-1]:
        path.append(rule['test'])
        break

# Color the nodes along the path to highlight the diagnosis
for node in dot.nodes():
    if any(test in node for test in path):
        node.attr['style'] = 'filled'
        node.attr['fillcolor'] = 'yellow'

# Display the tree view
dot.render(view=True)
