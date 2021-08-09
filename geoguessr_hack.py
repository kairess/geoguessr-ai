from selenium import webdriver
import time, json
from tqdm import tqdm

URL = 'https://www.geoguessr.com/maps/world/play'

NUMBER_OF_GAMES = 10000
EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS'
PASSWORD = 'YOUR_PASSWORD'

driver = webdriver.Chrome('/Users/brad/Development/bdf_code/ai-geoguessr/chromedriver')
driver.set_window_position(0, 0)
driver.set_window_size(1920, 1080)

# login
driver.get('https://www.geoguessr.com/signin')
input_text = driver.find_element_by_css_selector("input[name=email]")
input_text.send_keys(EMAIL_ADDRESS)
input_text = driver.find_element_by_css_selector("input[name=password]")
input_text.send_keys(PASSWORD)
input_text.submit() 
time.sleep(1)

for _ in tqdm(range(NUMBER_OF_GAMES)):
    driver.get(URL)
    time.sleep(2)

    driver.find_element_by_css_selector('button[data-qa=start-game-button]').click()
    time.sleep(5)

    file_paths = []

    for i in range(5):
        driver.refresh()

        el = driver.find_element_by_css_selector('#__NEXT_DATA__')
        html = el.get_attribute('innerHTML')
        data = json.loads(html)
        rounds = data['props']['pageProps']['game']['rounds']

        print(rounds[-1]['lat'], rounds[-1]['lng'])
        gmap_url = f'https://google.com/maps/place/{rounds[-1]["lat"]},{rounds[-1]["lng"]}'
        driver.execute_script(f'window.open("{gmap_url}")')

        input()

driver.close()
