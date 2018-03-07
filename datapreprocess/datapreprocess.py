import io,csv

keyBase=['SP.POP.80UP','SP.POP.7579','SP.POP.7074','SP.POP.6569','SP.POP.6064','SP.POP.5559','SP.POP.5054','SP.POP.4549','SP.POP.4044','SP.POP.3539','SP.POP.3034','SP.POP.2529','SP.POP.2024','SP.POP.1519','SP.POP.1014','SP.POP.0509','SP.POP.0004','SP.DYN.CDRT.IN','SP.DYN.CBRT.IN','SP.DYN.TO65.MA.ZS','SP.DYN.TO65.FE.ZS']
popkey='SP.POP'
ClusterDict={}#国家名称指向聚类区域
Clusters=[]#统计有哪些聚类
def readDict(fileName):
    f=open(fileName)
    r=csv.reader(f)
    for i in r:
        ClusterDict[i[1]]=i[0]
        nothave=True
        for j in Clusters:
            if j==i[0]:
                nothave=False
                break
        if nothave:
            Clusters.append(i[0])

def gravity(fileName,Table=True):
    data=[]
    cnt=-1
    maxlen=-1
    for key in keyBase:
        first=True
        loader=open(fileName+'.csv','r',encoding='utf-8')
        reader=csv.reader(loader)
        counter=0
        for csvR in reader:
            if Table:
                data.append(csvR[0:])
                maxlen=len(csvR)
                cnt+=1
                Table=False
            if len(csvR)>2 and (key in csvR[1]):
                counter+=1
                if first:
                    first=False
                    data.append([])
                    cnt+=1
                    data[cnt].append(csvR[0])
                    data[cnt].append(key)
                    for i in range(2,maxlen):
                        if i>len(csvR) or csvR[i]=='':data[cnt].append(0.0)
                        else:data[cnt].append(float(csvR[i]))
                else:
                    for i in range(2,len(csvR)):
                        if csvR[i]!='':
                            data[cnt][i]+=float(csvR[i])
        if counter!=0:
            for i in range(2,maxlen):
                data[cnt][i]/=float(counter)
    saver=open('gravity/'+fileName+'.csv','w',newline='',encoding='utf-8')
    writer=csv.writer(saver)
    writer.writerows(data)

readDict('ClusterOfCountry.csv')
for i in Clusters:
    gravity(i)
#SM.POP.NETM