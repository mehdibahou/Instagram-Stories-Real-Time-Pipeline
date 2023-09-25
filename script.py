from seleniumwire import webdriver  # Import from seleniumwire
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scraper(user):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)

    def cookiegetter(a):
        cookies_dict = {}
        for cookie in a.split(";"):
            cookies_dict[cookie.split("=")[0]] = cookie.split("=")[1]
        return cookies_dict

    # Go to the Google home page
    driver.get('https://instanavigation.com/profile/fdsbamo')

    # Access requests via the `requests` attribute

    for request in driver.requests:
        if request.headers['x-xsrf-token'] != None:
            xsrftoken = request.headers['x-xsrf-token']
            break

    for request in driver.requests:
        if request.response:
            if request.headers['cookie'] != None:
                useragent = request.headers['user-agent']
                XSRFTOKEN = cookiegetter(request.headers['cookie'])[
                    "XSRF-TOKEN"]
                laravel_session = cookiegetter(request.headers['cookie'])[
                    " laravel_session"]
                break

    url = "https://instanavigation.com/get-user-info"

    # Set the headers
    headers = {
        "x-xsrf-token": xsrftoken

    }

    # Set the cookies
    cookies = {
        "laravel_session": laravel_session,
        "XSRF-TOKEN": XSRFTOKEN,
        "user-agent": useragent
    }
    payload = {
        "userName": user,

    }

    # Make the request
    response = requests.post(url, headers=headers,
                             cookies=cookies, json=payload)

    # Check the status code of the response
    if response.status_code == 200:
        # Process the response data
        data = response.json()
        print(data)
        return data['lastStories']
    else:
        # Handle the error
        print("Error Error Error Error Error Error")
        return "error"
