from enum import Enum


class Browser(Enum):
    CHROME = "chromedriver"
    CHROME_UNDETECTED = "chrome_undetected"
    FIREFOX = "geckodriver"


class SelectorType(Enum):
    SELENIUM = "selenium"
    SOUP = "soup"
