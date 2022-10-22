import wx
import matplotlib.pyplot as plt
import wx.lib.buttons as lib_button
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

# 翻译功能
from translate import translate

# 识别功能
from PIL import Image
import pytesseract

# 一键生成词云
from wordscloud import wordcloud_show

# 截图功能
from screenshot import CaptureScreen

# 为解决pyQt的初始化DPI问题（会导致窗口大小比例错位），此处引入函数获取DPI。并在后面的设置的参数中乘上这个比例来使得界面比例保持正常
from get_dpi import get_scaling

'''创建GUI程序'''

class Frame(wx.Frame):
    def __init__(self):
        DPI = get_scaling()
        self.imapp = QApplication(sys.argv)
        wx.Frame.__init__(self, None, title = '截图翻译', size = (DPI*854, DPI*580), name = 'frame')
        self.window = wx.Panel(self)
        self.Center()
        # 更改界面图标
        self.icno = wx.Icon(name=".\\icon\\App.ico",type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icno)

        # 创建box1作为输入框
        self.box1 = wx.TextCtrl(self.window, size=(DPI*473, DPI*164), pos=(DPI*54, DPI*131),value='',name='text',style = wx.TE_MULTILINE|wx.TE_WORDWRAP)
        self.box1.SetFont(wx.Font(12,74,90,400, False,'Microsoft YaHei UI',33))
        self.box1.SetOwnBackgroundColour((242, 244, 249, 255))
        
        # 创建选择框来更改语言
        self.changes = wx.ComboBox(self.window,value='',pos=(DPI*237, DPI*65),name='comboBox',choices=['汉语', 'English', '日本語', 'français', ''],style=16)
        self.changes.SetSize((DPI*99, DPI*35))
        self.changes.SetFont(wx.Font(10,74,90,700, False, 'Microsoft YaHei UI',33))
        self.changes.SetForegroundColour((0, 128, 255, 255))
        self.changes.Bind(wx.EVT_COMBOBOX, self.change)

        # 创建button1作为翻译按钮
        image_button1 = wx.Image(".\\icon\\translate.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button1 = lib_button.ThemedGenBitmapTextButton(self.window, bitmap = image_button1, pos=(DPI*107, DPI*52),size=(DPI*84, DPI*51),label= '翻译', name='翻译')
        self.button1.Bind(wx.EVT_BUTTON,self.click1)
        self.button1.SetFont(wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28).Bold())
        self.button1.SetOwnBackgroundColour((218, 227, 243, 255))

        # 创建label1作为结果显示框
        self.label1 = wx.TextCtrl(self.window, size=(DPI*473, DPI*164), pos=(DPI*54, DPI*306), value = '结果', name='staticText',style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_WORDWRAP)
        self.label1.SetFont(wx.Font(12,74,90,400,False,'Microsoft YaHei UI',33))
        self.label1.SetOwnBackgroundColour((242, 244, 249, 255))

        # 创建button2作为清空按钮
        image_button2 = wx.Image(".\\icon\\clear.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button2 =lib_button.ThemedGenBitmapTextButton(self.window, bitmap= image_button2, size = (DPI*84, DPI*51), pos = (DPI*385, DPI*52),label = '清除',name = 'button')
        self.button2.Bind(wx.EVT_BUTTON,self.click2)
        self.button2.SetFont(wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28).Bold())
        self.button2.SetOwnBackgroundColour((218, 227, 243, 255))

        
        # 创建标准文件对话框选择图片
        self.dlg = wx.FileDialog(self.window, message = "选择图片", defaultDir = ".", defaultFile = "", wildcard = "图片|*.png;*.jpg;*.bmp", style = wx.FD_OPEN)
        self.dlg2 = wx.FileDialog(self.window, message = "选择图片", defaultDir = ".", defaultFile = "云.jpg", wildcard = "图片|*.png;*.jpg;*.bmp", style = wx.FD_OPEN)

        # 创建button3开始选择图片
        image_button3 = wx.Image(".\\icon\\upload.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button3 = wx.BitmapButton(self.window, size=(DPI*29, DPI*23), pos=(DPI*535, DPI*311), bitmap = image_button3, name = 'button')
        self.button3.Bind(wx.EVT_BUTTON,self.click3)

        # 创建label2作为需识别图片的地址显示框
        self.label2 = wx.TextCtrl(self.window, size=(DPI*226, DPI*26), pos=(DPI*578, DPI*309), name = 'ImageAddress')
        self.label2.SetFont(wx.Font(6,74,90,400,False,'Microsoft YaHei UI',28))

        # 创建label3作为词云底图地址显示框
        self.label3 = wx.TextCtrl(self.window, size=(DPI*226, DPI*26), pos=(DPI*578, DPI*450), name = 'ImageAddress')
        self.label3.SetFont(wx.Font(6,74,90,400,False,'Microsoft YaHei UI',28))

        
        # 创建button4进行图片识别
        image_button4 = wx.Image(".\\icon\\ocr.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button4 = lib_button.ThemedGenBitmapTextButton(self.window, bitmap= image_button4, size=(DPI*84, DPI*51),pos=(DPI*578, DPI*242), label = '识别', name = 'button')
        self.button4.Bind(wx.EVT_BUTTON,self.click4)
        self.button4.SetFont(wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28).Bold())
        self.button4.SetOwnBackgroundColour((218, 227, 243, 255))

        # 创建button5进行截图
        image_button5 = wx.Image(".\\icon\\screenshot.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button5 = lib_button.ThemedGenBitmapTextButton(self.window, bitmap= image_button5, size=(DPI*84, DPI*51),pos=(DPI*578, DPI*149), label = '截图', name = 'button')
        self.button5.Bind(wx.EVT_BUTTON,self.click5)
        self.button5.SetFont(wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28).Bold())
        self.button5.SetOwnBackgroundColour((218, 227, 243, 255))

        # 创建按钮6生成词云
        image_button6 = wx.Image(".\\icon\\wordcloud.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button6 = lib_button.ThemedGenBitmapTextButton(self.window, bitmap= image_button6, size=(DPI*84, DPI*51),pos=(DPI*578, DPI*383), label = '词云', name = 'button')
        self.button6.Bind(wx.EVT_BUTTON,self.click6)
        self.button6.SetFont(wx.Font(14,74,90,700,False,'Microsoft YaHei UI',28).Bold())
        self.button6.SetOwnBackgroundColour((218, 227, 243, 255))

        # 创建按钮7选择词云底图
        image_button3 = wx.Image(".\\icon\\upload.ico", wx.BITMAP_TYPE_ICO).ConvertToBitmap()
        self.button3 = wx.BitmapButton(self.window, size=(DPI*29, DPI*23), pos=(DPI*535, DPI*450), bitmap = image_button3, name = 'button')
        self.button3.Bind(wx.EVT_BUTTON,self.click7)


    # 翻译按钮点击事件   
    def click1(self,event):
        text = self.box1.GetValue()
        self.change(event)
        self.label1.SetValue(translate(text, "auto", to_lang))
        self.box1.SetFocus()
        
    # 清除按钮点击事件   
    def click2(self, event):
        self.box1.SetValue('')
        self.label1.SetValue('结果')
        self.box1.SetFocus()
        img_path = ''
        self.label2.SetValue('')
        self.label3.SetValue('')

    # 选择需识别图片选择按钮点击事件
    def click3(self, event):
        if self.dlg.ShowModal() == wx.ID_OK:
            self.path = self.dlg.GetPath()
            global img_path
            img_path = self.path
            self.label2.SetValue('路径：%s'%img_path)
            self.box1.SetFocus()
        

    # 识别按钮点击事件
    def click4(self, event):
        global img_path
        try:
            if img_path == '':
                self.box1.SetValue('请先选择图片，再进行识别')
            else:
                self.box1.SetValue(pytesseract.image_to_string(Image.open(img_path)))
        except:
            self.box1.SetValue('路径失效，请重新选择图片') 

    # 截图按钮点击事件
    def click5(self, event):
        global img_path
        windows = CaptureScreen()
        windows.show()
        self.imapp.exec_()
        img_path = windows.im_path
        self.label2.SetValue('路径：%s'%img_path)
        windows.destroy()
        self.imapp.quit()
        
        
    # 词云按钮点击事件
    def click6(self, event):
        text = self.box1.GetValue()
        wordcloud_show(text, color_mask_path)

    # ‘词云底图选择’按钮点击事件
    def click7(self, event):
        if self.dlg2.ShowModal() == wx.ID_OK:
            self.path = self.dlg2.GetPath()
            global color_mask_path
            color_mask_path = self.path
            self.label3.SetValue('路径：%s'%color_mask_path)
            self.box1.SetFocus()

    
    # 选择框改变事件（选择要翻译为的语言）
    def change(self, event):
        global to_lang 
        if self.changes.GetValue() == '汉语':
            to_lang = 'zh-CN'
        elif self.changes.GetValue() == 'English':
            to_lang = 'en'
        elif self.changes.GetValue() == '日本語':
            to_lang = 'ja'
        elif self.changes.GetValue() == 'français':
            to_lang = 'fr'
        else:
            to_lang = 'zh-CN'
        
# 运行GUI
class myApp(wx.App):
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
    




