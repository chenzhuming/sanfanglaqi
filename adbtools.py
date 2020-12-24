import wx
import subprocess
import re
import readJson
from ConfigIni import ConfigIni

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

        self.packageNameTxt = wx.StaticText(self, label="包名: ")
        grid.Add(self.packageNameTxt, pos=(1, 0), flag=wx.ALIGN_RIGHT)
        self.packageName = wx.TextCtrl(self, value=ConfigIni("self.ini").read("android", "packagename"))
        grid.Add(self.packageName, pos=(1, 1), span=(1, 3), flag=wx.EXPAND)

        self.classNameTxt = wx.StaticText(self, label="类名: ")
        grid.Add(self.classNameTxt, pos=(2, 0), flag=wx.ALIGN_RIGHT)
        self.className = wx.TextCtrl(
            self, value=ConfigIni("self.ini").read("android", "classname"))
        grid.Add(self.className, pos=(2, 1), flag=wx.EXPAND, span=(1, 3))

        # 加载控件
        curosr = 0
        self.json_data = readJson.readconfig()
        data_keys = self.json_data.keys()
        self.lables = {}
        self.controls = {}
        # print(data_keys)
        for data_key in data_keys:
            self.lables[data_key] = wx.StaticText(self, label=data_key+":")
            grid.Add(self.lables[data_key], pos=(
                curosr/4+3, curosr % 4), flag=wx.ALIGN_RIGHT)
            curosr = curosr+1
            self.controls[data_key] = wx.ComboBox(self, size=(
                95, -1), choices=list(self.json_data[data_key]), style=wx.CB_DROPDOWN)
            grid.Add(self.controls[data_key], pos=(
                curosr/4+3, curosr % 4), flag=wx.EXPAND)
            curosr = curosr+1
        # 日志输入
        self.logger = wx.TextCtrl(self, size=(
            400, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        grid.Add(self.logger, pos=(curosr/4+4, 0), span=(1, 4), flag=wx.EXPAND)
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
        cmd=''
        for control_key in self.controls.keys():
            control_value =self.controls[control_key].GetValue()
            # 判断控件是否输入了
            if control_value is '':
                continue
            # 如果是数字则是自定义的值，不是从json获取的
            if control_value.isdigit():
                cmd += ",'"+control_key+"' : '" + control_value + "'"
            else:
                cmd += ",'"+control_key+"' : '" + self.json_data[control_key][control_value] + "'"
        if 'showType' not in cmd:
            dlg = wx.MessageDialog(self, "showType为必填项", "error", wx.OK)
            dlg.ShowModal()  # Show it
            dlg.Destroy()  # finally destroy it when finished.
            return
        cmd = "{"+cmd[1:]+"}"

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
Config_Ini=ConfigIni("self.ini")
pos = (int(Config_Ini.read("pos", "x")), int(Config_Ini.read("pos", "y")))
size = (int(Config_Ini.read("size", "x")), int(Config_Ini.read("size", "y")))
# frame = wx.Frame(None, pos=(200,20), size=(600,600))
frame = wx.Frame(None, pos=pos, size=size)
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()