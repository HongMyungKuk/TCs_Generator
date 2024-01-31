import tkinter as tk
import tkinter.messagebox as msgbox
import core as CORE
from tkinter import filedialog

global g_screen_width
global g_screen_height

class GUI : 
    def __init__(self, core, width, height) :         
        self.__width = width
        self.__height = height

        self.__login_entry_width = 10
        self.__label_entry_width = 15

        self.__padding_x = 5
        self.__padding_y = 10
        
        self.__core = core

        self.__window = tk.Tk()

        # Get Screen Width, Height
        g_screen_width = self.__window.winfo_screenwidth()
        g_screen_height = self.__window.winfo_screenheight()

        # Set Window LT Position
        self.__ltPosX = g_screen_width/2 - self.__width / 2
        self.__ltPosY = g_screen_height/2 - self.__height / 2

        # Initialize
        NEWS = 'news'
        self.Init(NEWS)

        # Set Position
        x_pos = 10
        y_pos = 10 
        self.SetPosition(x_pos, y_pos)

    def Init(self, NEWS) : 
        # Init Widnow
        self.__InitWindow()
        # Init Frame
        self.__InitFrame(NEWS)
        # Init Label
        self.__InitLabel()
        # Entry
        self.__InitEntry()
        # Button
        self.__InitButton()

    def __InitWindow(self) : 
        self.__window.title("TC Generator_protoType_v0.1.0")
        self.__window.geometry(str(self.__width)+"x"+str(self.__height)+"+"+str(int(self.__ltPosX))+"+"+str(int(self.__ltPosY)))
        self.__window.resizable(False, False)

    def __InitFrame(self, NEWS) : 
        # login frame
        self.__login_frame = tk.LabelFrame(self.__window, text='Login')
        self.__login_frame.grid(row=0, column=0, sticky=NEWS)
        # Select Parameter Frame
        self.__select_param_frame = tk.LabelFrame(self.__window, text='Select Parameter')
        self.__select_param_frame.grid(row=1, column=0, sticky=NEWS)
        # Complete & Cancel Frame
        self.__cc_frame = tk.Frame(self.__window)
        self.__cc_frame.grid(row=2, column=0, sticky='e')

    def __InitLabel(self) : 
        self.__id_label = tk.Label(self.__login_frame, text='ID:')
        self.__password_label = tk.Label(self.__login_frame, text='Password:')
        self.__label_label = tk.Label(self.__select_param_frame, text='Label')
        self.__project_name_label = tk.Label(self.__select_param_frame, text='Project')

    def __InitEntry(self ) :
        self.__user_id_entry = tk.Entry(self.__login_frame, width=self.__login_entry_width)
        self.__user_password_entry = tk.Entry(self.__login_frame, width=self.__login_entry_width, show='*')
        self.__label_entry = tk.Entry(self.__select_param_frame, width= self.__label_entry_width )
        self.__project_name_entry = tk.Entry(self.__select_param_frame, width= self.__label_entry_width )

    def __InitButton(self) : 
        self.__login_button = tk.Button(self.__login_frame, text='로그인', command=self.LoginProc)
        self.__complete_button = tk.Button(self.__cc_frame, text='확인', command=self.CompleteProc)
        self.__cancel_button = tk.Button(self.__cc_frame, text='취소', command = self.CancelProc)

    def SetPosition(self, x_pos, y_pos) : 
        self.__SetLoginSectionPosition(x_pos, y_pos)
        self.__SetLabelSectionPosition(x_pos, y_pos)
        self.__SetProjectSectionPosition(x_pos, y_pos)
        self.__SetCompleteSectionPosition(x_pos, y_pos)
        self.__SetCancelSectionPosition(x_pos, y_pos)

    def __SetLoginSectionPosition(self, x_pos, y_pos) :
        # id position setting
        self.__id_label.grid(row=0, column=0, pady=self.__padding_y)
        self.__user_id_entry.grid(row=0, column=1, pady=self.__padding_y)
        self.__user_id_entry.insert(0, 'P000000')

        # password position setting
        self.__password_label.grid(row=0, column=2, pady=self.__padding_y)
        self.__user_password_entry.grid(row=0, column=3, pady=self.__padding_y)

        # login button position setting
        self.__login_button.grid(row=0, column=4, padx=self.__padding_x, pady=self.__padding_y)

    def __SetProjectSectionPosition(self, x_pos, y_pos) :
        # project name position setting
        self.__project_name_label.grid(row=0, column=0)
        self.__project_name_entry.grid(row=0, column=1)
        self.__project_name_entry.insert(0, 'AUTO_QA')

    def __SetLabelSectionPosition(self, x_pos, y_pos) :
        # label position setting
        self.__label_label.grid(row=1, column=0)
        self.__label_entry.grid(row=1, column=1)
        self.__label_entry.insert(0, 'TMAP_Mig_XX')

    def __SetCompleteSectionPosition(self, x_pos, y_pos) :
        self.__complete_button.grid(row=2, column=0)

    def __SetCancelSectionPosition(self, x_pos, y_pos) : 
        self.__cancel_button.grid(row=2, column=1)

    def Run(self) :
        self.__window.protocol('WM_DELETE_WINDOW', self.CancelProc) 
        # main loop
        self.__window.mainloop()

    def GetFilePath(self) : 
        filepath = filedialog.askopenfilename(initialdir='./data/')
        return filepath
    
    def LoginProc(self) :
        print(self.__user_id_entry.get())
        print(self.__user_password_entry.get())

        self.__core.SetID(self.__user_id_entry.get())
        self.__core.SetPassword(self.__user_password_entry.get())

        # 로그인 성공 시
        msgbox.showinfo('Login Complete.', '로그인에 성공했습니다.')
        ## 로그인 실패 시
        # msgbox.showerror('Login Failed.', '로그인에 실패했습니다.')

    def CompleteProc(self) :
        # 추가 : SelectProjectName
        self.__core.SetLabelName(self.__label_entry.get())
        # self.NewWindow()
        self.__window.destroy()

    def NewWindow(self) :
        global new
        self.__new = tk.Toplevel()
        self.__new.geometry('300x500+'+str(int(self.__ltPosX))+'+'+str(int(self.__ltPosY)))

        listbox = tk.Listbox(self.__new, height=0, selectmode='extented')
        
        for ele in self.__core.GetAllSenarioID() : 
            listbox.insert(0, ele)

        listbox.pack()
        self.__NewWindowInit()

    def __NewWindowInit(self) :
        pass

    def CancelProc(self) :
        self.__window.destroy()
        exit()