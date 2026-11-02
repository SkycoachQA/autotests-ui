import allure
from playwright.sync_api import Locator, expect

from ui_coverage_tool import ActionType

from elements.base_element import BaseElement

from tools.logger import get_logger

logger = get_logger("INPUT")


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return "input"

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        return super().get_locator(nth, **kwargs).locator('input')

    def get_raw_locator(self, nth: int = 0, **kwargs) -> str:
        return f'{super().get_raw_locator(nth, **kwargs)}//input'

    def fill(self, value: str, nth: int = 0, **kwargs):
        display_value = "***" if "password" in self.locator.lower() else value
        step = f'Fill {self.type_of} "{self.name}" to value "{display_value}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            locator.fill(value)

        self.track_coverage(ActionType.FILL, nth, **kwargs)

    def check_have_value(self, value: str, nth: int = 0, **kwargs):
        display_value = "***" if "password" in self.locator.lower() else value
        step = f'Checking that {self.type_of} "{self.name}" has a value "{display_value}"'

        with allure.step(step):
            logger.info(step)
            locator = self.get_locator(nth, **kwargs)
            expect(locator).to_have_value(value)

        self.track_coverage(ActionType.VALUE, nth, **kwargs)
