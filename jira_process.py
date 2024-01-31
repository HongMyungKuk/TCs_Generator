from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyautogui as pt

class Jira :
    def __init__(self, width, height) -> None :
        self.__width = width
        self.__height = height
        self.__options = webdriver.ChromeOptions()
        # 브라우저 윈도우 사이즈 설정
        self.__options.add_argument('window-size='+ str(self.__width)+','+str(self.__height))
        self.__driver = webdriver.Chrome(options=self.__options)

    def Start(self, url, time) -> None :
        self.__driver.get(url)
        self.__driver.implicitly_wait(time)

    def Login(self, id, password) ->  None :
        search_box = self.__driver.find_element(By.XPATH, '//*[@id="input-username"]')
        search_box.send_keys(id)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        # ID 입력 후 Enter 입력까지 대기 (Needs modification)
        pt.write(password)
        # 로그인 실패했을 경우 예외처리 추가 필요!

        
    def CreateNewTab(self, url) -> None :
        self.__driver.execute_script('window.open('');')
        self.__driver.switch_to.window(self.__driver.window_handles[-1])
        self.__driver.get(url)

    def ClickMakeTestCase(self) -> None :
        make_tc = self.__driver.find_element(By.XPATH, '//*[@id="create_link"]')
        make_tc.click()

    def ClickProject(self) -> None :
        click_project = self.__driver.find_element(By.XPATH, '//*[@id="project-single-select"]/span')
        click_project.click()

    def SelectProject(self, name) -> None : 
        select_project = self.__driver.find_element(By.XPATH, '//*[@id="project-field"]')
        select_project.click()
        select_project.send_keys(name)
        select_project.send_keys(Keys.ENTER)

    def SelectIssueType(self, name) -> None :
        select_issue_type = self.__driver.find_element(By.XPATH, '//*[@id="issuetype-field"]')
        select_issue_type.click()
        select_issue_type.send_keys(name)
        select_issue_type.send_keys(Keys.ENTER)

    def __WriteTestStep(self, desc) -> None :
        write_text = self.__driver.find_element(By.XPATH, '//*[@id="teststep-table"]/tbody[2]/tr/td[3]/textarea')
        write_text.send_keys(desc)

    def __WriteDataTest(self, desc) -> None :
        write_text = self.__driver.find_element(By.XPATH, '//*[@id="teststep-table"]/tbody[2]/tr/td[4]/textarea')
        write_text.send_keys(desc)

    def __WriteExpectedResult(self, desc) -> None :
        write_text = self.__driver.find_element(By.XPATH, '//*[@id="teststep-table"]/tbody[2]/tr/td[5]/textarea')
        write_text.send_keys(desc)

    # 아래의 3개 함수의 경우 하드 코딩이 아닌 동적으로 확장 필요!!
    def __SetTestStepData(self, col_names, col_index_dic, desc, prev_descs, index) :
        data = ''
        # [시나리오 ID]
        # AutoAppControl_Media_Stop_01
        #
        # [Ver]
        # 0.3.8
        #
        # [기능 이름]
        # 종료 예약
        #
        # [기능 상세설명]
        # 미디어 종료 예약 불가 (미지원기능)
        # 
        # [intent (domain)]
        # set.end_time (general)
        #
        
        # 데이터가 nan 일 경우
        # 이전 데이터 값을 넣어준다.
        for i in range(0, index) :
            if len(prev_descs) == 0 :
                break
            if desc[col_names[i]] == 'nan' :
                desc[col_names[i]] = prev_descs[col_names[i]] 

        for i in range(0, index) : 
            data += '*[' + col_names[i] + ']*' + '\n' + desc[col_names[i]] + '\n\n' 

        # data = '*[' + col_names[0] + ']*' + '\n' \
        #      + desc[col_names[0]] + '\n\n' \
        #      + '*[' + col_names[1] + ']*' + '\n' \
        #      + desc[col_names[1]] + '\n\n' \
        #      + '*[' + col_names[2] + ']*' + '\n' \
        #      + desc[col_names[2]] + '\n\n' \
        #      + '*[' + col_names[3] + ']*' + '\n' \
        #      + desc[col_names[3]] + '\n\n' \
        #      + '*[' + col_names[4] + ']*' + '\n' \
        #      + desc[col_names[4]] + '\n\n' \

        return data
    
    def __SetDataTestData(self, col_names, col_index_dic, desc, prev_descs, index) :
        data = ''
        # 데이터가 nan 일 경우
        # 이전 데이터 값을 넣어준다.
        for i in range(index, index + 1) :
            if len(prev_descs) == 0 :
                break
            if desc[col_names[i]] == 'nan' :
                desc[col_names[i]] = prev_descs[col_names[i]] 

        # [대표발화]
        # [general]
        # W, 10시 30분에 종료해줘
        data = '*[' + col_names[index] + ']*' + '\n' \
             + desc[col_names[index]] + '\n\n' \

        return data
    
    def __SetExpectedResultData(self, col_names, col_index_dic, desc, prev_descs, index) :
        data = ''
        # 데이터가 nan 일 경우
        # 이전 데이터 값을 넣어준다.
        for i in range(index, index + 1) :
            if len(prev_descs) == 0 :
                break
            if desc[col_names[i]] == 'nan' :
                desc[col_names[i]] = prev_descs[col_names[i]]

        # [TTS 답변]
        # 지원하지 않는 기능이에요.
        data = '*[' + col_names[index] + ']*' + '\n' \
             + desc[col_names[index]] + '\n\n' \

        return data
    
    def __CalcIndex(self, col_index_dic, col_name) :
        return col_index_dic[col_name]
    
    def __CalcIndex2_Test(self, col_names, col_name) : 
        i = 0
        for ele in col_names : 
            if col_name in ele :
                return i
            i += 1

    def WriteTestCase(self, col_names, col_index_dic, descs, prev_descs, filename) -> None :
        # 1. col 명 전달 필요!!
        # 2. 데이터 값에 nan 이 있을경우 이전 데이터 참조

        # [대표발화] column 이 나오기 전 index 찾기!!
        index = self.__CalcIndex(col_index_dic, '대표 발화')
        test_step_data = self.__SetTestStepData(col_names, col_index_dic, descs, prev_descs, index)
        data_test_data = self.__SetDataTestData(col_names, col_index_dic, descs, prev_descs, index)
        index = self.__CalcIndex(col_index_dic, 'TTS 답변')
        set_expected_result_data = self.__SetExpectedResultData(col_names, col_index_dic, descs, prev_descs, index)
        index = self.__CalcIndex2_Test(col_names, '동작')
        set_expected_result_data += '\n'
        set_expected_result_data += self.__SetExpectedResultData(col_names, col_index_dic, descs, prev_descs, index)
        set_expected_result_data += '\n\n'
        set_expected_result_data += '- ' + filename

        self.__WriteTestStep(test_step_data)
        self.__WriteDataTest(data_test_data)
        self.__WriteExpectedResult(set_expected_result_data)

    def WriteSummary(self, summary) -> None : 
        write_summary = self.__driver.find_element(By.XPATH, '//*[@id="summary"]')
        write_summary.send_keys(summary)

    def SelectManager(self, name) -> None :
        select_manager = self.__driver.find_element(By.XPATH, '//*[@id="assignee-field"]')
        select_manager.click()
        select_manager.send_keys(name)
        #select_manager.send_keys(Keys.ENTER)

    def SelectManager(self) -> None :
        select_manager = self.__driver.find_element(By.XPATH, '//*[@id="assign-to-me-trigger"]')
        select_manager.click()

    def MakeTestCaseButtonClick(self) -> None :
        select_make_button = self.__driver.find_element(By.XPATH, '//*[@id="create-issue-submit"]')
        select_make_button.click()

    def SelectAddButton(self) -> None : 
        select_add_button = self.__driver.find_element(By.XPATH, '//*[@id="teststep-table"]/tbody[2]/tr/td[6]/input')
        select_add_button.click()

    def SelectLabel(self, label) -> None :
        select_label = self.__driver.find_element(By.XPATH, '//*[@id="labels-textarea"]')
        select_label.click()
        select_label.send_keys(label)
        select_label.send_keys(Keys.ENTER)

    # def WriteExplanation(self, explanation) -> None :
    #     write_explanation = self.__driver.find_element(By.XPATH, '//*[@id="description-wiki-edit"]/div[1]/div/div[1]/div[2]/div[1]')
    #     write_explanation.send_keys(explanation)

    def End(self) -> None:
        self.__driver.quit()
