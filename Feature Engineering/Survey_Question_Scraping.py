# import libraries
from pathlib import Path

import pandas as pd
from selenium import webdriver

# specify url
urlpage = 'http://psy.dotin.us/psy_test/view'
# print(urlpage)

# run chrome webdriver from executable path
driver = webdriver.Chrome(executable_path = 'C:/Users/Ergo/Desktop/chromedriver/chromedriver.exe')

# get web page
driver.get(urlpage)

# change the style display from none to block for each chunk of the survey (chunk=page of the survey)
# this will bring all questions into 1 page instead of 18 pages

# for quiz 0
for i in range(1, 5):
    chunk = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[%i]" % (i))
    chunk = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", chunk)

# for quiz-1
for i in range(1, 2):
    chunk = driver.find_element_by_xpath("/html/body/div/form/div[5]/div[%i]" % (i))
    chunk = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", chunk)

# for quiz-2
for i in range(1, 8):
    chunk = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[%i]" % (i))
    chunk = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", chunk)

# for quiz-3
for i in range(1, 6):
    chunk = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[%i]" % (i))
    chunk = driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", chunk)

    # quiz 0 questions
print("==QUIZ 0==")
print("==bf_questions==")

# chunk 1 questions
p1_bf_list = []
for i in range(3, 11):
    p1_question = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[1]/div[%i]/div[1]" % (i))
    p1_question_id = p1_question.text
    p1_bf_list.append(p1_question_id)

p2_bf_list = []
# chunk 2 questions
for i in range(1, 11):
    p2_question = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[2]/div[%i]/div[1]" % (i))
    p2_question_id = p2_question.text
    p2_bf_list.append(p2_question_id)

# chunk 3 questions
p3_bf_list = []
for i in range(1, 11):
    p3_question = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[3]/div[%i]/div[1]" % (i))
    p3_question_id = p3_question.text
    p3_bf_list.append(p3_question_id)

# chunk 4 questions
p4_bf_list = []
for i in range(1, 11):
    p4_question = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[4]/div[%i]/div[1]" % (i))
    p4_question_id = p4_question.text
    p4_bf_list.append(p4_question_id)

# chunk 5 questions
p5_bf_list = []
for i in range(1, 5):
    p5_question = driver.find_element_by_xpath("/html/body/div/form/div[4]/div[5]/div[%i]/div[1]" % (i))
    p5_question_id = p5_question.text
    p5_bf_list.append(p5_question_id)

#######################################
# quiz 1 questions
print("==QUIZ 1==")
print("==bs_questions==")

p1_bs_list = []
# chunk 6 questions
for i in range(3, 7):
    p1_bs_question = driver.find_element_by_xpath("/html/body/div/form/div[5]/div/div[%i]/div[1]" % (i))
    p1_bs_question_id = p1_bs_question.text
    p1_bs_list.append(p1_bs_question_id)

#######################################
# quiz 2 questions
print("==QUIZ 2==")
print("==miq_questions==")

p1_miq_list = []
# chunk 7 questions
for i in range(3, 11):
    p1_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[1]/div[%i]/div[1]" % (i))
    p1_miq_question_id = p1_miq_question.text
    p1_miq_list.append(p1_miq_question_id)

p2_miq_list = []
# chunk 8 questions
for i in range(1, 11):
    p2_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[2]/div[%i]/div[1]" % (i))
    p2_miq_question_id = p2_miq_question.text
    p2_miq_list.append(p2_miq_question_id)

# chunk 9 questions
p3_miq_list = []
for i in range(1, 11):
    p3_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[3]/div[%i]/div[1]" % (i))
    p3_miq_question_id = p3_miq_question.text
    p3_miq_list.append(p3_miq_question_id)

# chunk 10 questions
p4_miq_list = []
for i in range(1, 11):
    p4_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[4]/div[%i]/div[1]" % (i))
    p4_miq_question_id = p4_miq_question.text
    p4_miq_list.append(p4_miq_question_id)

# chunk 11 questions
p5_miq_list = []
for i in range(1, 11):
    p5_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[5]/div[%i]/div[1]" % (i))
    p5_miq_question_id = p5_miq_question.text
    p5_miq_list.append(p5_miq_question_id)

p6_miq_list = []
# chunk 12 questions
for i in range(1, 11):
    p6_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[6]/div[%i]/div[1]" % (i))
    p6_miq_question_id = p6_miq_question.text
    p6_miq_list.append(p6_miq_question_id)

p7_miq_list = []
# chunk 13 questions
for i in range(1, 9):
    p7_miq_question = driver.find_element_by_xpath("/html/body/div/form/div[6]/div[7]/div[%i]/div[1]" % (i))
    p7_miq_question_id = p7_miq_question.text
    p7_miq_list.append(p7_miq_question_id)

#######################################
# quiz 3 questions
print("==QUIZ 3==")
print("==pgi_liking_competence_questions==")

p1_pgi_list = []
# chunk 14 questions
for i in range(3, 11):
    p1_pgi_question = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[1]/div[%i]/div[1]" % (i))
    p1_pgi_question_id = p1_pgi_question.text
    p1_pgi_list.append(p1_pgi_question_id)

p2_pgi_list = []
# chunk 15 questions
for i in range(1, 11):
    p2_pgi_question = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[2]/div[%i]/div[1]" % (i))
    p2_pgi_question_id = p2_pgi_question.text
    p2_pgi_list.append(p2_pgi_question_id)

p3_pgi_list = []
# chunk 16 questions
for i in range(1, 11):
    p3_pgi_question = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[3]/div[%i]/div[1]" % (i))
    p3_pgi_question_id = p3_pgi_question.text
    p3_pgi_list.append(p3_pgi_question_id)

p4_pgi_list = []
# chunk 17 questions
for i in range(1, 11):
    p4_pgi_question = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[4]/div[%i]/div[1]" % (i))
    p4_pgi_question_id = p4_pgi_question.text
    p4_pgi_list.append(p4_pgi_question_id)

p5_pgi_list = []
# chunk 18 questions
for i in range(1, 5):
    p5_pgi_question = driver.find_element_by_xpath("/html/body/div/form/div[7]/div[5]/div[%i]/div[1]" % (i))
    p5_pgi_question_id = p5_pgi_question.text
    p5_pgi_list.append(p5_pgi_question_id)

# create dictionary holding all these values
dict_questions = {"bf_questions": [p1_bf_list, p2_bf_list, p3_bf_list, p4_bf_list, p5_bf_list],
                  "bs_questions": p1_bs_list,
                  "miq_questions": [p1_miq_list, p2_miq_list, p3_miq_list, p4_miq_list, p5_miq_list,
                                    p6_miq_list, p7_miq_list],
                  "pgi_liking_competence_questions": [p1_pgi_list, p2_pgi_list, p3_pgi_list, p4_pgi_list,
                                                      p5_pgi_list]}

# turn dict to dataframe
survey_questions = pd.DataFrame(list(dict_questions.items()))
survey_questions.columns = ['question_type', 'questions']

# set path directory
path = Path("C:/Users/Ergo/Desktop/Github_Capstone/Dotin-Columbia-Castone-Team-Alpha-/Data")

survey_questions.to_csv(path / "scraped_survey_questions.csv")
