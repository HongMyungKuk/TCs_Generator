import jira_process as JIRA
import parser_test as PARSER
import time

global width
global height

class Core :
    def __init__(self) :
        width = 1920
        height = 1080
        self.__id = ''
        self.__password = ''
        self.__label = ''
        self.__jira = JIRA.Jira(width, height)
        self.__parser = PARSER.Parser()

    def Init(self, filepath, filename) :
        self.__filename = filename
        self.InitParser(filepath)
        # 여러개 시트의 데이터를 불러오도록 확장
        self.InitData('2.VUX 시나리오_TMAP전화')
        
    def InitParser(self, filepath) :
        self.__filepath = filepath
        self.__parser.Init(filepath)
        self.__sheet_names = self.__parser.GetSheetNames()

    def InitData(self, sheetname) :
        # skipvalue 일반화
        self.__parser.LoadSheetData(self.__filepath, sheetname, 0) 
        self.__parser.ProcessingData()
        #print(self.__parser.GetData())        
        self.__sheet_names = self.__sheet_names[3:9]
        self.__data = self.__parser.GetData()
        self.__scenario_id_data = self.__parser.GetAllSenarioID()

        self.InitDataSize()

    def InitDataSize(self) :
        data_size = self.__parser.GetSize()
        self.__row_size = data_size[0]
        self.__col_size = data_size[1]

    def SetID(self, id) :
        self.__id = id

    def SetPassword(self, password) : 
        self.__password = password

    def SetLabelName(self, label) : 
        self.__label = label

    def GetAllSenarioID(self) : 
        return self.__scenario_id_data

    def Run(self, set_row=0) :
        # Jira 실행
        self.__jira.Start('https://jira.tde.sktelecom.com/secure/Dashboard.jspa', 10)
        # ID, Password GUI 에서 전달함
        self.__jira.Login(self.__id, self.__password)
        time.sleep(1)

        #for ele in self.__sheet_names : 

        col_names = self.__parser.GetColmnName()
        # print(col_names)
        # exit()

        prev_test_cases_dic = {}
        for row in range(set_row, self.__row_size) :
            test_cases = []
            test_cases_dic = {}
            col_index_dic = {}
            for col in range(0, self.__col_size) : 
                test_cases.append(str(self.__data.iloc[row, col]))
                # col 이름에 개행문자 (\n) 가 들어가 있으면 제거한다.
                temp = str(col_names[col])
                col_names[col] = temp.replace('\n', '')
                # test_cases 를 dictionary 자료구조로 관리
                test_cases_dic[col_names[col]] = test_cases[col]
                col_index_dic[col_names[col]] = col

            ## Debugging
            # print(col_index_dic)
            # exit()
                
            # print(test_cases_dic['기능 이름'])

            # 프로젝트 유형, 이슈 타입은 추후 GUI 에서 전달함
            # 개행 문자가 존재하면 프로그램이 종료됨.
            # 개행 문자 제거를 위한 부분
            if test_cases_dic['기능 이름'] == 'nan' :
                test_cases_dic['기능 이름'] = prev_test_cases_dic['기능 이름']
            if '\n' in test_cases_dic['기능 이름'] :
                test_cases_dic['기능 이름'] = str(test_cases_dic['기능 이름']).replace('\n', '')
            
            # print(test_cases_dic['기능 이름'])
            # exit()

            if test_cases_dic['기능 상세설명'] == 'nan' :
                test_cases_dic['기능 상세설명'] = prev_test_cases_dic['기능 상세설명']
            if '\n' in test_cases_dic['기능 상세설명'] :
                test_cases_dic['기능 상세설명'] = str(test_cases_dic['기능 상세설명']).replace('\n', '')

            # index = col_index_dic['기능 이름']
            # summary = str(self.__data.iloc[row,0]) + ' ' + str(self.__data.iloc[row, index])
            summary = str(self.__data.iloc[row,0]) + ' ' + str(test_cases_dic['기능 이름'] + '_' + str(test_cases_dic['기능 상세설명']))
            self.CreateTestCase('AUTO_QA', 'Test Case', summary, test_cases, col_names, col_index_dic, test_cases_dic, 
                                prev_test_cases_dic)
            # nan 값을 처리하기 위해 이전 딕셔너리 값을 생성한다.
            prev_test_cases_dic = test_cases_dic

        self.__jira.End()

    def CreateTestCase(self, project_name, issue_type, summary, test_cases, col_names, col_index_dic, test_cases_dic, 
                       prev_test_cases_dic) :
        self.__jira.ClickMakeTestCase()
        time.sleep(1)
        self.__jira.SelectProject(project_name)
        time.sleep(1)
        self.__jira.SelectIssueType(issue_type)
        time.sleep(1)
        self.__jira.WriteSummary(summary)
        time.sleep(1)
        self.__jira.SelectManager()
        time.sleep(1)
        # self.__jira.WriteExplanation('test')
        # time.sleep(1)
        self.__jira.WriteTestCase(col_names, col_index_dic, test_cases_dic, prev_test_cases_dic, self.__filename)
        time.sleep(1)
        self.__jira.SelectAddButton()
        time.sleep(1)
        self.__jira.SelectLabel(self.__label)
        time.sleep(1)
        self.__jira.MakeTestCaseButtonClick()
        time.sleep(5)

            

