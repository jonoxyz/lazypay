from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime 
from selenium.webdriver.support.ui import Select

# lazypay built by Jonathan Edwards because 
# typing in your sign on and off times is just too hard.
# Visit lazypay.xyz


#requirements
#python 3.8 + https://www.python.org/downloads/
#Selenium https://pypi.org/project/selenium/
#Google Chrome https://www.google.com.au/chrome/
#Chrome Driver

#font ogre
#Insert LAZY PAY onto Pay Calculator




#### User Variables
username = ""
password = ""
#Chrome Webdriver Path
#enter the install path of your chrome web driver
path = ""
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
print("   __                     ___            ")
print("  / /  __ _ _____   _    / _ \__ _ _   _ ")
print(" / /  / _` |_  / | | |  / /_)/ _` | | | |")
print("/ /__| (_| |/ /| |_| | / ___/ (_| | |_| |")
print("\____/\__,_/___|\__, | \/    \__,_|\__, |")
print("                |___/              |___/ ")
print("The laziest way to check your pay\n ultra pre Alpha version 0.001\n\n\n")


########
first_fortnight = datetime.date(2017, 11, 12)
current_fortnight = first_fortnight
today = datetime.date.today()
pay_fortnights = []
#fortnight is the number of fortnights ago this pay period was.
#current fortnight is 0
#the previous fortnight would be 1
fortnight_number = 0

#to calculate most recent go through dates until you reach current date
while current_fortnight + datetime.timedelta(days=28) < today:
    current_fortnight = current_fortnight + datetime.timedelta(days=14)
    pay_fortnights.append(current_fortnight.strftime("%Y%m%d"))
    #print(current_fortnight.strftime("%Y%m%d"))

#print(current_fortnight)
#print("####\n")
print("most recent fortnight was " + str(current_fortnight))
print("If you want to check you pay for the most recent fortnight press Enter")
input_date = input("If you want to check a different fortnight enter the start date in the format YYYYMMDD\n")

#print(input_date == "")
if input_date == "":
    input_date = current_fortnight.strftime("%Y%m%d")
    date_selected = True

else:
    date_selected = False
    while not date_selected:
        if input_date in pay_fortnights:
            #print("Date " + input_date + " selected.")
            fortnight_number = len(pay_fortnights) - pay_fortnights.index(input_date) - 1
            break
        else:
            #print("Date given was not the first day in a pay period\nPlease try again in the format YYYYMMDD")
            input_date = input()

#######    


login_url = "https://go.metroapp.com.au/"
date_url = "https://go.metroapp.com.au/#/sign-on/"

###


driver = webdriver.Chrome(path)
#first we log in
driver.get(login_url)

driver.find_element("id", "login").send_keys(username)
driver.find_element("id", "pass").send_keys(password)
driver.find_element("id", "login-button").click()

#Then navigate to desired date

#driver.get(date_url)

## Data to store
# Sign On 
# Sign Off
# Wasted Meal
# OJT
# PH
# DDO? Have to ask upfront if this is ddo fortnight

###

#sign_on = driver.find_element()

shift_date = datetime.datetime(int(input_date[:4]), int(input_date[4:6]), int(input_date[6:]))
shift_list = []

for day in range(14):
    #lookup webpage for shift date
    shift_url = date_url + shift_date.strftime("%Y%m%d")
    driver.get(shift_url)
    time.sleep(1)
    all_data = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div").text
    #add one to the shift date
    shift_date = shift_date + datetime.timedelta(days=1)
    if "OFF" in all_data:
        shift_list.append({
        "type": "OFF",
        })
    elif "DDO" in all_data:
        shift_list.append({
        "type": "DDO",
        })
    elif "PH" in all_data:
        shift_list.append({
        "type": "PH",
        })
    elif "Sick" in all_data:
        shift_list.append({
        "type": "Sick",
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
            "type": "running",
            "sign_on": sign_on[:2] + sign_on[3:],
            "sign_off": sign_off[:2] + sign_off[3:],
            "ojt": ojt,
            "wasted_meal": wasted_meal
            })





#sign_on = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div/div[4]/div[2]").text
#sign_off = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div/div[9]/div[2]").text
#print("Sign on: ", sign_on)
#print("Sign off: ", sign_off)
ojt = False
wasted_meal = False

#print("*******")
all_data = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[3]/div[2]/div/div/div").text
#print(all_data)
if "OJT" in all_data:
    ojt = True

