# -*- coding: utf-8 -*-

from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi

@Mod.Binding(name="tpaUI", version="0.0.1")
class tpaUI(object):

    def __init__(self):
        pass

    @Mod.InitServer()
    def tpaUIServerInit(self):
        serverApi.RegisterSystem('tpaUI', 'tpaUISS', 'tpaUI.tpaUISS.tpaUISS')
        pass

    @Mod.DestroyServer()
    def tpaUIServerDestroy(self):
        pass

    @Mod.InitClient()
    def tpaUIClientInit(self):
        clientApi.RegisterSystem('tpaUI', 'tpaUICS', 'tpaUI.tpaUICS.tpaUICS')
        pass

    @Mod.DestroyClient()
    def tpaUIClientDestroy(self):
        pass
