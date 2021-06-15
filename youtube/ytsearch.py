from youtubesearchpython import *

VSearch = VideosSearch('pewdiepie')#,limit = 3)
count = 0
i= 0

result = VSearch.result()
while(count<60):
    try:
        print(f"\n{count+1} ) ",result['result'][i]['id'])
        i+=1
        count+=1
    except:
        # i=03
        # count+=len(result['result'])
        print("\n####################### COUNT #######################\n\t",count)
        VSearch.next()
        result = VSearch.result()
        i=0