# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()

class tpaplayerUISN(ScreenNode):
    def __int__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.client_system = clientApi.GetSystem('tpaUI', 'tpaUICS')
        self.controls = {}

    def Create(self):
        self.controls