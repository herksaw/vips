# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:45:17 2018

@author: Hard-
"""
import uuid
import BlockRule

class BlockVo:
    
    id = None
    x = 0
    y = 0
    width = 0
    height = 0
    boxs = []
    parent = None
    children = []
    isVisualBlock = True
    isDividable = True
    Doc = 0
    count = 1
    maxHeight = 0
    blocksChosen = []
    titleScore = 0
    contentScore = 0
        
    def __init__(self):
        self.id = str(BlockVo.count)
        BlockVo.count += 1
        #str(uuid.uuid4())
        self.boxs = []
        self.children = []
        self.titleScore = 0
        self.contentScore = 0
    
    def refresh(self):
        for i in range(0, len(self.boxs)):
            box = self.boxs[i]
            #print (box.get_attribute("id"),",",box.tag_name,",",box.location)
            if i == 0:
                self.x = box.visual_cues['bounds']['x']
                self.y = box.visual_cues['bounds']['y']
                self.width = box.visual_cues['bounds']['width']
                self.height = box.visual_cues['bounds']['height']
            else:
                RBX = self.x + self.width
                RBY = self.y + self.height
                boxRBX = box.visual_cues['bounds']['x']+box.visual_cues['bounds']['width']
                boxRBY = box.visual_cues['bounds']['y']+box.visual_cues['bounds']['height']
                RBX = boxRBX if (boxRBX > RBX) else RBX
                RBY = boxRBY if (boxRBY > RBY) else RBY
                self.x = box.visual_cues['bounds']['x'] if (box.visual_cues['bounds']['x']<self.x) else self.x
                self.y = box.visual_cues['bounds']['y'] if (box.visual_cues['bounds']['y'] <self.y) else self.y
                self.width = RBX - self.x
                self.height = RBY - self.y

    @staticmethod  
    def refreshBlock(block):
        block.refresh()
        if block.height > BlockVo.maxHeight and block.boxs[0].nodeName != "body":
                BlockVo.maxHeight = block.height   
        for blockVo in block.children:
            BlockVo.refreshBlock(blockVo)

    #Find block(s) with height greater or equal to the threshold
    @staticmethod
    def findBlocks(block):
        if block.height >= (BlockVo.maxHeight*0.8) and block.boxs[0].nodeName != "body" and block.boxs[0].nodeType != 3:
            BlockVo.blocksChosen.append(block)
        for blockVo in block.children:
            BlockVo.findBlocks(blockVo)
    