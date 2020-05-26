#!D:\projects\py\git_python\smc_script\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'codecov==2.1.3','console_scripts','codecov'
__requires__ = 'codecov==2.1.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('codecov==2.1.3', 'console_scripts', 'codecov')()
    )
