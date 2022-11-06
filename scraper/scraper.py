import time
import requests
import cloudscraper
from pathlib import Path
from urllib.parse import urlparse
from selenium import webdriver
import pdb

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from . import settings
from . import enums
from . import utils
from . import settings as db_settings
from . import db_enums as db_enums


# actor_id = db_settings.ACTOR_SETTINGS["id"]

# default_catalog_obj = db_settings.DEFAULT_CATALOG_OBJ


class BaseScraper:
    def __init__(self, super_catalog=None):
        self.browser = settings.BROWSER
        self.super_catalog = super_catalog
        self.super_catalog_config = settings.SUPER_CATALOG_TEMPLATES[super_catalog]
        self.is_logged_in = False
        self.brand_counter = 0
        self.item_counter = 0
        self.current_brand = None
        self.brands = []
        self.items = []
        self.urls = []
        self.processed_urls = []

    def exec_methods(self, config):
        for method in config["methods"]:
            try:
                eval(method)
            except Exception as e:
                print(e)
                pass

    def fetch_brand_a_tags(self, a_tags):
        for a_tag in a_tags:
            try:
                name = a_tag.text
                url = a_tag["href"]
                self.add_brand(name, url)
            except:
                pass

    def add_brand(self, name, url):
        self.brand_counter += 1
        item = {
            "name": utils.clean_text(name),
            "catalogUrl": url,
            "type": db_enums.CatalogType.Catalog.value,
            "actorSchedule": db_enums.ActorSchedules.Every7Days.value,
        }
        self.brands.append(item)

    def process_brands(self, url):
        brands_config = self.super_catalog_config["brands"]
        self.scrape_web_page(url)
        self.exec_methods(brands_config)
        self.process_brand_page()

    def process_listing(self, url):
        items_config = self.super_catalog_config["items"]
        self.scrape_web_page(url)
        self.exec_methods(items_config)
        self.process_listing_page()

    def process_items(self):
        items_config = self.super_catalog_config["items"]
        if items_config["is_required"]:
            for brand in self.brands:
                url = brand["catalogUrl"]
                print(f"processing brand url: {url}")
                self.scrape_web_page(url)
                self.exec_methods(items_config)
                self.process_item_pages()

    def process(self):
        self.process_brands()
        self.brands = utils.convert_class_objects_to_list_dic(self.brands)
        self.process_items()

    def end_process(self):
        self.quit_driver()


