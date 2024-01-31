import core
import gui as GUI
import function

if __name__ == '__main__' : 
    core_ = core.Core()

    gui = GUI.GUI(core_, 300, 160)

    gui.Run()

    filepath = gui.GetFilePath()

    filename = function.GetFilename(filepath)

    core_.Init(filepath, filename)

    print('작업을 시작하고자 하는 행을 선택해주세요.')
    set_row = input()

    core_.Run(int(set_row))

else : 
    print('This .py file is not main.py')
    print(-1)
    exit()
