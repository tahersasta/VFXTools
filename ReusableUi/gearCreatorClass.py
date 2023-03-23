from maya import cmds

class Gear(object):
    """
    This is a gear object that lets us create and modify a gear 
    """
    def __init__(self):
        self.extrude = None
        self.transform =None
        self.constructor = None


    def createGear(self,teeth=10, length=0.3):
        """
        This function will create a gear with the given parameters
        :param teeth: The number of teeth
        :param length: The length of the teeth
        :return: A tuple of the transform , constructor and extrude node

        """

        # Teeth are every alternate face
        spans = teeth * 2

        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)

        sideFaces = range(spans * 2, spans * 3, 2)

        cmds.select(clear=True)

        for face in sideFaces:
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(localTranslateZ=length)[0]


    def changeTeeth(self,teeth=10, length=0.3):
         """
        This function will edit the number of teeth
        :param teeth: The number of teeth
        :param length: The length of the teeth
        :return:None
        """
        spans = teeth * 2
        cmds.polyPipe(self.constructor, edit=True,
                      subdivisionsAxis=spans)
        sideFaces = range(spans * 2, spans * 3, 2)
        faceN = []

        for face in sideFaces:
            faceName = 'f[%s]' % (face)
            faceN.append(faceName)

        cmds.setAttr("%s.inputComponents" % (self.extrude),
                     len(faceN),
                     *faceN, type="componentList")

        cmds.polyExtrudeFacet(self.extrude, edit=True, ltz=length)
