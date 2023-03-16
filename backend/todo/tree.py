# from sklearn.tree import export_graphviz
# import graphviz

# # Assuming that you have trained a decision tree model and stored it in a variable called `clf`

# # Create a visualization of the decision tree model
# dot_data = export_graphviz(clf, out_file=None, 
#                            feature_names=X.columns, 
#                            class_names=['0', '1'], 
#                            filled=True, 
#                            rounded=True, 
#                            special_characters=True)
# graph = graphviz.Source(dot_data)
# graph.format = 'png' # set image format
# graph.render('decision_tree') # save image to file

