#from asyncio.windows_events import NULL
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime 
from selenium.webdriver.support.ui import Select
import sys



#import login details
from config import *
#for testing
#from configtest import *


version = "Beta 0.1"
# lazypay built by Jonathan Edwards because 
# typing in your sign on and off times is just too hard.
# Visit https://www.lazypay.xyz

# This would not have been possible without the amazing work
# of the Hyperchiecken Pay Calculator by Petar Stankovic
# https://hyperchicken.com/paycalc/

#requirements
#python 3.8 + https://www.python.org/downloads/
#Selenium https://pypi.org/project/selenium/
#Google Chrome https://www.google.com.au/chrome/
#Chrome Driver https://chromedriver.chromium.org/downloads

#font ogre


#### User Variables

#Crashes may occur if your connection is too slow. 
#Increase GO_SLEEP_TIME to pause for longer on each shift
#This will ensure the page fully loads and may reduce crashing
GO_SLEEP_TIME = loading_speed

#enter your metrogo login details
#these are not needed now due to credentials being stored
#in the config.py file.
#username = ""
#password = ""

#Chrome Webdriver Path
#enter the install path of your chrome web driver
#you should be able to leave emoty if webdriver is in the same folder as lazypay.py
path = ""

def printLogo():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("   __                     ___            ")
    print("  / /  __ _ _____   _    / _ \__ _ _   _ ")
    print(" / /  / _` |_  / | | |  / /_)/ _` | | | |")
    print("/ /__| (_| |/ /| |_| | / ___/ (_| | |_| |")
    print("\____/\__,_/___|\__, | \/    \__,_|\__, |")
    print("                |___/              |___/ ")
    print("The laziest way to check your pay\n" + version +"\n\n\n")

printLogo()

if username == "firstname.lastname":
    print("#### ERROR - Default Login Details")
    print("Please update your login details in the config.py file.\n\n\n")
    sys.exit()

########

first_fortnight = datetime.date(2017, 11, 12)
current_fortnight = first_fortnight
today = datetime.date.today()

#list of all pay fortnight start dates from first_fortnight to today
pay_fortnights = []

#fortnight_number is the number of fortnights ago this pay period was.
#current fortnight is 0
#the previous fortnight would be 1
#this is used for selecting the correct week in hyperchicken 
fortnight_number = 0

#Determines if you just calculate one pay or all pays since specified date
multiple_pays = None

#to calculate most recent go through dates until you reach current date
#add all of the start dates to the pay_fortnights list
while current_fortnight + datetime.timedelta(days=28) < today:
    current_fortnight = current_fortnight + datetime.timedelta(days=14)
    pay_fortnights.append(current_fortnight.strftime("%Y%m%d"))

print("The most recent fortnight was " + str(current_fortnight))
print("If you want to check you pay for the most recent fortnight press Enter")
input_date = input("If you want to check a different fortnight \nEnter the start date in the format YYYYMMDD\n")

#if they just press enter
if input_date == "":
    input_date = current_fortnight.strftime("%Y%m%d")
    date_selected = True
    #Set multiple pays to false as you can't have multiple pays from most recent pay
    multiple_pays = False

#if they enter a date ensure the date given is the pay_fortnights list
#if it is set input_date to the given input
else:
    date_selected = False
    while not date_selected:
        print(input_date)
        if input_date in pay_fortnights:
            #print("Date " + input_date + " selected.")
            fortnight_number = len(pay_fortnights) - pay_fortnights.index(input_date) - 1
            break
        else:
            print("\nDate given was not the first day in a pay period\nPlease try again in the format YYYYMMDD")
            input_date = input()

#Determine if you want multiple pays checked or just one
time.sleep(0.2)

print("###########################################")
print("Fortnight date " + input_date + " selected.")
print("###########################################")


if multiple_pays == None:
    time.sleep(1)

    print("\nDo you wish to calculate just one fortnights pay \nor all fortnights since the specified date?\n")
    time.sleep(1)
    while True:
        multiple_pays_input = input("To calculate a single fortnight pay press Enter. \nIf you wish to all pays since specified date type Y.\n")
        if multiple_pays_input == "":
            multiple_pays = False
            break
        elif multiple_pays_input in "yY":
            multiple_pays = True
            break
        else:
            print("\n Error Please Try Again")

#if multiple pays selected we need to scrape more days from metrogo

if multiple_pays:
    number_of_days = 14 * (fortnight_number + 1)
else:
    number_of_days = 14
#for debug purposes
#number_of_days = 3
print("\nChecking multiple pays: " + str(multiple_pays))


#             _               ___      
#  /\/\   ___| |_ _ __ ___   / _ \___  
# /    \ / _ \ __| '__/ _ \ / /_\/ _ \ 
#/ /\/\ \  __/ |_| | | (_) / /_\\ (_) |
#\/    \/\___|\__|_|  \___/\____/\___/ 
#

