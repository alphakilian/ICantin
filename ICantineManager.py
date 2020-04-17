import sys
from ICantineLoginPage import ICLoginPage
from ICantineManagerMenu import ICantineManagerMenu

# Initialize DB
#login_status = 0
#lp = ICLoginPage()

#lp.topPage(login_status)

#if (login_status == 0):
#    print("Login failed!")
#    sys.exit()

mm = ICantineManagerMenu()
mm.DrawMenu()



