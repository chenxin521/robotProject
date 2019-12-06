#!E:\大三上半学期\小组项目\老师的项目\study-task\第三周\倒数第二版本git\robotProject\venv\Scripts\python.exe -x
# EASY-INSTALL-ENTRY-SCRIPT: 'pip==19.0.3','console_scripts','pip3.5'
__requires__ = 'pip==19.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pip==19.0.3', 'console_scripts', 'pip3.5')()
    )
