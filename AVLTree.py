# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0
        self.successor = None
        self.predeccessor = None

    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        if self.value == None:
            return False
        return True
    def is_virtual_node(self):
        if self.value == None:
            return True
        return False


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None

    """searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""

    def search(self, key):
        """helper function: gets a node and key, recursively searches for node with this key in tree
        @type node: AVLNode, key: int
        @param key: a key to be searched
        @rtype AVLNode if node is in tree, else None
        @returns: node corresponding to key
        """

        def searchRec(node, key):
            if node.is_virtual_node():
                return None
            elif node.key > key:
                return searchRec(node.left, key)
            elif node.key < key:
                return searchRec(node.right, key)
            else:
                return node

        if self.root==None:                            #deal with empty tree
            return None
        return searchRec(self.root, key)               

    """inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert(self, key, val):
        if self.search(key)!=None:
            raise AssertionError("Key already exists in the AVL tree.")
           
        ######## OUTSIDE OF HELPER FUNCTIONS, BACK IN INSERT FUNCTION ########
        
        newNode, height_change = self.naive_insert(key, val) #naive_insert adds new node to its position which may result in criminal, and returns pointer to it before AVL fix, and the change in height due to adding the node
        #update_successor(newNode) 
        criminalNode = self.find_criminal(newNode) #find criminal node in tree if exists
        if criminalNode != None: #if criminal node is found, rebalance tree
            return self.balance(criminalNode)
        else: 
            return height_change #else return 0, no rebalancing needed


        """
        naive_insert creates a new node with the key, val parameters 
        and inserts it into the BST placement, without rebalancing
        returns pointer to the added node, for further use (finding criminal, balancing, etc)
        """

    def naive_insert(self, key, val):
        newNode=AVLNode(key,val)
        newNode.size=1
        newNode.height = 0
        height_change = 0
        if self.root == None: # Check if tree is empty, and create the virtual node that we will be shared between whole tree
            virNode = AVLNode(None, None)
            self.root = newNode
            newNode.left = virNode
            newNode.right = virNode
            newNode.parent = None
            newNode.successor=virNode
            newNode.predeccessor=virNode
            virNode.successor=newNode
            virNode.predeccessor=newNode
            return newNode, height_change
        else: # Tree has nodes, traverse until finding the proper placement for node and add it as a leaf
            node = self.root
            while (node.right.is_real_node() and node.key<key) or ((node.left.is_real_node() and node.key>key)):
                if node.key<key:
                    node=node.right
                elif node.key>key:
                    node=node.left
            if node.key>key and (node.left.is_virtual_node()): # Left - Place node in correct location and define virtual node as children
                virtualNode = node.left
                node.left = newNode
                newNode.left = virtualNode
                newNode.right = virtualNode 
                newNode.parent = node
            elif node.key<key and (node.right.is_virtual_node()): # Right - Place node in correct location and define virtual node as children
                virtual_node=node.right
                node.right=newNode
                newNode.left=virtual_node
                newNode.right=virtual_node
                newNode.parent=node

            height_change = self.update_height(node) #calculate change in height due to adding the node
            self.update_size(newNode)
            self.update_successor(newNode)

            return node, height_change #return a tuple - pointer to the new node, and the change in height due to adding the node
        
    """update_height receives a pointer to the newly added node
        updates all heights in its path to the root.
    """
    def update_height(self, node):
        height_changed = 0
        while node != None:
            new_height = 1 + max(node.left.height, node.right.height)  # Calculate new height based on children heights
            if new_height != node.height:  # If the height has changed
                height_changed +=1
                node.height = new_height  # Update the height
            node = node.parent  # Move to the parent node
        return height_changed
    
    """update_size receives a pointer to the newly added node
        updates all sizes in its path to the root.
    """
    def update_size(self, node):
        curr_node = node

        while curr_node != None:
            curr_node.size = curr_node.left.size + curr_node.right.size + 1
            curr_node = curr_node.parent
            
    """update_successor receives a pointer to the newly added node
        updates all successors in its path to the root.
    """

    def update_successor(self, node):
        curr=node #pointer for traveling on the tree and look for predecessor (assuming node is leaf)
        while curr.parent != None: #go up while you are not the root
            if curr.parent.right == curr: #if you turn left (while going up) the parent is the predeccessor
                pre=curr.parent #pre is the predecessor
                pro=pre.successor   #pro is the successor
                break
            curr = curr.parent
        if curr.parent == None:      #if root was reached without turning left it means that you are the minimum
            pro=node.parent
            pre=pro.predeccessor
        
        pre.successor=node    #push node between pre and pro          
        node.successor=pro
        pro.predeccessor=node
        node.predeccessor=pre

        return
    """find_criminal receives a pointer to the newly added node,
        searches for a criminal node in the tree, BF >= 1 or BF <= -1, and returns a pointer to the node.
    """
    def find_criminal(self, node):
        while node is not None: # iterate until we reach the root
            BF = node.left.height - node.right.height # calculate balance factor
            if BF not in (-1,1,0): # if BF is not 0 or 1 or -1, we have a criminal
                return node
            node = node.parent # move to the parent node
        return None  # if we reach the root and haven't found a criminal, return None
        
    """
    balance receives the criminal node and rebalances the tree 
    returns the number of rebalancing operations required to balance the tree.
    """
    def balance(self, node):
        if node == None:
            return
        #node is real
        BF = node.left.height - node.right.height #calculate balance factor
        if BF == 2: #tree is left heavy
            leftBF = node.left.left.height - node.left.right.height
            if leftBF == 1 or leftBF == 0: #left child with balance factor 1, meaning child tree is also left heavy, rotate right to fix
                self.rotate_right(node)
                return 1

            elif leftBF == -1: #left child with balance factor -1, meaning child tree is right heavy, rotate left then right to fix
                self.rotate_left(node.left)
                self.rotate_right(node)
                return 2

        elif BF == -2: #tree is right heavy
            rightBF = node.right.left.height - node.right.right.height
            if rightBF == 1: #right child with balance factor 1, meaning child tree is left heavy, rotate right then left to fix
                self.rotate_right(node.right)
                self.rotate_left(node)
                return 2
            elif rightBF == -1 or rightBF == 0: #right child with balance factor -1, meaning child tree is also right heavy, rotate left to fix
                self.rotate_left(node)
                return 1
        else: #balance factor is ok, and return is irrelevant
            return -1
                


    """
    rotate_right receives the node B in the rotation sequence.
    after rotation: B is right child of A, A is parent of B, A's right child becomes B's left child. 
    A's left child does not change, B's left child does not change
    """
    def rotate_right(self, node):
        B = node
        A = B.left

        if self.root == B: #this means B is the root
            self.root = A
            A.parent = None
            
        else:
            if B.key == B.parent.left.key:
                B.parent.left = A
                A.parent = B.parent
            elif B.key == B.parent.right.key:
                B.parent.right = A
                A.parent = B.parent
        B.left = A.right
        A.right.parent = B
        A.right = B
        B.parent = A
        B.size = B.right.size + B.left.size + 1 #update size for B
        A.size = A.right.size + A.left.size + 1 #update size for A
        self.update_height(B) #change to update height only for B and A manually
        return
    
    """
    symmetrical rotation:
    rotate_left receives the node B in the rotation sequence.
    after rotation: B is left child of A, A is parent of B, A's left child becomes B's right child. 
    A's right child does not change, B's right child does not change
    """
    def rotate_left(self, node):
        B = node
        A = B.right
        if self.root == B: #this means B is the root
            self.root = A
            A.parent = None
            
        else:
            if B == B.parent.left: 
                B.parent.left = A
                A.parent = B.parent
            elif B == B.parent.right:
                B.parent.right = A
                A.parent = B.parent
        B.right = A.left
        A.left.parent = B
        A.left = B
        B.parent = A
        B.size = B.right.size + B.left.size + 1 #update size for B
        A.size = A.right.size + A.left.size + 1 #update size for A
        self.update_height(B) #update height for B and potentially all nodes above it
        return
        


    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        if node == None or self.search(node.key) == None:
            raise AssertionError(f"Node {node.key} doesnt exists in the AVL tree.") 
        
        self.update_successor_for_deletions(node)
        fixNode,heightChanges=self.naive_delete(node) 
        counter=0
        criminal=self.find_criminal(fixNode)
        while criminal != None:
            self.balance(criminal)
            criminal=self.find_criminal(criminal)

    def delete_one_or_zero(self,node): #terrible function but it does the job. we have 3 almost identical cases
        if self.root == node: #if you want to delete the root make your child the root or make the tree empty
            if node.right.is_real_node():
                self.root = node.right
                self.root.parent = None
                #self.root.size -=1     ###update size
            elif node.left.is_real_node():
                self.root = node.left
                self.root.parent = None
                #self.root.size -= 1     ###update size
                #self.root.height -= 1   ###update height
            else:
                self.root = None
            return self.root #this is the first node that its size/height might change so we return it for future fixation

        elif node.parent.right == node: #node is not root and it is someone's right child. so make a "baypass"
            if node.right.is_real_node():
                node.parent.right = node.right
                node.right.parent = node.parent
            elif node.left.is_real_node():
                node.parent.right = node.left
                node.left.parent = node.parent
            else: #node.left is virtual node
                node.parent.right = node.left
            
        
        else: #unforunally the same code with node as left child
            if node.right.is_real_node():
                node.parent.left = node.right
                node.right.parent = node.parent
            elif node.left.is_real_node():
                node.parent.left = node.left
                node.left.parent = node.parent
            else: #node.left is virtual node
                node.parent.left = node.left
        temp=node.parent
        # while(temp != None):  ###update size
        #     temp.size -= 1
        #     temp=temp.parent
        # self.update_height(node)   ###update height
        return node.parent
        
    def update_successor_for_deletions(self, node): #bridge over troubled node 
        pre=node.predeccessor
        pro=node.successor
        pre.successor=pro
        pro.predeccessor=pre
 
    def naive_delete(self, node):
        if node.left.is_virtual_node() or node.right.is_virtual_node(): 
            fixNode = self.delete_one_or_zero(node)
            heightChange = self.update_height(fixNode)
            self.update_size(fixNode)

        else: #node has two children. take out the successor from tree and replace it with node (it has 1/0 children so we can use our function)
            succ = node.successor
            fixNode = self.delete_one_or_zero(succ)
            heightChange = self.update_height(fixNode)
            self.update_size(fixNode)
            succ.height=node.height
            succ.size=node.size
            succ.left = node.left
            succ.right = node.right
            succ.parent=node.parent
            node.left.parent = succ #might cause virtual node to have parents, but doesnt matter
            node.right.parent = succ
            
            if self.root == node:   #again we have 3 almost identical cases
                self.root = succ
            elif node.parent.right == node:
                node.parent.right = succ
            elif node.parent.left == node:
                node.parent.left = succ
        #heightChange=self.update_height(fixNode) #  MUST BE CHANGED!!!!!!!
        return fixNode,heightChange

        
        
 



    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        """helper function: gets a node and lst, recursively fill the list with tuples of key,value sorted by the key
        @type node: AVLNode, lst: list
        @base case: reached virtual node
        @returns: doesn't return anything. just filling the list
        """

        def avl_to_arrayRec(node, lst):
            if node.is_virtual_node():
                return lst
            avl_to_arrayRec(node.left, lst)
            lst.append((node.key,node.value))
            avl_to_arrayRec(node.right, lst)

        sortedArray = []
        avl_to_arrayRec(self.root, sortedArray)
        return sortedArray

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        if self.root == None:
            return 0
        return self.root.size

    """compute the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	"""

    # If we go up to the right, don't do anything
    def rank(self, node):
        counter = 0
        curr = node
        while curr.parent != None:  # Keep going up to the root
            if curr.parent.key < curr.key:
                counter += (
                    1 + curr.parent.left.size
                )  # If we go up to the left, add parent's left sub-tree + 1 to the counter
            curr = curr.parent
        counter += 1 + curr.left.size
        return counter

    """finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	"""

    def select(self, i):
        def selectRec(node,i):
            n=node.left.size                           #assuming size of a virtual node is 0         
            
            if n>=i:                                    #means the left son has at least i nodes
                return selectRec(node.left, i)         #go search the i'th in the left branch
            
            elif n+1==i:                               #means this node if the i'th, so return it                             
                return node
            else:                                      #means i>n+1
                return selectRec(node.right, i-n-1)    #return the i-n-1 item in the right branch which is the i'th in the tree
        
        
        if self.root==None:                            #deal with empty tree
            return None
        
        node_temp=selectRec(self.root,i)
        return node_temp

    """finds the node with the largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: the node with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	"""

    def max_range(self, a, b):
        startNode=self.search(a)
        if startNode == None:
            raise AssertionError(f"Key {a} doesnt exist in the AVL tree.") 
        maxNode=startNode
        searchingNode = startNode.successor
        while searchingNode.is_real_node() and searchingNode.key <= b:
            if searchingNode.value > maxNode.value:
                maxNode = searchingNode
            searchingNode = searchingNode.successor
        return maxNode

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root
