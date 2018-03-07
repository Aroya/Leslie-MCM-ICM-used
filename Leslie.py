import numpy as np
import csv,io
ClusterDict={}#国家名称指向聚类区域
Clusters=[]#统计有哪些聚类
Population=[]
Item=[]
birth=[0,0,0,0.11764705882352941176470588235294,#4
0.31372549019607843137254901960784,0.31372549019607843137254901960784,#2,6
0.1960784313725490196078431372549,0.01960784313725490196078431372549,#2,8
0,0,0,0,0,0,0,0,0,0,0,0]#12,20
birthIndex=[3,4,5,6,7]
baseYear=1967
baseYearStr='1967'
def getbaseYear():
    return 1967
def getbaseYearStr():
    return '1967'
global L
global S
global B
global P
#读取聚类词典
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

#default
global defaultSize
defaultSize=17
P=np.zeros((defaultSize,1))
S=np.zeros((defaultSize,defaultSize))
B=np.zeros((defaultSize,defaultSize))
L=np.zeros((defaultSize,defaultSize))

def clear():
    global defaultSize
    global L
    global S
    global B
    global P
    P=np.zeros((defaultSize,1))
    S=np.zeros((defaultSize,defaultSize))
    B=np.zeros((defaultSize,defaultSize))
    L=np.zeros((defaultSize,defaultSize))

#执行一次Leslie计算
def Leslie():
    global L
    global S
    global B
    global P
    L=S+B
    # print(L)
    # P=L*P
    P=np.dot(L,P)
    sum=0.0
    for i in P:
        for j in i:
            sum+=j
    return sum
#加载人口信息
def loadPopulation(fileName):
    f=open(fileName,'r',encoding='utf-8')
    r=csv.reader(f)
    for i in r:
        Population.append(i)
#加载每个地区的信息
def loadItem(fileName):
    Item.clear()
    f=open(fileName,'r',encoding='utf-8')
    r=csv.reader(f)
    for i in r:
        Item.append(i)

#保存矩阵
def save(fileName):
    global L
    global S
    global B
    global P
    np.savetxt('temp/'+fileName+'-'+'L.txt',L)
    np.savetxt('temp/'+fileName+'-'+'S.txt',S)
    np.savetxt('temp/'+fileName+'-'+'B.txt',B)
    np.savetxt('temp/'+fileName+'-'+'P.txt',P)

#加载矩阵
def load(fileName):
    global L
    global S
    global B
    global P
    L=np.loadtxt('temp/'+fileName+'-'+'L.txt')
    S=np.loadtxt('temp/'+fileName+'-'+'S.txt')
    B=np.loadtxt('temp/'+fileName+'-'+'B.txt')
    P=np.loadtxt('temp/'+fileName+'-'+'P.txt')

#找到类的索引
def searchPopulation(str):
    for i in range(0,len(Population)):
        if Population[i][0]==str:
            return i
    return -1

#加载信息到矩阵
def attach(fileName,year):
    global L
    global S
    global B
    global P
    popPs=-1
    itemPs=-1
    #确定是哪个簇
    Ps=searchPopulation(fileName)
    #找到列位置
    for i in range(0,len(Population[0])):
        if year==Population[0][i]:
            popPs=i
            break
    for i in range(0,len(Item[0])):
        if year==Item[0][i]:
            itemPs=i
            break
    if popPs<0 or itemPs<0 or Ps<0:
        print('Ps Error')
        print(str(popPs)+'\t'+str(itemPs)+'\t'+str(Ps))
        input()
    #加载到矩阵
    population=float(Population[Ps][popPs])
    #P
    #补正系数（原文件中 人口分布百分比和不为100）
    # fixK=0.0
    # for i in range(defaultSize,0,-1):
    #     fixK+=float(Item[i][itemPs])
    # fixK=1.0/fixK
    # fixKbefore=0.0
    # for i in range(defaultSize,0,-1):
    #     fixKbefore+=float(Item[i][itemPs-5])
    # fixKbefore=1.0/fixKbefore
    #补正系数不使用
    for i in range(defaultSize,0,-1):
        P[defaultSize-i][0]=population*float(Item[i][itemPs])/100
    #S
    #先计算存活率
    if popPs==1:
        print('year to small')
        input()
    
    for i in range(defaultSize,0,-1):
        if i==1:
            S[defaultSize-1][defaultSize-1]=S[defaultSize-1][defaultSize-2]
        else:
            lastPeriod=float(Population[Ps][popPs-1])*float(Item[i][itemPs-5])
            thisPeriod=float(Population[Ps][popPs])*float(Item[i-1][itemPs])
            S[defaultSize-i+1][defaultSize-i]=thisPeriod/lastPeriod
    #B
    #总出生率
    #出生率和死亡率建立在全体人口上
    #千分制转换
    # birthRate=(float(Item[defaultSize+2][itemPs])-float(Item[defaultSize+1][itemPs]))/1000.0
    birthRate=float(Item[defaultSize+2][itemPs])/1000.0*3.5
    # 平均到20岁-40岁
    # start=3
    # end=8
    # birthRate=birthRate*defaultSize/float(end-start)
    parents=0
    for i in birthIndex:
        parents+=P[i][0]
    zoom=population/parents*len(birthIndex)
    birthRate*=zoom
    for i in birthIndex:
        B[0][i]=birthRate*birth[i]
    #全分配
    # for i in range(0,defaultSize):
    #     B[0][i]=birthRate
    #L
    # print('P')
    # print(P)
    # print('S')
    # print(S)
    # print('B')
    # print(B)

loadPopulation('population.csv')
readDict('ClusterOfCountry.csv')
ans=[]
cnt=-1
for i in Clusters:
    clear()
    loadItem('datapreprocess/gravity/'+i+'.csv')
    attach(i,'1967')
    ans.append([])
    cnt+=1
    ans[cnt].append(i)
    for j in ['1972','1977','1982','1987','1992','1997','2002','2007','2012']:
        ans[cnt].append(Leslie())
        save(i+'-'+j)
    
f=open('Leslie/ans.csv','w',newline='',encoding='utf-8')
w=csv.writer(f)
w.writerows(ans)
#     pass
