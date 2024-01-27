# -*- coding: utf-8 -*-

import mod.client.extraClientApi as clientApi

ClientSystem = clientApi.GetClientSystemCls()

class tpaUICS(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)

        self.ui_list = {}
        self.ListenForOriginEvents()
        self.ListenForCustomEvents()

    def ListenForOriginEvents(self):
        events = {
            'UiInitFinished': self.UiInitFinished
        }

        for eventName in events:
            self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), eventName, self,
                                events[eventName])

    def ListenForCustomEvents(self):
        events = {
            'tpaUI': ['tpaUISS', 'OpenTpaUI', self.OpenTpaUI],
            'UpdatePlayerList': ['tpaUI', 'UpdatePlayerList', self.UpdatePlayerList]
        }

        for namespace in events:
            self.ListenForEvent(namespace, events[namespace][0], events[namespace][1], self,
                                events[namespace][2])

    # UI初始化事件
    def UiInitFinished(self, data):
        # 注册tpaUI           mod名字    UI短名  UI的脚本文件类路径                   画布路径(ui的json文件名字.画布名字)你的画布被我改名为tpaUI了
        clientApi.RegisterUI('tpaUI', 'tpaUI', 'tpaUI.uiScript.tpaUISN.tpaUISN', 'tpaUI.tpaUI')
        clientApi.RegisterUI('tpaUI', 'tpaplayerUI', 'tpaUI.uiScript.tpaplayerUISN.tpaplayerUISN', 'tpaplayerUI.main')

        # 这一串代码是测试用的 ui初始化完毕后直接createui创建ui给玩家看       isHud是1代表ui打开的同时可以移动，0则相反
        self.ui_list['tpaUI'] = clientApi.CreateUI('tpaUI', 'tpaUI', {'isHud': 1})
        self.ui_list['tpaplayerUI'] = clientApi.CreateUI('tpaUI', 'tpaplayerUI', {'isHud': 1})
        # 隐藏ui画布
        self.ui_list['tpaUI'].SetScreenVisible(False)
        self.ui_list['tpaplayerUI'].setScreenVisible(False)

    # 服务端通知你打开tpaUI事件
    def OpenTpaUI(self, data):
        # 显示ui画布
        self.ui_list['tpaUI'].SetScreenVisible(True)

    def OpenTpaplayerUI(self, data):
        self.ui_list['tpaplayerUI'].SetScreenVisible(True)

    # 监听引擎OnScriptTickClient事件，引擎会执行该tick回调，1秒钟30帧
    def OnTickClient(self):
        """
        Driven by event, One tick way
        """
        pass

    # 被引擎直接执行的父类的重写函数，引擎会执行该Update回调，1秒钟30帧
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
