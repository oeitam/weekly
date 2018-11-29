# oeitam

import sys
if 'C:\\Users\\oeitam\\VScode\\weekly' not in sys.path:
    sys.path.append(r'C:\Users\oeitam\VScode\weekly')

from test import test_defs_sections

# thsi code makes a fresh start in developement mode
#from os import remove as remove
#remove(r"C:\\weekly.local\\developement\\dfa.csv")
#remove(r"C:\\weekly.local\\developement\\dfm.csv")
#remove(r"C:\\weekly.local\\developement\\dft.csv")
#remove(r"C:\\weekly.local\\developement\\dfp.csv")
#remove(r"C:\\weekly.local\\developement\\ID")

test_commands = []
#test_commands.extend(test_defs_sections.test_commands_s1)
#test_commands.extend(test_defs_sections.test_commands_s2)
#test_commands.extend(test_defs_sections.test_commands_s3)

test_commands.append('die')



test_responses = []

