import win32clipboard, sqlite3

try:
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    if data == '':
        print("None")
    print(data[0]) # testing
    print(data[1]) # testing
    test = ''.join(data)
    print(test)
    print('--'+data+'--')


except TypeError as e:
    pass
    print(e)