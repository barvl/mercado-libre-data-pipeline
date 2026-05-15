from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Edge(options=options)
driver.get("https://listado.mercadolibre.com.mx/celulares-smartphones")
time.sleep(6)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, "lxml")
productos = soup.find_all("li", class_="ui-search-layout__item")

# Ver HTML completo del primer producto
print(productos[0].prettify())

driver.quit()