###
login_url = "https://go.metroapp.com.au/"
date_url = "https://go.metroapp.com.au/#/sign-on/"
###

#initiate chrome driver
driver = webdriver.Chrome(path)


#first we log in
driver.get(login_url)

driver.find_element("id", "login").send_keys(username)
driver.find_element("id", "pass").send_keys(password)
driver.find_element("id", "login-button").click()

#check login details were correct
time.sleep(GO_SLEEP_TIME)
if str(driver.current_url) == "https://go.metroapp.com.au/#/login":
    print("You have entered the wrong username and password.\nPlease update config.py with your correct login details.")
    sys.exit()

input("Press enter to quit.")

#Then navigate to desired date
shift_date = datetime.datetime(int(input_date[:4]), int(input_date[4:6]), int(input_date[6:]))
shift_list = []

for day in range(number_of_days):
    #lookup webpage for shift date
    shift_url = date_url + shift_date.strftime("%Y%m%d")
    driver.get(shift_url)
    time.sleep(GO_SLEEP_TIME)
    print("Fetching day " + str(day))

    #extract all shift data
    all_data = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div").text
    
    #add one day to the shift date to be ready for the next lookup
    shift_date = shift_date + datetime.timedelta(days=1)

    #Check if shift is a Non Worked Shift
    if "OFF" in all_data:
        shift_list.append({
        "paid": False,
        "type": "OFF",
        })
    elif "DDO" in all_data:
        shift_list.append({
        "paid": True,
        "type": "DDO",
        "sign_on": "",
        "sign_off": "",
        "ojt": False,
        "wasted_meal": False
        })
    
    elif "PH" in all_data:
        shift_list.append({
        "paid": True,
        "type": "PH",
        "sign_on": "",
        "sign_off": "",
        "ojt": False,
        "wasted_meal": False
        })
    elif "Sick" in all_data:
        shift_list.append({
        "paid": True,
        "type": "Sick",
        "sign_on": "",
        "sign_off": "",
        "ojt": False,
        "wasted_meal": False
        })
    elif "AL" in all_data:
        shift_list.append({
        "paid": True,
        "type": "AL",
        "sign_on": "",
        "sign_off": "",
        "ojt": False,
        "wasted_meal": False
        })
    

    else:

        ojt = True
        ojt = False
        wasted_meal = False

        #set ShiftNumber
        shift = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div/div[7]/div[2]/a/u").text

        #set SignOn
        sign_on = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div/div[4]/div[2]").text
        #set SignOff
        sign_off = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div/div[9]/div[2]").text

        #set OJT
        if "OJT" in all_data:
            ojt = True
        #set wastedmeal
        if "Wasted" in all_data:
            wasted_meal = True
        

        #add to shift list
        shift_list.append({
            "paid": True,
            "type": "running",
            "sign_on": sign_on[:2] + sign_on[3:],
            "sign_off": sign_off[:2] + sign_off[3:],
            "ojt": ojt,
            "wasted_meal": wasted_meal
            })

########
ojt = False
wasted_meal = False

all_data = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div").text
#print(all_data)
if "OJT" in all_data:
    ojt = True

if "Wasted" in all_data:
    wasted_meal = True
print("\n\nprinting shift list")
print(shift_list)

#                               ___ _     _      _              
#  /\  /\_   _ _ __   ___ _ __ / __\ |__ (_) ___| | _____ _ __  
# / /_/ / | | | '_ \ / _ \ '__/ /  | '_ \| |/ __| |/ / _ \ '_ \ 
#/ __  /| |_| | |_) |  __/ | / /___| | | | | (__|   <  __/ | | |
#\/ /_/  \__, | .__/ \___|_| \____/|_| |_|_|\___|_|\_\___|_| |_|
#        |___/|_|                                               
#
# Enter data into Hyper chicken
hyper_url = "https://hyperchicken.com/paycalc/"
driver.get(hyper_url)

#set pay scale to SPOT
Select(driver.find_element("id", "pay-grade")).select_by_visible_text('SPOT')
driver.execute_script("updateGrade()")


