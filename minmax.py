class Node():
    def __init__(self, value):
        # Heurestic value
        self.value = value
        self.child_nodes=[]
        self.child_count=0
    def AddNode(self,node):

        self.child_nodes.append(node)
        self.child_count=len(self.child_nodes)
def minmax(depth):
    # Choix de la profondeur à 2 pour l'instant
    pass
