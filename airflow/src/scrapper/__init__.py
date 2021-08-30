
import urllib.parse
import json


import os

local_dir = os.path.dirname(os.path.abspath(__file__))

download_dir = os.path.join(local_dir, 'downloads')
def generate_maze(name, width, count=1):
    

    url = 'http://www.mazegenerator.net/'

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as ec
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support.select import Select


    EXE_PATH = os.path.join(
      local_dir,
      "chromedriver"
    )


    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--lang=en-us')
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--window-size=700x700")
    chrome_options.add_experimental_option('w3c', False)
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})

    driver = None
  
    try:
        driver = webdriver.Chrome(executable_path=EXE_PATH, options=chrome_options)
        # driver.set_window_size(700, 700)
        driver.get(url)
        import time 
        time.sleep(1)

        el = driver.find_element_by_id("S1WidthTextBox")
        el.clear()
        el.send_keys(str(width))

        el = driver.find_element_by_id("S1HeightTextBox")
        el.clear()
        el.send_keys(str(width))


        # function to handle setting up headless download
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

        for i in range(count):
          el = driver.find_element_by_id("GenerateButton")
          el.click()
          
          time.sleep(1)
          # image_url = driver.find_element_by_id("MazeDisplay").get_attribute("src")

          select_fr = Select(driver.find_element_by_id("FileFormatSelectorList"))
          select_fr.select_by_index(8)
          
          el = driver.find_element_by_id("DownloadFileButton")
          el.click()

          time.sleep(2)

          for root, dirs, files in os.walk(download_dir):
            for filename in files:
                # print(filename)
                if not 'renamed' in filename:
                  new_file_path = os.path.join(download_dir, 'maze_renamed_'+name+'_'+str(i)+'.png')
                  os.rename(
                    os.path.join(download_dir, filename),
                    new_file_path
                  )
                  print('downloaded', new_file_path)
                  yield new_file_path

    except Exception as exp:
        print(exp)
    finally:
      if driver:
        driver.close()


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", dest="picture_name", help="picture name")
    parser.add_argument("-p", "--params", dest="params",  default=None, help="params")

    args = parser.parse_args()

    if args.params:
        generate_picture(args.picture_name, json.loads(dummy_params))
    else:
        generate_picture(args.picture_name, dummy_params)
    
