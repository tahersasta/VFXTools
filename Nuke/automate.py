####################################################################################################################################################################
Automate the keying of 48 shotss which are identical

####################################################################################################################################################################

import nuke
import os 

shotNo='Shot1'
read = nuke.createNode('Read')
read['file'].setValue(sys.argv[1])
write = nuke.createNode('Write')
write['file'].setValue(sys.argv[2])
write['create_directories'].setValue(True)
nuke.execute(name='Write1',start =1,end=2)
nuke.scriptSaveAs('C:/Users/graphic/Desktop/'+shotNo+'.nk',1)
nuke.scriptExit()
