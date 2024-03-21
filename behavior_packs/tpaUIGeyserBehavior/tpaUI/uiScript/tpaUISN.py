# -*- coding: utf-8 -*-
import mod.client.extraClientApi as clientApi

ViewBinder = clientApi.GetViewBinderCls()
ViewRequest = clientApi.GetViewViewRequestCls()
ScreenNode = clientApi.GetScreenNodeCls()


class tpaUISN(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        # 获取客户端脚本实例
        self.client_system = clientApi.GetSystem('tpaUI', 'tpaUICS')

        self.controls = {}

        self.ListenForCustomEvents()

    def ListenForCustomEvents(self):

        # namespace
        events = {'tpaUI': [
            # system_name event_name   class(就是你callback这个方法 在哪个类实例，你得给)     callback
            ['tpaUISS', 'UpdatePlayerList', self, self.UpdatePlayerList]
        ]
        }
        for namespace, info in events.items():
            for system_name, event_name, cls, callback in info:
                self.client_system.ListenForEvent(namespace, system_name, event_name, cls,
                                                  callback)

    def Create(self):
        """
        @description UI创建成功时调用
        """
        # 你这个什么b路径 我劝你后续自己改
        self.controls['edit_box'] = self.GetBaseUIControl('/panel/image/edit_box').asTextEditBox()

        tpa_button = self.GetBaseUIControl('/panel/image/button').asButton()
        tpa_button.AddTouchEventParams({"isSwallow": True})
        tpa_button.SetButtonTouchUpCallback(self.onTpaButtonClicked)

        close_button = self.GetBaseUIControl('/panel/image/button(1)').asButton()
        close_button.AddTouchEventParams({"isSwallow": True})
        close_button.SetButtonTouchUpCallback(self.onCloseButtonClicked)

        self.controls['selections'] = self.GetBaseUIControl(
            '/panel/image/selections/selections').asNeteaseComboBox()

        # 注册打开快捷选择栏列表时的事件（每次打开都会检测editbox里已经输入的内容 检测当前所有玩家里有没有含有内容的玩家名字
        self.controls['selections'].RegisterOpenComboBoxCallback(self.onOpenComboBoxCallback)

        # 注册关闭快捷选择栏列表时的事件（每次关闭都会清空选项
        self.controls['selections'].RegisterCloseComboBoxCallback(self.onCloseComboBoxCallback)

        # 注册快捷栏选择某个项的时的事件（点击就把内容返回到edit_box里
        self.controls['selections'].RegisterSelectItemCallback(self.onSelectItemCallback)
        pass

    def onSelectItemCallback(self, index, showName, userData):
        if userData:
            playerName = userData['playerName']
            self.controls['edit_box'].SetEditText(playerName)
        self.onCloseComboBoxCallback()
        pass

    def onTpaButtonClicked(self, data):
        playerName = self.controls['edit_box'].GetEditText()
        self.client_system.NotifyToServer('PlayerTpaRequest', {'playerName': playerName})

    def UpdatePlayerList(self, data):
        playerList = data.get("playerList", [])
        self.controls['selections'].ClearOptions()
        for playerName in playerList:
            self.controls['selections'].AddOption(playerName, None, {"playerName": playerName})

    def onOpenComboBoxCallback(self):
        self.client_system.NotifyToServer('RequestPlayerList', {})

    def onCloseComboBoxCallback(self):
        # 移除所有选项
        i = 0
        while True:
            result = self.controls['selections'].RemoveOptionByIndex(i)
            if result:
                i += 1
            else:
                break
        pass

    def onCloseButtonClicked(self, data):
        self.SetScreenVisible(False)
        print("关闭按钮执行")

    def Destroy(self):
        """
        @description UI销毁时调用
        """
        pass

    def OnActive(self):
        """
        @description UI重新回到栈顶时调用
        """
        pass

    def OnDeactive(self):
        """
        @description 栈顶UI有其他UI入栈时调用
        """
        pass
