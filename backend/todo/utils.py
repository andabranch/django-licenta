import base64
from sklearn.tree import export_graphviz
import pydotplus
from IPython.display import Image
from sklearn.tree import DecisionTreeClassifier


def get_decision_tree_data(model):
    # Export the decision tree as a DOT file
    dot_data = export_graphviz(model, out_file=None, 
                               feature_names=['age','polyuria','hypotonic urine', 'thirst', 'serum osmolality','serum sodium'],  
                               class_names=[    ],  
                               filled=True, rounded=True,  
                               special_characters=True)  
    # Convert the DOT file to a PNG image
    graph = pydotplus.graph_from_dot_data(dot_data)  
    graph.write_png('tree.png')
    
    # Return the image as a data URL
    with open('tree.png', 'rb') as f:
        image_data = f.read()
    data_url = "data:image/png;base64," + base64.b64encode(image_data).decode()
    return data_url

def get_decision_tree_model(dataset):
    # Define the features and target variable
    X = dataset[['age', 'polyuria', 'hypotonic urine', 'thirst', 'serum osmolality', 'serum sodium']]
    y = dataset['Fluid Overload','Osmotic Diuresis','DI','ADI','Healthy']

    # Create a decision tree classifier with default parameters
    clf = DecisionTreeClassifier()

    # Fit the classifier to the data
    clf.fit(X, y)

    # Return the decision tree model
    return clf
