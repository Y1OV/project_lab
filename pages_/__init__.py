from collections import namedtuple
from .resume_info import main as resume_info
from .main import main as main


Page = namedtuple("Page", "title method")

pages: dict[str, Page] = {
    'Главная': Page(title="Главная", method=main),
    'Resume_info': Page(title="Resume info", method=resume_info),

}