if "Wasted" in all_data:
    wasted_meal = True



######
####
###
##
# Enter data into Hyper chicken
hyper_url = "https://hyperchicken.com/paycalc/"
driver.get(hyper_url)

#set pay scale to SPOT
Select(driver.find_element("id", "pay-grade")).select_by_visible_text('SPOT')
driver.execute_script("updateGrade()")

#Make hyperchicken look pretty
driver.execute_script("arguments[0].style.backgroundColor = '#000';",driver.find_element(By.XPATH, "/html/body/ul"))
driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body"))
driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div"))
driver.execute_script("arguments[0].style.backgroundColor = '#000'; ",driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div"))

driver.execute_script("arguments[0].innerHTML = arguments[1]", driver.find_element(By.XPATH, "/html/body/ul/li[1]/sup"), "FULED BY LAZY PAY");

driver.execute_script("arguments[0].style.fontFamily = 'monospace'; ",driver.find_element(By.XPATH, "/html/body/span"))
driver.execute_script("arguments[0].style.textAlign = 'center'; ",driver.find_element(By.XPATH, "/html/body/span"))

driver.execute_script("arguments[0].innerHTML = arguments[1]", driver.find_element(By.XPATH, "/html/body/span"), "<pre>   __                     ___            <br />  / /  __ _ _____   _    / _ \__ _ _   _ <br /> / /  / _` |_  / | | |  / /_)/ _` | | | |<br /<br />/ /__| (_| |/ /| |_| | / ___/ (_| | |_| |<br />\____/\__,_/___|\__, | \/    \__,_|\__, |<br />                |___/              |___/  </pre>")




#Set correct fortnight
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[3]/span[1]").click()
for i in range(fortnight_number):
    time.sleep(1)

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
    x = xpath_lookup[day]
    driver.find_element(By.XPATH, x).click()

    if shift_list[day]["ojt"]:
        #select xpath of OJT button
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[1]").click()
    
    if shift_list[day]["wasted_meal"]:
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[3]").click()
    
    if shift_list[day]["type"] == "DDO":
        driver.find_element(By.XPATH, x[:40] + str(int(x[40:-3]) + 2) + "]/a[2]").click()

    driver.find_element(By.XPATH, x).click()



#This is where we enter data into hyperchicken for each shift
for day in range(len(shift_list)):
    time.sleep(0.05)

#    print(shift_list[day]["sign_on"])
    if shift_list[day]["type"] == "running":
        if day == 0:
            #Sun 1
            #enter sign on and sign off times
            driver.find_element("id", "sun1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sun1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 1:
            #Mon 1
            #enter sign on and sign off times
            driver.find_element("id", "mon1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "mon1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()
            #driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[5]/div[12]/a").click()

        if day == 2:
            #Tue 1
            #enter sign on and sign off times
            driver.find_element("id", "tue1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "tue1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
 
            addDetails()

        if day == 3:
            #Wed 1
            #enter sign on and sign off times
            driver.find_element("id", "wed1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "wed1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 4:
            #Thu 1
            #enter sign on and sign off times
            driver.find_element("id", "thu1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "thu1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 5:
            #Fri 1
            #enter sign on and sign off times
            driver.find_element("id", "fri1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "fri1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 6:
            #Sat 1
            #enter sign on and sign off times
            driver.find_element("id", "sat1-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sat1-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 7:
            #Sun 2
            #enter sign on and sign off times
            driver.find_element("id", "sun2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sun2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 8:
            #Monday 2
            #enter sign on and sign off times
            driver.find_element("id", "mon2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "mon2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 9:
            #Tue 2
            #enter sign on and sign off times
            driver.find_element("id", "tue2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "tue2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day == 10:
            #Wed 2
            #enter sign on and sign off times
            driver.find_element("id", "wed2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "wed2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day == 11:
            #Thu 2
            #enter sign on and sign off times
            driver.find_element("id", "thu2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "thu2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


        if day == 12:
            #Fri 2
            #enter sign on and sign off times
            driver.find_element("id", "fri2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "fri2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()

        if day == 13:
            #Sat 2
            #enter sign on and sign off times
            driver.find_element("id", "sat2-start").send_keys(shift_list[day]["sign_on"])
            driver.find_element("id", "sat2-end").send_keys(shift_list[day]["sign_off"])

            #edit shift details
            addDetails()


input("Press enter to exit.")