#Make hyperchicken look pretty
def prettyChicken():
    driver.execute_script("arguments[0].style.backgroundColor = '#000';",driver.find_element(By.XPATH, "/html/body/ul"))
    driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body"))
    driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div"))
    driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div"))

    driver.execute_script("arguments[0].innerHTML = arguments[1]", driver.find_element(By.XPATH, "/html/body/ul/li[1]/sup"), "FULED BY LAZY PAY");

    driver.execute_script("arguments[0].style.fontFamily = 'monospace'; ",driver.find_element(By.XPATH, "/html/body/span"))
    driver.execute_script("arguments[0].style.textAlign = 'center'; ",driver.find_element(By.XPATH, "/html/body/span"))

    driver.execute_script("arguments[0].innerHTML = arguments[1]", driver.find_element(By.XPATH, "/html/body/span"), "<pre>   __                     ___            <br />  / /  __ _ _____   _    / _ \__ _ _   _ <br /> / /  / _` |_  / | | |  / /_)/ _` | | | |<br /<br />/ /__| (_| |/ /| |_| | / ___/ (_| | |_| |<br />\____/\__,_/___|\__, | \/    \__,_|\__, |<br />                  |___/              |___/  <br /><br /><br /><a href='https://lazypay.xyz/'>lazypay.xyz</a><br />The laziest way to check your pay.</pre>")
    driver.execute_script("arguments[0].style.color = 'white'; ",driver.find_element(By.XPATH, "/html/body/span/pre/a"))

prettyChicken()


#Set correct fortnight
time.sleep(0.2)
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[3]/span[1]").click()
for i in range(fortnight_number):
    time.sleep(0.05)

    #click back
    driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[3]/span[1]").click()

#HyperChicken Variables
xpath_lookup = [
    "/html/body/div[2]/div[1]/div/div[5]/div[8]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[12]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[16]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[20]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[24]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[28]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[32]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[37]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[41]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[45]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[49]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[53]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[57]/a",
    "/html/body/div[2]/div[1]/div/div[5]/div[61]/a",
]
#function to add shift details 
def addDetails():
    time.sleep(0.05)
    x = xpath_lookup[day % 14]
    driver.find_element(By.XPATH, x).click()

    if shift_list[day]["ojt"]:
        #select xpath of OJT button
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[1]").click()
    
    if shift_list[day]["wasted_meal"]:
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[3]").click()
    
    if shift_list[day]["type"] == "DDO":
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[2]").click()
    
    if shift_list[day]["type"] == "AL":
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[5]").click()

    driver.find_element(By.XPATH, x).click()
    driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div"))
    driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div"))

#counts the number of shifts entered so far in each fortnight
#once you get to the end of the fortnight a new fortnight will be selected in hyper chicken
shift_count = 0
#This is where we enter data into hyperchicken for each shift
for day in range(len(shift_list)):
    print("Entering Shift: " + str(shift_list[day]) )
    time.sleep(0.05)
    if shift_count == 14:
        shift_count = 0
        driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[3]/span[3]").click()
        prettyChicken()
        



#    print(shift_list[day]["sign_on"])
    if shift_list[day]["paid"]:
        if day % 14 == 0:
            #Sun 1
            #enter sign on and sign off times
            driver.find_element("id", "sun1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sun1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 1:
            #Mon 1
            #enter sign on and sign off times
            driver.find_element("id", "mon1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "mon1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()
            #driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[5]/div[12]/a").click()

        if day % 14 == 2:
            #Tue 1
            #enter sign on and sign off times
            driver.find_element("id", "tue1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "tue1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
 
            addDetails()

        if day % 14 == 3:
            #Wed 1
            #enter sign on and sign off times
            driver.find_element("id", "wed1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "wed1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 4:
            #Thu 1
            #enter sign on and sign off times
            driver.find_element("id", "thu1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "thu1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 5:
            #Fri 1
            #enter sign on and sign off times
            driver.find_element("id", "fri1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "fri1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 6:
            #Sat 1
            #enter sign on and sign off times
            driver.find_element("id", "sat1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sat1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 7:
            #Sun 2
            #enter sign on and sign off times
            driver.find_element("id", "sun2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sun2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 8:
            #Monday 2
            #enter sign on and sign off times
            driver.find_element("id", "mon2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "mon2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 9:
            #Tue 2
            #enter sign on and sign off times
            driver.find_element("id", "tue2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "tue2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day % 14 == 10:
            #Wed 2
            #enter sign on and sign off times
            driver.find_element("id", "wed2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "wed2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day % 14 == 11:
            #Thu 2
            #enter sign on and sign off times
            driver.find_element("id", "thu2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "thu2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day % 14 == 12:
            #Fri 2
            #enter sign on and sign off times
            driver.find_element("id", "fri2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "fri2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day % 14 == 13:
            #Sat 2
            #enter sign on and sign off times
            driver.find_element("id", "sat2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sat2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()
    shift_count += 1
    #exit if only calculating one fortnight
    if shift_count == 14 and multiple_pays == False:
        break
        
driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, "/html/body/span/pre"))

#Debug

printLogo()
print("\n\n\nYour pay has been entered the lazy way.\n")
input("Press enter to quit.")

driver.close()
