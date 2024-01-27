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

    def Create(self):
        """
        @description UI创建成功时调用
        """
        # 你这个什么b路径 我劝你后续自己改
        self.controls['edit_box'] = self.GetBaseUIControl('/panel/image/edit_box').asTextEditBox()
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

    def onOpenComboBoxCallback(self):
        name = self.controls['edit_box'].GetEditText()
        '''
        这里模拟一个玩家列表，具体需要你服务端传给客户端，也可以在这里打开的回调函数 发送申请，然后服务端收到 返回给你客户端，然后在返回接到的事件里再创建选项
        （不过没什么必要啊，每次玩家打开这个ui的时候请求一次就行了（不过你不是pushscreen create只有在初始化 createui的时候执行一次，所以看你自己咯）
        '''
        players = ['亦染', '雪紫', '野兽先辈', '李田所', '我修院']
        for playerName in players:
            if name in playerName:  # 不知道这个AddOption用法 就去文档找
                success = self.controls['selections'].AddOption(playerName, None,
                                                                {"playerName": playerName})

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
