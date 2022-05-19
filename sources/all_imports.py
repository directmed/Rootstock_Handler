# include for GUI
from tkinter import *
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from functools import partial

# include for navigating chrome browser
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException, StaleElementReferenceException, NoSuchWindowException
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException, UnexpectedAlertPresentException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import re

# include for automatic chrome browser updates
import chromedriver_autoinstaller

# install for reading csv files
import pandas as pd
import numpy as np

# install for creating Word documents
from datetime import date
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
import sys
import os
import subprocess
import logging
import traceback

if __name__ == "__main__":
    print("Hello world!")
