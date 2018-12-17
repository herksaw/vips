# -*- coding: utf-8 -*-
"""
Created on Tue May 29 12:37:05 2018

@author: Hard-
"""
import sys
import BlockVo
import BlockRule

class BlockExtraction:
    
    html = None
    blockList = []
    hrList = []
    cssBoxList = dict()
    block = None
    count = 0
    count1 = 0
    count2 = 0
    count3 = 1
    all_text_nodes = []
    important_blocks = []
    title_block = []
    content_block = []
    page_width = 0
    page_height = 0
    max_title_score = 0
    max_content_score = 0


    def __init__(self):
        self.blockList = []
        self.block = BlockVo.BlockVo()
        BlockExtraction.max_title_score = 0
        BlockExtraction.max_content_score = 0
        BlockExtraction.title_block = []
        BlockExtraction.content_block = []
        BlockExtraction.important_blocks = []
                
    def service(self, url, nodeList, window_size):
        BlockRule.BlockRule.initialize(nodeList)
        self.page_width = window_size['width']
        self.page_height = window_size['height']
        body = nodeList[0]
        self.initBlock(body, self.block)  
        print("-----Done Initialization-----")
        #sys.exit(0)       
        self.count3 = 0
        self.dividBlock(self.block)
        print(self.count2)       
        print("-----Done Division-----")
        BlockVo.BlockVo.refreshBlock(self.block)
        print("-----Done Refreshing-----")
        self.chooseBlocks(self.block)
        self.filList(self.block)
        print("-----Done Filling-----")
        #self.checkText()
        BlockExtraction.title_block.append(self.block)
        BlockExtraction.content_block.append(self.block)
        #self.findTitle(BlockVo.BlockVo.blocksChosen[0]
        self.findTitle(self.block)
        self.findContent(self.block)
        BlockExtraction.important_blocks.append(self.title_block[0])
        BlockExtraction.important_blocks.extend(self.content_block)
        print("Max Title Score:" + str(BlockExtraction.max_title_score))
        print("Title Block:" + BlockExtraction.title_block[0].id)
        print("Content Block:" + BlockExtraction.content_block[0].id)
        return self.block
        
    def chooseBlocks(self, block):
        idList = []
        heightList = []
        duplicateList = []
        centerPoint = self.count3/2

        BlockVo.BlockVo.findBlocks(block)
        BlockVo.BlockVo.blocksChosen.sort(key=lambda x:x.height, reverse=True)

        #Remove redundant blocks with same height
        for i in range(0, len(BlockVo.BlockVo.blocksChosen)):
            if BlockVo.BlockVo.blocksChosen[i].height not in heightList:
                heightList.append(BlockVo.BlockVo.blocksChosen[i].height)
            else:
                duplicateList.append(BlockVo.BlockVo.blocksChosen[i])

        BlockVo.BlockVo.blocksChosen = [x for x in BlockVo.BlockVo.blocksChosen if x not in duplicateList]
        
        heightList.sort()
        mininum_height   = heightList[0]

        #Only select block(s) with mininum height and contained the center point among chosen blocks 
        BlockVo.BlockVo.blocksChosen = [blockChosen for blockChosen in BlockVo.BlockVo.blocksChosen if blockChosen.height == mininum_height 
        and (block.x < centerPoint < (block.x + block.width))]

        for blckChosen in BlockVo.BlockVo.blocksChosen:
            idList.append(blckChosen.id)
            print(blckChosen.id,",",blckChosen.boxs[0].nodeName,",", blckChosen.height)


    #Find the block contains title of a blog post
    def findTitle(self, blockVo):
            BlockRule.BlockRule.titleRule1(blockVo)
            BlockRule.BlockRule.titleRule2(blockVo)
            BlockRule.BlockRule.titleRule3(blockVo, self.page_width)
            BlockRule.BlockRule.titleRule4(blockVo, self.page_height)
            BlockRule.BlockRule.titleRule5(blockVo, self.page_width)
            if blockVo.titleScore > BlockExtraction.max_title_score:
                    BlockExtraction.max_title_score = blockVo.titleScore
                    BlockExtraction.title_block[0] = blockVo
            for c in blockVo.children:
                self.findTitle(c)
            
    #Find the block contains the content of a blog post
    def findContent(self, blockVo):
        BlockRule.BlockRule.contentRule1(blockVo, BlockExtraction.title_block[0], self.page_height)
        #BlockRule.BlockRule.contentRule2(blockVo)
        BlockRule.BlockRule.contentRule3(blockVo, self.page_width, self.page_height)
        if blockVo.contentScore > BlockExtraction.max_content_score:
            BlockExtraction.max_content_score = blockVo.contentScore
            BlockExtraction.content_block[0] = blockVo
        for c in blockVo.children:
            self.findContent(c)


    
    def initBlock(self, box, block):
        block.boxs.append(box)
        print(self.count,"####Here Name=",box.nodeName)
        self.count+=1
            
        if(box.nodeName == "hr"):
            self.hrList.append(block)
            self.count1 = 0
        if box.nodeType != 3:
            subBoxList = box.childNodes
            for b in subBoxList:
                try:
                    if b.nodeName != "script" and b.nodeName != "noscript" and b.nodeName != "style":
                        #print(self.count1," : ",b.nodeName,", ",box.nodeName)
                        print(b.nodeName,", ",b.visual_cues['display'],", ",b.visual_cues['visibility'])
                        self.count1+=1
                        bVo = BlockVo.BlockVo()
                        bVo.parent = block
                        block.children.append(bVo)
                        self.initBlock(b, bVo)
                except AttributeError:
                    print(b,",",b.nodeType)
                    sys.exit(0)
            
    def dividBlock(self, block):
        self.count2+=1
        print (self.count2)
        
        if(block.isDividable and BlockRule.BlockRule.dividable(block)):
            block.isVisualBlock = False         
            for b in block.children:
                self.count3+=1
                print(self.count3)
                self.dividBlock(b)
                
    def filList(self, block):
        if block.isVisualBlock:
            self.blockList.append(block)
        else:
            for blockVo in block.children:
                self.filList(blockVo)

    def checkText(self):
        for blockVo in self.blockList:
            removed = True
            for box in blockVo.boxs:
                if box.nodeType == 3:
                    if box.parentNode.nodeName != "script" and box.parentNode.nodeName != "noscript" and box.parentNode.nodeName != "style":
                         if not box.nodeValue.isspace() or box.nodeValue == None:
                             removed = False
            if(removed):
                self.blockList.remove(blockVo)
        
    def resetBlocks(self):
        print("Resetting Blocks...")
        self.html = None
        self.blockList.clear()
        self.hrList.clear()
        self.cssBoxList = dict()
        self.block = None
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 1
        self.all_text_nodes.clear()
        BlockExtraction.title_block.clear()
        BlockVo.BlockVo.blocksChosen.clear()
        BlockVo.BlockVo.count = 1
        BlockVo.BlockVo.maxHeight = 0