from selenium import webdriver
import time, json, os
from datetime import datetime
from tqdm import tqdm

# URL = 'https://www.geoguessr.com/maps/south-korea/play'
URL = 'https://www.geoguessr.com/maps/famous-places/play'

start_time = datetime.now().strftime('%Y%m%d_%H%M%S')

os.makedirs(f'dataset/{start_time}', exist_ok=True)

NUMBER_OF_GAMES = 10000
SCREENSHOT_SIZE = 800
NUMBER_OF_SCREENSHOTS = 4
EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS'
PASSWORD = 'YOUR_PASSWORD'

driver = webdriver.Chrome('/Users/brad/Development/bdf_code/ai-geoguessr/chromedriver')
driver.set_window_position(0, 0)
driver.set_window_size(SCREENSHOT_SIZE, SCREENSHOT_SIZE + 171)

# login
driver.get('https://www.geoguessr.com/signin')
input = driver.find_element_by_css_selector("input[name=email]")
input.send_keys(EMAIL_ADDRESS)
input = driver.find_element_by_css_selector("input[name=password]")
input.send_keys(PASSWORD)
input.submit() 
time.sleep(1)

def screenshot_canvas(file_path):
    '''
    Take a screenshot of the streetview canvas.
    '''
    with open(file_path, 'xb') as f:
        canvas = driver.find_element_by_tag_name('canvas')
        f.write(canvas.screenshot_as_png)


def rotate_canvas():
    '''
    Drag and click the <main> elem a few times to rotate us ~90 degrees.
    '''
    main = driver.find_element_by_tag_name('main')
    for _ in range(0, 5):
        action = webdriver.common.action_chains.ActionChains(driver)
        action.move_to_element(main) \
            .click_and_hold(main) \
            .move_by_offset(118, 0) \
            .release(main) \
            .perform()


def move_to_next_point():
    '''
    Click one of the next point arrows, doesn't matter which one
    as long as it's the same one for a session of Selenium.
    '''
    next_point = driver.find_element_by_css_selector('[fill="black"]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.click(next_point).perform()



for _ in tqdm(range(NUMBER_OF_GAMES)):
    driver.get(URL)
    time.sleep(2)

    driver.find_element_by_css_selector('button[data-qa=start-game-button]').click()
    time.sleep(5)

    file_paths = []

    for i in range(5):
        # for _ in range(0, NUMBER_OF_SCREENSHOTS):
        #     file_path = f'dataset/{start_time}/{int(time.time())}.png'
        #     screenshot_canvas(file_path)
        #     move_to_next_point()
        #     rotate_canvas()

        file_path = f'dataset/{start_time}/{int(time.time())}.png'
        screenshot_canvas(file_path)
        file_paths.append(file_path)

        if i >= 4:
            break

        driver.find_element_by_css_selector('.guess-map__canvas-container').click()
        time.sleep(0.5)
        driver.find_element_by_css_selector('.guess-map__guess-button > .button').click()
        time.sleep(2)
        try:
            driver.find_element_by_css_selector('button[data-qa=confirmation-dialog-continue]').click()
            time.sleep(0.5)
        except:
            pass
        driver.find_element_by_css_selector('button[data-qa=close-round-result]').click()
        time.sleep(2)

    driver.refresh()

    el = driver.find_element_by_css_selector('#__NEXT_DATA__')
    html = el.get_attribute('innerHTML')
    data = json.loads(html)

    '''
    [{'lat': 37.38809585571289, 'lng': 127.00364685058594, 'panoId': '756C70622D6A34324135625362475442524D48597277', 'heading': 0, 'pitch': 0, 'zoom': 0, 'streakLocationCode': None}]
    '''
    rounds = data['props']['pageProps']['game']['rounds']

    for i in range(len(rounds)):
        rounds[i]['img_path'] = os.path.basename(file_paths[i])

    with open(f'dataset/{start_time}/metadata_{int(time.time())}.json', 'w') as f:
        json.dump(rounds, f)

driver.close()
