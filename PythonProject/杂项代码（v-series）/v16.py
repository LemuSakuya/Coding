# #1
# import wx

# class SimpleFrame(wx.Frame):
#     def __init__(self, parent, title):
#         super(SimpleFrame, self).__init__(parent, title=title, size=(350, 200))

#         panel = wx.Panel(self)

#         vbox = wx.BoxSizer(wx.VERTICAL)

#         self.text_input = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
#         vbox.Add(self.text_input, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)

#         self.checkbox = wx.CheckBox(panel, label="启用功能")
#         vbox.Add(self.checkbox, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

#         self.button = wx.Button(panel, label="提交")
#         self.button.Bind(wx.EVT_BUTTON, self.solve)
#         vbox.Add(self.button, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

#         panel.SetSizer(vbox)

#         self.Centre()
#         self.Show()
    
#     def solve(self, event):
#         text_value = self.text_input.GetValue()
#         is_checked = self.checkbox.GetValue()
        
#         message = f"您输入的内容是: {text_value}\n"
#         message += f"复选框状态: {'已启用' if is_checked else '未启用'}"
        
#         wx.MessageBox(message, "提交结果", wx.OK | wx.ICON_INFORMATION)

# class MyApp(wx.App):
#     def OnInit(self):
#         frame = SimpleFrame(None, "简单GUI示例")
#         return True

# if __name__ == "__main__":
#     app = MyApp()
#     app.MainLoop()

# 2
# import wx

# class SizerFrame(wx.Frame):
#     def __init__(self, parent, title):
#         super(SizerFrame, self).__init__(parent, title=title, size=(300, 200))
        
#         panel = wx.Panel(self)
#         vbox = wx.BoxSizer(wx.VERTICAL)
#         self.text1 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
#         vbox.Add(self.text1, flag=wx.EXPAND|wx.ALL, border=10, proportion=1)
#         self.text2 = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
#         vbox.Add(self.text2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10, proportion=1)
#         panel.SetSizer(vbox)
        
#         self.Centre()
#         self.Show()

# class MyApp(wx.App):
#     def OnInit(self):
#         frame = SizerFrame(None, "垂直文本框")
#         return True

# if __name__ == "__main__":
#     app = MyApp()
#     app.MainLoop()

# #3
# import wx

# class EventExample(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title="事件处理示例", size=(300, 200))
#         self.panel = wx.Panel(self)

#         self.button = wx.Button(self.panel, label="me")
#         self.counter = 0

#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(self.button, proportion=1, flag=wx.EXPAND|wx.ALL, border=50)
#         self.panel.SetSizer(sizer)

#         self.button.Bind(wx.EVT_BUTTON, self.on_button_click)
        
#         self.Centre()
#         self.Show()
    
#     def on_button_click(self, event):
#         self.counter += 1
#         print(f"pushed {self.counter} ")
#         self.SetTitle(f"num: {self.counter}")
#         self.button.SetLabel(f"click ({self.counter})")

# if __name__ == "__main__":
#     app = wx.App()
#     frame = EventExample()
#     app.MainLoop()

# #4
# import wx

# class StudentManager(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title="一个app...", size=(600, 400))
#         self.students = {}
#         self.panel = wx.Panel(self)
#         self.create_controls()
#         self.setup_layout()
#         self.Centre()
#         self.Show()
    
#     def create_controls(self):
#         self.sid_input = wx.TextCtrl(self.panel)
#         self.name_input = wx.TextCtrl(self.panel)
#         self.score_input = wx.TextCtrl(self.panel)

#         self.add_btn = wx.Button(self.panel, label="add")
#         self.query_btn = wx.Button(self.panel, label="check")
#         self.del_btn = wx.Button(self.panel, label="delete")

#         self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT)
#         self.list_ctrl.InsertColumn(0, "学号", width=100)
#         self.list_ctrl.InsertColumn(1, "姓名", width=100)
#         self.list_ctrl.InsertColumn(2, "成绩", width=100)

