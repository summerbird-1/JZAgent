import re
import sys
import traceback
from Agent.utils.logger import agent_logger as logger


def print_traceback():
    logger.error(''.join(traceback.format_exception(*sys.exc_info())))


def has_chinese_chars(data) -> bool:
    text = f'{data}'
    return len(re.findall(r'[\u4e00-\u9fff]+', text)) > 0