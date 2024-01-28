# -*- coding: utf-8 -*-

import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()


class tpaUISS(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenForOriginEvents()
        self.ListenForCustomEvents()

    def ListenForOriginEvents(self):
        events = {
            'ServerChatEvent': self.ServerChatEvent
        }

        for eventName in events:
            self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), eventName, self,
                                events[eventName])

    def ListenForCustomEvents(self):
        events = [
            {'tpaUI': ['tpaUICS', 'RequestPlayerList', self.RequestPlayerList]},
        ]
        for event_dict in events:
            for namespace, info in event_dict.items():
                self.ListenForEvent(namespace, info[0], info[1], self,
                                    info[2])

    def RequestPlayerList(self, data):
        playerList = []
        for playerId in serverApi.GetPlayerList():
            playerList.append(serverApi.GetEngineCompFactory().CreateName(playerId).GetName())

        self.NotifyToClient(data['__id__'], 'UpdatePlayerList', {'playerList': playerList})

    def ServerChatEvent(self, data):
        message = data['message']
        playerId = data['playerId']
        if message == '打开tpaUI':
            self.NotifyToClient(playerId, 'OpenTpaUI', {})

    # OnScriptTickServer的回调函数，会在引擎tick的时候调用，1秒30帧（被调用30次）
    def OnTickServer(self):
        """
        Driven by event, One tick way
        """
        pass

    # 这个Update函数是基类的方法，同样会在引擎tick的时候被调用，1秒30帧（被调用30次）
    def Update(self):
        """
        Driven by system manager, Two tick way
        """
        pass

    def Destroy(self):
        pass