#         self.add_btn.Bind(wx.EVT_BUTTON, self.on_add)
#         self.query_btn.Bind(wx.EVT_BUTTON, self.on_query)
#         self.del_btn.Bind(wx.EVT_BUTTON, self.on_delete)
    
#     def setup_layout(self):
#         main_sizer = wx.BoxSizer(wx.VERTICAL)

#         form_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
#         form_sizer.Add(wx.StaticText(self.panel, label="学号:"), flag=wx.ALIGN_CENTER_VERTICAL)
#         form_sizer.Add(self.sid_input, flag=wx.EXPAND)
#         form_sizer.Add(wx.StaticText(self.panel, label="姓名:"), flag=wx.ALIGN_CENTER_VERTICAL)
#         form_sizer.Add(self.name_input, flag=wx.EXPAND)
#         form_sizer.Add(wx.StaticText(self.panel, label="成绩:"), flag=wx.ALIGN_CENTER_VERTICAL)
#         form_sizer.Add(self.score_input, flag=wx.EXPAND)
#         form_sizer.AddGrowableCol(1, 1)

#         btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
#         btn_sizer.Add(self.add_btn, proportion=1, flag=wx.RIGHT, border=5)
#         btn_sizer.Add(self.query_btn, proportion=1, flag=wx.RIGHT, border=5)
#         btn_sizer.Add(self.del_btn, proportion=1, flag=wx.RIGHT, border=5)

#         main_sizer.Add(form_sizer, flag=wx.EXPAND|wx.ALL, border=10)
#         main_sizer.Add(btn_sizer, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
#         main_sizer.Add(self.list_ctrl, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10, proportion=1)
        
#         self.panel.SetSizer(main_sizer)

#     def on_add(self, event):
#         sid = self.sid_input.GetValue().strip()
#         name = self.name_input.GetValue().strip()
#         score = self.score_input.GetValue().strip()

#         if not all([sid, name, score]):
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
#             return
        
#         if not score.isdigit():
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
#             return
        
#         if sid in self.students:
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
#             return

#         self.students[sid] = {"name": name, "score": int(score)}
#         self.update_list()
#         self.clear_inputs()
#         wx.MessageBox("Y", wx.OK|wx.ICON_INFORMATION)
    
#     def on_query(self, event):
#         sid = self.sid_input.GetValue().strip()
        
#         if not sid:
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
#             return
        
#         if sid in self.students:
#             student = self.students[sid]
#             wx.MessageBox(
#                 f"学号: {sid}\n姓名: {student['name']}\n成绩: {student['score']}", 
#                 "result", 
#                 wx.OK|wx.ICON_INFORMATION
#             )
#         else:
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
    
#     def on_delete(self, event):
#         sid = self.sid_input.GetValue().strip()
        
#         if not sid:
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
#             return
        
#         if sid in self.students:
#             del self.students[sid]
#             self.update_list()
#             wx.MessageBox("Y", wx.OK|wx.ICON_INFORMATION)
#         else:
#             wx.MessageBox("E", wx.OK|wx.ICON_ERROR)
    
#     def on_clear(self, event):
#         dlg = wx.MessageDialog(
#             self, 
#             wx.YES_NO|wx.ICON_WARNING
#         )
        
#         if dlg.ShowModal() == wx.ID_YES:
#             self.students.clear()
#             self.update_list()
#             wx.MessageBox("CLR", wx.OK|wx.ICON_INFORMATION)
#         dlg.Destroy()

#     def update_list(self):
#         self.list_ctrl.DeleteAllItems()
#         for idx, (sid, info) in enumerate(self.students.items()):
#             self.list_ctrl.InsertItem(idx, sid)
#             self.list_ctrl.SetItem(idx, 1, info["name"])
#             self.list_ctrl.SetItem(idx, 2, str(info["score"]))

# if __name__ == "__main__":
#     app = wx.App()
#     frame = StudentManager()
#     app.MainLoop()