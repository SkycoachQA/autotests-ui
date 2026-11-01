import platform
import sys

from config import settings


def create_allure_environment_file():
    values = settings.model_dump()
    # Пароль не должен попадать в распространяемый отчёт.
    values['test_user']['password'] = '***'
    items = [f'{key}={value}' for key, value in values.items()]
    items.extend([
        f'os_info={platform.system()}, {platform.release()}',
        f'python_version={sys.version}',
    ])
    # Обратные слеши в путях Windows экранируются по формату properties.
    properties = '\n'.join(item.replace('\\', '\\\\') for item in items)
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w', encoding='utf-8') as file:
        file.write(properties)
