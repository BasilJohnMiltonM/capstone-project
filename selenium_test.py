from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

options = webdriver.EdgeOptions()
driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=options)

driver.get("https://www.google.com")
print(driver.title)
driver.quit()