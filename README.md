# Lazy Pay
[LazyPay.xyz](https://lazypay.xyz/)

Lazy Pay was developed by Jonathan Edwards to automate the process of collecting shift details from MetroGo and calculating your pay with the [HyperChicken](https://hyperchicken.com/paycalc/) pay calculator (Developed by Petar Stankovic).
## Download Lazy Pay

There are two files required to run Lazy Pay. 
Download these files from GitHub into a folder on your computer.
[lazypay.py](https://github.com/jonoxyz/lazypay/blob/main/lazypay.py) and [config.py](https://github.com/jonoxyz/lazypay/blob/main/config.py)

Once these files are downloaded use a text editor to update config.py and add your login details.

## Prerequisites

Before running lazypay.py, make sure you have the following prerequisites installed on your system:

1. **Python**: Make sure you have Python installed. You can download and install Python from [python.org](https://www.python.org/downloads/).

   - On macOS, you might need to use `python3` instead of `python`. To check your Python version, open a terminal and run:
     ```bash
     python3 --version
     ```

     If you see a version number, you can use `python3` instead of `python` in the commands below.

   - On Windows, you can use either `python` or `py` as the command. To check your Python version, open a command prompt and run:
     ```bash
     py --version
     ```
     If you see a version number, you can use `py` instead of `python` in the commands below.

2. **Selenium for Python**: Install the Selenium library for Python. If you have Python 3.x, use the following command:
Note If you don't have `pip` installed, you can you will need first to get `pip` with the following commands:

   - On macOS:
     ```bash
     python3 -m ensurepip --upgrade
     ```

   - On Windows:
     ```bash
     py -m ensurepip --upgrade
     ```

Once  `pip` is installed you can get Selenium with the following commands:

   - On macOS:
     ```bash
     pip3 install selenium
     ```

   - On Windows:
     ```bash
     py -m pip install selenium
     ```


3. **Google Chrome**: Download and install the latest version of Google Chrome from [chrome.google.com](https://www.google.com/chrome/).

4. **ChromeDriver**: Download the appropriate version of ChromeDriver for your operating system from [chromedriver.chromium.org](https://sites.google.com/chromium.org/driver/downloads). Ensure that the ChromeDriver version matches your installed Chrome version.

   - To find your version of Google Chrome, open Chrome and click on the three vertical dots in the top-right corner.
   - From the dropdown menu, hover over "Help," and then click on "About Google Chrome."
   - A new tab will open, displaying the version number of Chrome.
## Setting Up ChromeDriver

1. After downloading ChromeDriver, extract the archive to obtain the `chromedriver.exe` (Windows), `chromedriver` (macOS) executable.

2. Save the `chromedriver.exe` or `chromedriver` executable in the same directory as the Python scripts you downloaded and saved from GitHub.

## Running the Script

Now that you have the prerequisites in place, follow these steps to run Lazy Pay:

1. Open a terminal (macOS) or command prompt (Windows).

2. Navigate to the directory containing the Python scripts and the `chromedriver.exe` or `chromedriver` executable.

3. Run the lazypay.py script using one of the following commands:

   - On macOS:
     ```bash
     python3 lazypay.py
     ```

   - On Windows:
     ```bash
     py lazypay.py
     ```

## Troubleshooting

- Just try running the script again. Sometimes lazypay.py crashes on the first run.
- If you experience crashing it may be due to a slow network speed. It may help to increase the value of `loading_speed `in config.py.
- If you encounter any issues, ensure that ChromeDriver is the correct version for your Chrome installation.
- Make sure the `chromedriver.exe` or `chromedriver` executable is in the same directory as your Python script.