class SeleniumBaseScraper(BaseScraper):
    def __init__(self, super_catalog=None):
        super().__init__(super_catalog)
        self.driver = None
        self.profile = None
        self.options = None
        self.set_options()
        self.set_profile()
        self.set_proxy()
        self.set_driver()
        self.set_captcha_extension()
        self.login()

    def login(self):
        try:
            login_config = self.super_catalog_config["login"]
            if login_config["is_required"]:
                self.scrape_web_page(login_config["url"])
                self.exec_methods(login_config)
                self.is_logged_in = True
        except Exception as e:
            print(e)
            pass

    def set_driver(self):
        if self.browser == enums.Browser.FIREFOX.value:
            self.driver = webdriver.Firefox(
                firefox_profile=self.profile,
                executable_path=GeckoDriverManager().install(),
                options=self.options,
            )
        elif self.browser == enums.Browser.CHROME.value:
            self.driver = webdriver.Chrome(options=self.options)
        elif self.browser == enums.Browser.CHROME_UNDETECTED.value:
            self.driver = uc.Chrome(
                version_main=settings.CHROME_UNDETECTED_VERSION, options=self.options
            )

    def set_options(self):
        if self.browser == enums.Browser.FIREFOX.value:
            self.options = webdriver.FirefoxOptions()
            # self.options.add_argument("--private")
        elif self.browser == enums.Browser.CHROME.value:
            self.options = webdriver.ChromeOptions()
            # self.options.add_argument(f"user-agent={utils.get_user_agent()}")
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--disable-dev-shm-usage")
            self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_prefs = {"profile.default_content_settings": {"images": 2}}
            self.options.experimental_options["prefs"] = chrome_prefs
            self.options.add_argument("--headless")
            preferences = {
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False,
            }
            self.options.add_experimental_option("prefs", preferences)
            if settings.CHROME_PROFILE:
                self.options.add_argument(
                    f"--profile-directory={settings.CHROME_PROFILE_NAME}"
                )
                self.options.add_argument(
                    settings.CHROME_PROFILE_DIR_PATH
                )  # Path to your chrome profileath to your chrome profile

        elif self.browser == enums.Browser.CHROME_UNDETECTED.value:
            self.options = webdriver.ChromeOptions()
            self.options.add_argument(f"user-agent={utils.get_user_agent()}")
            preferences = {
                "webrtc.ip_handling_policy": "disable_non_proxied_udp",
                "webrtc.multiple_routes_enabled": False,
                "webrtc.nonproxied_udp_enabled": False,
            }
            self.options.add_experimental_option("prefs", preferences)

    def set_profile(self):
        if self.browser == enums.Browser.FIREFOX.value:
            self.profile = webdriver.FirefoxProfile()
            self.profile.set_preference(
                "general.useragent.override", utils.get_user_agent()
            )
            # You would also like to block flash
            self.profile.set_preference(
                "dom.ipc.plugins.enabled.libflashplayer.so", False
            )
            self.profile.set_preference("media.peerconnection.enabled", False)
            self.profile.update_preferences()

    def set_proxy(self):
        if settings.PROXY:
            proxy = utils.get_random_proxy()
            proxy_ip, proxy_port = proxy.split(":")

            if self.browser == enums.Browser.FIREFOX.value:
                self.profile.set_preference("network.proxy.type", 1)
                self.profile.set_preference("network.proxy.http", str(proxy_ip))
                self.profile.set_preference("network.proxy.http_port", int(proxy_port))
                self.profile.set_preference("network.proxy.ssl", str(proxy_ip))
                self.profile.set_preference("network.proxy.ssl_port", int(proxy_port))
                self.profile.set_preference("network.proxy.ftp", str(proxy_ip))
                self.profile.set_preference("network.proxy.ftp_port", int(proxy_port))
                self.profile.set_preference("network.proxy.socks", str(proxy_ip))
                self.profile.set_preference("network.proxy.socks_port", int(proxy_port))
                self.profile.set_preference("network.http.use-cache", False)
                self.profile.set_preference("network.proxy.socks_remote_dns", True)
                self.profile.set_preference("places.history.enabled", False)
                self.profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
                self.profile.set_preference("privacy.clearOnShutdown.passwords", True)
                self.profile.set_preference(
                    "privacy.clearOnShutdown.siteSettings", True
                )
                self.profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
                self.profile.set_preference("signon.rememberSignons", False)
                self.profile.set_preference("network.cookie.lifetimePolicy", 2)
                self.profile.set_preference("network.dns.disablePrefetch", True)
                self.profile.set_preference("network.http.sendRefererHeader", 0)
                self.profile.set_preference("javascript.enabled", True)
                self.profile.set_preference("permissions.default.image", 2)
                self.profile.update_preferences()
            elif self.browser == enums.Browser.CHROME.value:
                self.options.add_argument("--proxy-server=%s" % proxy)
            elif self.browser == enums.Browser.CHROME_UNDETECTED.value:
                self.options.add_argument("--proxy-server=%s" % proxy)

    def set_captcha_extension(self):
        if settings.CAPTCHA_EXTENSION:
            if self.browser == enums.Browser.FIREFOX.value:
                self.driver.install_addon(
                    (str(Path(settings.CAPTCHA_EXTENSION_PATH).absolute()))
                )

                utils.random_sleep(3, 10)

                utils.acp_api_send_request(
                    self.driver,
                    "setOptions",
                    {"options": {"antiCaptchaApiKey": settings.CAPTCHA_EXTENSION_KEY}},
                )

    def render_browser(self):
        height = utils.get_random_number(1200, 1400)

        width = utils.get_random_number(1200, 1400)

        self.driver.set_window_size(width, height)

    def resolve_captcha(self):
        if settings.CAPTCHA_EXTENSION:
            try:
                WebDriverWait(self.driver, utils.get_random_number(100, 120)).until(
                    lambda x: x.find_element_by_css_selector(".antigate_solver.solved")
                )
            except Exception as e:
                pass

    def resolve_press_and_hold(self):
        try:
            element = self.driver.find_element("xpath", "//*[text()='Press & Hold']")
            action = ActionChains(self.driver)
            click = ActionChains(self.driver)
            action.click_and_hold(element)
            action.perform()
            utils.random_sleep(200, 210)
            action.release(element)
            action.perform()
            time.sleep(0.2)
            action.release(element)
        except Exception as ex:
            print(ex)
            pass

    def scroll_web_page(self):
        last_height = self.driver.execute_script(
            "return document.documentElement.scrollTop"
        )

        while True:
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

            new_height = self.driver.execute_script(
                "return document.documentElement.scrollTop"
            )
            if new_height == last_height:
                break
            last_height = new_height

        self.driver.execute_script("window.scrollTo(0, 0);")

    def scrape_web_page(self, url):
        utils.random_sleep(1, 3)
        self.render_browser()
        self.driver.get(url)
        WebDriverWait(self.driver, 100).until(
            lambda driver: self.driver.execute_script("return document.readyState")
            == "complete"
        )
        self.scroll_web_page()
        # self.resolve_captcha()
        # self.resolve_press_and_hold()

    def get_domain_url(self):
        url = self.driver.current_url
        parsed_uri = urlparse(url)
        return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)

    def get_page_source(self):
        return self.driver.page_source

    def get_page_source_as_soup(self):
        return BeautifulSoup(self.get_page_source(), "html5lib")

    def driver_click(self, by, path):
        elems = self.find_elements(by, path)
        elems[0].click()

    def driver_fill_input(self, by, path, text):
        elems = self.find_elements(by, path)
        elems[0].send_keys(text)

    def find_elements(self, by, path):
        return self.driver.find_elements(by, path)

    def quit_driver(self):
        self.driver.quit()


class CloudBaseScraper(BaseScraper):
    def __init__(self, super_catalog=None):
        super().__init__(super_catalog)
        self.scraper = None
        self.web_page_content = None
        self.web_page_url = None
        self.set_scraper()
        self.login()

    def login(self):
        pass

    def set_scraper(self):
        rand_num = utils.get_random_number(
            0, len(settings.CLOUD_SCRAPER_BROWSER_SETTING) - 1
        )
        self.scraper = cloudscraper.create_scraper(
            delay=utils.get_random_number(8, 15),
            browser=settings.CLOUD_SCRAPER_BROWSER_SETTING[rand_num],
        )

    def scrape_web_page(self, url):
        self.web_page_content = self.scraper.get(url).text
        self.web_page_url = url
        if not self.is_logged_in:
            self.login()

    def get_page_source_as_soup(self):
        return BeautifulSoup(self.web_page_content, "html5lib")

    def get_domain_url(self):
        parsed_uri = urlparse(self.web_page_url)
        return "{uri.scheme}://{uri.netloc}".format(uri=parsed_uri)

    def quit_driver(self):
        pass
