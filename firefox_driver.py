from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions, FirefoxProfile, Firefox

options = FirefoxOptions()
options.headless = True
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
profile = r'C:\Users\OleksandrLukianets\AppData\Roaming\Mozilla\Firefox\Profiles\fx2jzzki.default-release'
# options.add_argument("--headless")
# options.add_argument("-profile")
# options.add_argument(r"C:\Users\OleksandrLukianets\AppData\Local\Mozilla\Firefox\Profiles\fx2jzzki.default-release")
# firefox_capabilities = DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True


driver = Firefox(
    firefox_profile=profile,
    executable_path=r"C:\Users\OleksandrLukianets\PycharmProjects\mitm_proxy\geckodriver.exe",
    options=options,
)
