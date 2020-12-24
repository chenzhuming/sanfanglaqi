import wx
import subprocess
import re


class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid = wx.GridBagSizer(hgap=10, vgap=4)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ipTxt = wx.StaticText(self, label="IP: ")
        grid.Add(self.ipTxt, pos=(0, 0), flag=wx.ALIGN_RIGHT)

        self.ip = wx.TextCtrl(self)
        grid.Add(self.ip, pos=(0, 1), flag=wx.ALIGN_BOTTOM |
                 wx.EXPAND)

        self.button = wx.Button(self, label="连接")
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        grid.Add(self.button, pos=(0, 2), flag=wx.EXPAND)

        self.send = wx.Button(self, label="发送")
        self.Bind(wx.EVT_BUTTON, self.OnClickSend, self.send)
        grid.Add(self.send, pos=(0, 3), flag=wx.EXPAND)

        # self.version = wx.Button(self, label="version")
        # self.Bind(wx.EVT_BUTTON, self.OnClickVersion, self.version)
        # grid.Add(self.version, pos=(7, 3), flag=wx.EXPAND)

        self.showType = wx.StaticText(self, label="showType: ")
        grid.Add(self.showType, pos=(1, 0), flag=wx.ALIGN_RIGHT)

        self.showTypeDict = {'跳转至首页': '0', '跳转至二级栏目': '1', '跳转至电影详情页': '2',
                             '跳转至的剧集详情页': '3', '跳转至的搜索页': '4', '历史': '5', '会员中心': '6', '收藏': '7'}

        self.sampleList = list(self.showTypeDict.keys())
        self.showTypeComboBox = wx.ComboBox(self, size=(
            95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        grid.Add(self.showTypeComboBox, pos=(1, 1), flag=wx.EXPAND)

        self.categoryId = wx.StaticText(self, label="categoryId: ")
        grid.Add(self.categoryId, pos=(1, 2), flag=wx.ALIGN_RIGHT)

        self.categoryIdText = wx.TextCtrl(self)
        grid.Add(self.categoryIdText, pos=(1, 3), flag=wx.EXPAND)

        self.howBack = wx.StaticText(self, label="howBack: ")
        grid.Add(self.howBack, pos=(2, 0), flag=wx.ALIGN_RIGHT)

        self.howbackDict = {'层层退出': '0', '直接退出': '1'}
        self.howbackList = list(self.howbackDict.keys())
        self.howBackComboBox = wx.ComboBox(self, size=(
            95, -1), choices=self.howbackList, style=wx.CB_DROPDOWN)
        grid.Add(self.howBackComboBox, pos=(2, 1), flag=wx.EXPAND)

        self.contentId = wx.StaticText(self, label="contentId: ")
        grid.Add(self.contentId, pos=(2, 2), flag=wx.ALIGN_RIGHT)

        self.contentIdText = wx.TextCtrl(self)
        grid.Add(self.contentIdText, pos=(2, 3), flag=wx.EXPAND)

        self.isFromIqy = wx.StaticText(self, label="isFromIqy: ")
        grid.Add(self.isFromIqy, pos=(3, 0), flag=wx.ALIGN_RIGHT)
        self.isFromIqyDict = {'否': '0', '是': '1'}
        self.isFromIqyList = list(self.isFromIqyDict.keys())
        self.isFromIqyComboBox = wx.ComboBox(self, size=(
            95, -1), choices=self.isFromIqyList, style=wx.CB_DROPDOWN)
        grid.Add(self.isFromIqyComboBox, pos=(3, 1), flag=wx.EXPAND)
        self.parentCategoryId = wx.StaticText(self, label="parentCategoryId: ")
        grid.Add(self.parentCategoryId, pos=(3, 2), flag=wx.ALIGN_RIGHT)
        self.parentCategoryIdText = wx.TextCtrl(self)
        grid.Add(self.parentCategoryIdText, pos=(3, 3), flag=wx.EXPAND)

        self.contentIqyType = wx.StaticText(self, label="contentIqyType: ")
        grid.Add(self.contentIqyType, pos=(4, 0), flag=wx.ALIGN_RIGHT)
        self.contentIqyTypeDict = {'否': '0', '是': '1'}
        self.contentIqyTypeList = list(self.contentIqyTypeDict.keys())
        self.contentIqyTypeComboBox = wx.ComboBox(self, size=(
            95, -1), choices=self.contentIqyTypeList, style=wx.CB_DROPDOWN)
        grid.Add(self.contentIqyTypeComboBox, pos=(4, 1), flag=wx.EXPAND)
        self.packageId = wx.StaticText(self, label="packageId: ")
        grid.Add(self.packageId, pos=(4, 2), flag=wx.ALIGN_RIGHT)
        self.packageIdText = wx.TextCtrl(self)
        grid.Add(self.packageIdText, pos=(4, 3), flag=wx.EXPAND)

        self.packageNameTxt = wx.StaticText(self, label="包名: ")
        grid.Add(self.packageNameTxt, pos=(5, 0), flag=wx.ALIGN_RIGHT)
        self.packageName = wx.TextCtrl(self, value='com.huawei.video4k')
        grid.Add(self.packageName, pos=(5, 1), span=(1, 3), flag=wx.EXPAND)

        self.classNameTxt = wx.StaticText(self, label="类名: ")
        grid.Add(self.classNameTxt, pos=(6, 0), flag=wx.ALIGN_RIGHT)
        self.className = wx.TextCtrl(
            self, value='com.huawei.video4k.activity.HomeActivity')
        grid.Add(self.className, pos=(6, 1), flag=wx.EXPAND, span=(1, 3))

        self.appIdTypeTxt = wx.StaticText(self, label="appIdType: ")
        grid.Add(self.appIdTypeTxt, pos=(7, 0), flag=wx.ALIGN_RIGHT)
        self.appIdType = wx.TextCtrl(self)
        grid.Add(self.appIdType, pos=(7, 1), flag=wx.EXPAND)

        self.logger = wx.TextCtrl(self, size=(
            400, 400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        grid.Add(self.logger, pos=(8, 0), span=(1, 4), flag=wx.EXPAND)

        hSizer.Add(grid, 0, wx.ALL, 5)
        # hSizer.Add(self.logger)
        mainSizer.Add(hSizer, 0, wx.ALL, 5)
        # mainSizer.Add(self.button, 0, wx.CENTER)
        self.SetSizerAndFit(mainSizer)

    def OnClick(self, event):
        match = re.match(
            r'(2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2}', self.ip.GetValue())
        if match:
            cmd = 'adb connect ' + self.ip.GetValue()
            self.cmdHelp(cmd)
        else:
            dlg = wx.MessageDialog(self, "请输入正确ip地址", "ip error", wx.OK)
            dlg.ShowModal()  # Show it
            dlg.Destroy()  # finally destroy it when finished.

    def OnClickVersion(self, event):
        self.cmdHelp('adb version')

    def OnClickSend(self, event):
        cmd = ''
        showType = self.showTypeComboBox.GetValue()
        if len(showType) == 0:
            dlg = wx.MessageDialog(self, "showType为必填项", "error", wx.OK)
            dlg.ShowModal()  # Show it
            dlg.Destroy()  # finally destroy it when finished.
            return
        if showType in self.showTypeDict.keys():
            showType = self.showTypeDict[showType]
        cmd = "{'showType' :'" + showType + "'"
        categoryId = self.categoryIdText.GetValue().strip()
        if len(categoryId) > 0:
            cmd += ",'categoryId' : '" + categoryId + "'"
        howBack = self.howBackComboBox.GetValue()
        if len(howBack) > 0:
            if howBack in self.howbackDict.keys():
                howBack = self.howbackDict[howBack]
            cmd += ",'howBack' :'" + howBack + "'"
        contentId = self.contentIdText.GetValue().strip()
        if len(contentId) > 0:
            cmd += ",'contentId' :'" + contentId + "'"
        isFromIqy = self.isFromIqyComboBox.GetValue()
        if len(isFromIqy) > 0:
            if isFromIqy in self.isFromIqyDict.keys():
                isFromIqy = self.isFromIqyDict[isFromIqy]
            cmd += ",'isFromIqy' :'" + isFromIqy + "'"
        packageId = self.packageIdText.GetValue().strip()
        if len(packageId) > 0:
            cmd += ",'packageId' :'" + packageId + "'"
        contentIqyType = self.contentIqyTypeComboBox.GetValue()
        if len(contentIqyType) > 0:
            if contentIqyType in self.contentIqyTypeDict.keys():
                contentIqyType = self.contentIqyTypeDict[contentIqyType]
            cmd += ",'contentIqyType' :'" + contentIqyType + "'"
        appIdType = self.appIdType.GetValue().strip()
        if len(appIdType) > 0:
            cmd += ",'appIdType' :'" + appIdType + "'"
        cmd += "}"
        cmd = r"adb shell am start -n " + self.packageName.GetValue().strip() + \
            "/" + self.className.GetValue().strip() + r" --es data '" + cmd + r"'"
        self.cmdHelp(cmd)

    def cmdHelp(self, cmd):
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        self.logger.AppendText('>>>%s\n' % cmd)
        return_code = p.poll()
        while return_code is None:
            line = p.stdout.readline()
            return_code = p.poll()
            line = line.strip()
            if line:
                self.logger.AppendText('<<<%s\n' % line)


app = wx.App(False)
frame = wx.Frame(None, pos=(500, 200), size=(510, 700))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()
