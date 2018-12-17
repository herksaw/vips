# -*- coding: utf-8 -*-
"""
Created on Tue May 29 20:40:03 2018

@author: Hard-
"""

class BlockRule:
    threshold = 40000
       
    @staticmethod
    def initialize(passed_nodeList):
        global nodeList 
        nodeList =  passed_nodeList
    
    @staticmethod
    def dividable(block):                 
        box = block.boxs[0]
        #print(box.tag_name)
        if box.nodeType == 3:
            return False
        name = box.nodeName
    
        if(name == "img"):
            return False
        if not BlockRule.isBlock(box):
            return BlockRule.inlineRules(block)
        elif (name == 'table'):
            return BlockRule.tableRules(block)
        elif (name == 'tr'):
            return BlockRule.trRules(block)
        elif (name == 'td'):
            return BlockRule.tdRules(block)
        elif (name == 'p'):
            return BlockRule.pRules(block)
        else:
            return BlockRule.otherRules(block)
    
    @staticmethod
    def otherRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule4(block):
            return True
        if BlockRule.rule6(block):
            return True
        if BlockRule.rule7(block):
            return True
        if BlockRule.rule9(block):
            return True
        if BlockRule.rule10(block):
            return True
        if BlockRule.rule12(block):
            return True    
        return False
    
    @staticmethod
    def pRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule4(block):
            return True
        if BlockRule.rule5(block):
            return True
        if BlockRule.rule6(block):
            return True
        if BlockRule.rule7(block):
            return True
        if BlockRule.rule9(block):
            return True
        if BlockRule.rule10(block):
            return True    
        if BlockRule.rule12(block):
            return True   
        return False
    
    @staticmethod
    def tdRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule4(block):
            return True
        if BlockRule.rule9(block):
            return True
        if BlockRule.rule10(block):
            return True
        if BlockRule.rule11(block):
            return True
        if BlockRule.rule13(block):
            return True
        return False
    
    @staticmethod
    def trRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule7(block):
            return True
        if BlockRule.rule8(block):
            return True
        if BlockRule.rule10(block):
            return True
        if BlockRule.rule13(block):
            return True
        return False
    
    @staticmethod
    def tableRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule8(block):
            return True
        if BlockRule.rule10(block):
            return True
        if BlockRule.rule13(block):
            return True
        return False
    
    @staticmethod    
    def inlineRules(block):
        if BlockRule.rule1(block):
            return True
        if BlockRule.rule2(block):
            return True
        if BlockRule.rule3(block):
            return True
        if BlockRule.rule4(block):
            return True
        if BlockRule.rule5(block):
            return True
        if BlockRule.rule6(block):
            return True
        if BlockRule.rule7(block):
            return True
        if BlockRule.rule9(block):
            return True
        if BlockRule.rule10(block):
            return True
        if BlockRule.rule12(block):
            return True
        return False
    
    
    """ 
    Rule 1: Remove all the invalid nodes and partially valid nodes which does not have any child. 
    Note that, valid nodes without any child must be kept, since, although they do not have a valid content, 
    they appear in the page layout and might be used as a separator between two different topics. 
    """
    @staticmethod
    def rule1(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        if not BlockRule.isValidNode(node):
            if BlockRule.isPartiallyValidNode(node) and subBoxList is None:
                return False
        return True
    
    """ 
    Rule 2: If a node has only text node or invalid children, no block extracted. 
    """
    @staticmethod
    def rule2(block):
        node = block.boxs[0]
        subBoxList = node.childNodes

        for box in subBoxList:
            if not BlockRule.isTextNode(box) and BlockRule.isValidNode(box):
                return True
        return False
    
    """ 
    Rule 3:  If node has only one child, 
    (a) If child is a text node or virtual text node, then no block extracted. 
    (b) If child is line-break node, then same rules are applied to the child node
    """
    @staticmethod
    def rule3(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        if(len(subBoxList) == 1):
            box = subBoxList[0]
            if BlockRule.isTextNode(box) or BlockRule.isVirtualTextNode(box):
                return False
            if BlockRule.isBlock(box):
                BlockRule.rule3(block.children)
        return False
        
    """
    Rule 4: If all the children are virtual text nodes 
    of a node, node is put into block pool 
    and we do not divide this rule in next turns. 
    """
    @staticmethod
    def rule4(block):
        node = block.boxs[0]
        subBoxList = node.childNodes

        for box in subBoxList:
            if not BlockRule.isVirtualTextNode(box):
                block.isDividable = False
                return False    
        return True
            
    """
    Rule 5: If a node contains a child whose tag is HR, 
    BR or any of valid nodes which has no children, 
    then the node is divided into two as the nodes 
    before the separator and after the separator. 
    For each side of the separator, two new blocks are created and 
    children nodes are put under these blocks. 
    Note that, separator does not extract a block under the main block, 
    it just serves to extract two blocks which other nodes are put into. 
    """
    @staticmethod
    def rule5(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        for box in subBoxList:
            if BlockRule.isValidNode(box):
                if box.child is not None:
                    return True
            if box.nodeName == 'hr' or box.nodeName == 'br': 
                return True
        return False
    
    """
    Rule 6:  If node is a table and some of its columns have different background color than the others, 
    divide the table into the number saparate columns and construct a block for each piece. 
    """
    @staticmethod
    def rule6(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        if node.nodeName == 'table':
            for box in subBoxList:
                if box.nodeName == 'td':
                    bColor = box.visual_cues['background-color']
                    break
            for box in subBoxList:
                if box.nodeName == 'td':
                    if box.visual_cues['background-color'] != bColor:
                        return True
        return False
    
    """
    Rule 7:  If one of the child node has bigger font size than its previous sibling, divide node into 
    two blocks. Put the nodes before the child node with bigger font size into the ﬁrst block, 
    and put the remaining nodes to the second block. 
    """
    #check child node
    @staticmethod
    def rule7(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        maxFontSize = subBoxList[0].visual_cues['font-size']
        for box in subBoxList:
            if box.visual_cues['font-size'] > maxFontSize:
                return True
        return False
        
    """
    Rule 8:  If the ﬁrst child of the node has bigger font size than the remaining children, extract 
    two blocks, one of which is the ﬁrst child with bigger font size, and the other  contains remaining children. 
    """
    @staticmethod
    def rule8(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        maxFontSize = subBoxList[0].visual_cues['font-size']
        for box in subBoxList:
            if box.visual_cues['font-size'] > maxFontSize:
                return False
        return True

    """
    Rule 9: If a node has some valid nodes and some partially valid nodes in its children, divide this node. 
    Each valid node will be a separate block, and each partially valid node next to each other create a block as a whole. 
    """
    @staticmethod
    def rule9(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        validCount = 0
        partiallyValidCount = 0
        for box in subBoxList:
            if BlockRule.isValidNode(box):
                validCount+=1
            if BlockRule.isPartiallyValidNode(box):
                partiallyValidCount+=1
        if validCount != 0 and partiallyValidCount != 0:
            return True
        return False
    """
    Rule 10:  If node has at least one child with ﬂoat value ”left” or ”right”, create three blocks. For each children, 
    (a) If child is left ﬂoat, put it into the ﬁrst block.
    (b) If child is right ﬂoat, put it into the second block. 
    (c) If child is not both left and right ﬂoat, put it into the third block. 
        If ﬁrst block or second block have children, create new blocks for them. 
        Also, create a new block for the child without ﬂoat.
    """
    @staticmethod
    def rule10(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        for box in subBoxList:
            if box.visual_cues['float'] == 'left' or box.visual_cues['float'] == 'right':
                return True 
        return False
    
    """
    Rule 11:  If a node has a child, whose at least one of margin-top and margin-bottom values are nonzero, divide this node into two blocks. 
    Put the sibling nodes before the node with nonzero margin into the ﬁrst block and put the siblings after the node with nonzero margin into the second block.
    (a) If child has only nonzero margin-top, put the child into second block. 
    (b) If child has only nonzero margin-bottom, put the child into ﬁrst block. 
    (c) If child has both nonzero margin-top and nonzero margin-bottom, create a third block and put it between two blocks.
    """
    @staticmethod
    def rule11(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        for box in subBoxList:
            if box.visual_cues['margin-top'] != 0 or box.visual_cues['margin-bottom'] != 0:
                return True 
        return False
    
    """
    Rule 12:  If a node has a line-break child containing an image, divide node into two blocks. 
    Put the nodes before the child with image into the ﬁrst block, and put the remaining children into the second block.
    """
    @staticmethod
    def rule12(block):
        node = block.boxs[0]
        subBoxList = node.childNodes
        for box in subBoxList:
            if BlockRule.isBlock(box):
                for child in box.childNodes:
                    if child.nodeName == 'img':
                        return True
        return False

    """
    Rule 13:  If the ﬁrst child of the node contains an image, put this child as a block, 
    and create a new block for the remaining children.

    """
    @staticmethod
    def rule13(block):
        node = block.boxs[0]
        firstChild = node.childNodes[0]
        for child in firstChild.childNodes:
            if child.nodeName == 'img':
                return True
        return False
    
    @staticmethod
    def hasValidChildNode(node):
        subBoxList = node.childNodes
        for box in subBoxList:
            if(BlockRule.isValidNode(box)):
                return True
        return False
    
    """
    Valid nodes are those appear in the page layout. They consist of partially valid 
    nodes with visible children and the remaining of the line-break nodes that does not included 
    in partially valid nodes. 
    """    
    @staticmethod
    def isValidNode(node): 
        display = node.visual_cues['display']
        visibility = node.visual_cues['visibility']
        
        if display == 'none' or visibility == 'hidden':
            if BlockRule.isPartiallyValidNode(node):
                return False
        height = node.visual_cues['bounds']['height']
        width = node.visual_cues['bounds']['width']
        #print(height,"+++++", type(height))
        #print(width,"+++++", type(width))
        if height == 0 or width == 0:
            return False
        return True
    
    @staticmethod
    def isPartiallyValidNode(node):
        subBoxList = node.childNodes
        for box in subBoxList:
            if BlockRule.isValidNode(box) or BlockRule.isTextNode(box):
                return True
        return False
    
    """
    the DOM node corresponding to free text, which does not have an html tag
    """   
    @staticmethod
    def isTextNode(node):
        return node.nodeType == 3

    
    """
    Virtual text node (recursive definition):
	 Inline node with only text node children is a virtual text node.
	 Inline node with only text node and virtual text node children is a virtual text node.
    """
    @staticmethod
    def isVirtualTextNode(node):
        subBoxList = node.childNodes
        count = 0
        for box in subBoxList:
            if(BlockRule.isTextNode(box) or BlockRule.isVirtualTextNode(box)):
                count+=1
        if(count == len(subBoxList)):
            return True
        return False
    
    
    @staticmethod
    def isBlock(box):
        if box.visual_cues['display'] == "inline" or box.visual_cues['display'] == "inline-block":
            return False
        else:
            return True  
        
    @staticmethod
    def isOnlyOneDomSubTree(pattern, node, result):
        if pattern.nodeName != node.nodeName:
            result = False
        pattern_child = pattern.childNodes
        node_child = node.childNodes
        if len(pattern_child) != len(node_child):
            result = False
        if not result:
            return 
        for i in range(0,len(pattern_child)):
            BlockRule.isOnlyOneDomSubTree(pattern_child[i],node_child[i],result)
                   
    @staticmethod
    def getDocByTagSize(tag, size):
        return 7
        