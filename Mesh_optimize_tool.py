"""
------------------------------------------
AssetOptimizer.py
Author: Yohan Kim
email: ae2eo@hotmail.com

Website : https://3dyohan.wixsite.com/3dart
------------------------------------------

Helps to optimize asset files.

============================================
"""

import os
import maya.cmds as mc
import pymel.core as pm
import sys
import maya.OpenMaya as OpenMaya


#create UI
def createUI():

    if mc.window('optimizeMeshes_UI', exists=True): 
        mc.deleteUI('optimizeMeshes_UI', window = True)  

    optimizeMeshes_UI = mc.window('optimizeMeshes_UI', title='mesh optimize tool', wh=(250,200))
    mc.columnLayout()

    selectDirectoryBtn = mc.button(label = 'Select Directory', command  = 'getPathtoAssetectory()') 
    
    mc.textField('directoryTextField', w = 300, ed = False)
    mc.text(label='')

    mc.text(label='Asset Group Name')   
    mc.textField('sourceTextField', text = '', ed = True, w = 250, en = True  )
    mc.text(label='')
    
    OptimizeSceneBtn = mc.button(label = '    Optimize   ', command  = 'OptimizeScene()') 
    mc.showWindow(optimizeMeshes_UI)

    


#reassign textures using UI
def OptimizeScene():

    PathtoAsset = mc.textField('directoryTextField', q= True, text = True)
    newAssetName = mc.textField('sourceTextField', q= True, text = True)
    ListofMayaF = mc.getFileList( folder = '%s' % PathtoAsset,filespec='*.ma')
    
    #check if directory name exist
    Directory_check(PathtoAsset)

    #check if group name exist
    Group_name_check(newAssetName)

    #new scene
    mc.file (f=True, new=True)

    #import all asset files
    for f in ListofMayaF:
       mc.file(PathtoAsset +"/" + f, namespace='temp', i=True)

    #clean up scene
    cleanup_scene_P()

    #check if there is deplicated name with asset group   
    Group_name_duplicated(newAssetName)

    selectGrp = mc.ls("*:geo_GRP")
    polyGons = mc.filterExpand(selectGrp, sm = 12)
    mc.select(polyGons, r = True)
    meshinGrp = mc.ls( sl=True )

    #Make objs keyable
    ChannelKeyable(polyGons)

    #assign 'lambert1' shader on meshes
    mc.sets(polyGons, forceElement="initialShadingGroup") 

    #create asset group
    newGrp_Name = '%s' % newAssetName + "_GRP" 

    mc.ls(polyGons)
    mc.group(n =newGrp_Name)

    freeze_meshes(polyGons)

    #rename meshes
    rename_number(meshinGrp)

    cleanup_scene_S(newGrp_Name)

    print "The process were done!"




#make channel keyable
def ChannelKeyable(self):
	KeyableList = ('translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','visibility')
	
	for sn in self:
		for brands in KeyableList:
			NewNameCom = sn + "." + brands
			mc.setAttr (NewNameCom, lock= False, keyable=True, cb = False)




#clean up scene files
def cleanup_scene_P():
    mc.select( all=True,hi = True )

	#unlock
    for obj in pm.selected():
        for a in pm.listAttr(obj):
            obj.attr(a).unlock()
    mc.SelectAllGeometry()
    mc.lockNode( lock=False )

    #remove preconstruction history
    mel.eval("DeleteAllHistory")
    mel.eval("BakeAllNonDefHistory")
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1","deleteUnusedNodes")')
    remove_pymelnode()


#freeze transform
def freeze_meshes(self):
	mc.makeIdentity( apply=True, translate=True, rotate=True, scale=True )




#remove all except asset group
def cleanup_scene_S(self):    
    mc.select( all=True)
    mc.select( self,d=True)
    mc.delete()



#unlock all objs
def unlock_all():
    for obj in pm.selected():
        for a in pm.listAttr(obj):
            obj.attr(a).unlock()
    mc.SelectAllGeometry()
    mc.lockNode( lock=False )



#remove pymel node
def remove_pymelnode():
    mc.select( '__pymelUndoNode')
    mc.lockNode( lock=False )
    mc.delete()  




#rename meshes with numbers
def rename_number(self):
        newAssetName = mc.textField('sourceTextField', q = True, text = True)

        start_number = 1
        end_number = len(self)
        padding_int = 4
        zero_padding = ""

        for s in reversed(self):
            end_number_len = len(str(end_number))
            
            if padding_int > end_number_len:
                zero_padding = "0" * (padding_int - end_number_len)

            #rename    
            mc.rename(s, "C_" + newAssetName + zero_padding + str(end_number) + "_GEO")
            end_number -= 1




#get directory
def getPathtoAssetectory():
    PathtoAssetectory = mc.fileDialog2(fm = 3, cap = 'Select New Directory', okc = 'Select')
    mc.textField('directoryTextField', e = True, tx = PathtoAssetectory[0])




#directory error check
def Directory_check(self):
    if len(self) > 0:
        print "Directory looks alright!"
    else:
        OpenMaya.MGlobal.displayError("Warning: Select directory!") 
        sys.exit()
  


#group name error check
def Group_name_check(self):
    if len(self) > 0:
        print "Group name looks nice!"
    else:
        OpenMaya.MGlobal.displayError("Warning: Group name required!") 
        sys.exit()



#group name error check
def Group_name_duplicated(self):
    findDuplicatedName = mc.ls("*:"+ self )
    if len(findDuplicatedName)  == 0:
        print "no duplicated group name!"
    else:
        OpenMaya.MGlobal.displayError("Warning: Asset group name is already used in!") 
        sys.exit()



#Run
createUI()
