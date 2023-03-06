import nuke
def seperateChannels():
    if len(nuke.selectedNode()) == 1:
        node = nuke.selectedNode()
        saveX = node.xpos()
        saveY = node.ypos()
        channels = node.channels()

        findAOV = list( set([c.split('.')[0] for c in channels]) )
        findAOV.sort()

        mergeNode = None


        for aov in findAOV:

            if mergeNode == None:
                node = nuke.nodes.Dot(inputs = [ node] , xpos=(node.xpos()+34),ypos = (node.ypos() + 250))
                copyDot =  nuke.nodes.Dot(inputs = [ node] , xpos=(node.xpos()+250),ypos = (node.ypos()))
                mergeNode = nuke.nodes.Shuffle(label = "[value in]" ,inputs=[ node ], xpos=node.xpos()-34, ypos=node.ypos()+50 )
                mergeNode['in'].setValue(aov)
                saveY = mergeNode.ypos()+750
            else:
                node = nuke.nodes.Dot( inputs=[ node ], xpos=node.xpos()-250, ypos=node.ypos())
                shuffleNode = nuke.nodes.Shuffle( label="[value in]", inputs=[ node ], xpos=node.xpos()-34, ypos=node.ypos()+50 )
                shuffleNode['in'].setValue(aov)
                dotNode = nuke.nodes.Dot( inputs=[ shuffleNode ], xpos=( node.xpos() ), ypos=saveY )
                mergeNode = nuke.nodes.Merge2( operation='plus', inputs=[ mergeNode , dotNode ], xpos=saveX, ypos=( dotNode.ypos()-5 ) )
                saveY = mergeNode.ypos()+75 
        if mergeNode != None:
            copyDot = nuke.nodes.Dot(inputs = [copyDot], xpos = (copyDot.xpos())  , ypos = saveY)
            copyNode = nuke.nodes.Copy(inputs = [mergeNode,copyDot],from0='rgba.alpha' , to0 = 'rgba.alpha', xpos=(mergeNode.xpos()), ypos=(copyDot.ypos()-11))
            pad = 75
            backdropNode = nuke.nodes.BackdropNode(label="CG Breakout", note_font_size=42, xpos=(node.xpos()-pad), bdwidth=abs(copyDot.xpos()-node.xpos())+(pad*2) , ypos=node.ypos()-pad, bdheight=abs(copyDot.ypos()-node.ypos())+(pad*2) )
    else:
        nuke.message('Invalid Selection')
        pass
   
seperateChannels()
    
    
