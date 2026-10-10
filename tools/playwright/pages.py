import os
import time

import allure
from playwright.sync_api import Playwright, Page

from config import settings


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        storage_state: str | None = None
) -> Page:
    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=storage_state,
        record_video_dir=settings.videos_dir
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    yield page

    context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))
    browser.close()

    allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trace', extension='zip')
    allure.attach.file(wait_for_video(page), name='video', attachment_type=allure.attachment_type.WEBM)


def wait_for_video(page: Page, timeout: float = 5.0) -> str:
    """Дождаться, пока Playwright допишет файл видео.

    На Windows browser.close() возвращает управление раньше, чем видео
    оказывается на диске: page.video.path() указывает на файл нулевого
    размера, и allure прикрепляет пустышку. Обычно хватает ~0.2 секунды.
    """
    path = page.video.path()
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            break
        time.sleep(0.1)
    return path
