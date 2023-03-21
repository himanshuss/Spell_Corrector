from time import sleep
import func
import pandas as pd
import numpy as np
import os
 

####
#master_file="master"
#slave_file="slave"
####


##reading the master and slave file
master_file=str(input("Master File name (xlsx format only):"))
ms=pd.read_excel("/Users/himanshusahrawat/Library/CloudStorage/OneDrive-O.P.JindalGlobalUniversity/Nestle/lib/"+master_file+".xlsx")

slave_file=str(input("Slave File name (xlsx format only):"))
sl=pd.read_excel("/Users/himanshusahrawat/Library/CloudStorage/OneDrive-O.P.JindalGlobalUniversity/Nestle/lib/"+slave_file+".xlsx")

##passing these files for some basic cleaning process
ms=func.clean_it(ms)
sl=func.clean_it(sl)

opt="0"

## Function Menu
while (opt!="4"):
    # Clearing the Screen
    func.clear()
    print("-"*100)
    print("#"*100)
    print("-"*100)
    print("1. Correct the Feild's Name to Standard Format")
    print("\n")
    print("2. Report Category Change")
    print("\n")
    print("3. Cross Feild Mapping")
    print("\n")
    print("4. Exit Menu")
    print("-"*100)
    print("#"*100)
    print("-"*100)
    opt=str(input("Please enter the option number: "))
    print("-"*100)

    if(opt=="1"):
        sl=func.mapp_it(ms,sl)
        sl.to_excel("/Users/himanshusahrawat/Library/CloudStorage/OneDrive-O.P.JindalGlobalUniversity/Nestle/results/updated.xlsx")

    if(opt=="2"):
        print("Coming Soon....")

    if(opt=="3"):
        print("Coming Soon....")

    if(opt=="4"):
        print("Take Care... Bye!!!")
        print("-"*100)

    else:
        print("Please Choose a Valid Input!!!   Wait.....")
        sleep(3)

