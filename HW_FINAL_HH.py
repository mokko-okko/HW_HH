import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime

dataset="dst-3.0_16_1_hh_database.csv"

mdf=pd.read_csv(dataset,delimiter=";")
df=mdf.copy()



"""
пол возраст ,  дата рождения
##########################################################################################
"""
df["gender"]=list(map(lambda x:x.split(",")[0][0],df["Пол, возраст"]))
df["Возраст"]=list(map(lambda x:int(x.split(",")[1].split()[0]),df["Пол, возраст"]))



	
s="родился 27 ноября 1979"
def date_of_born(s1):
    s=s1.split(",")[2]
    month={"января":'1',"февраля":'2',"марта":'3',"апреля":'4',"мая":'5',"июня":'6',"июля":'7',"августа":'8',"сентября":'9',"октября":'10',"ноября":'11',"декабря":'12'}
    tmp=s.split()
    m=s.split()[2]
    m_num=month[m]
    #date=pd.to_datetime()    
    date_str=tmp[1]+"-"+m_num+"-"+tmp[3]
    return pd.to_datetime(date_str , dayfirst=True)    

df["date_of_born"]=list(map(date_of_born,df["Пол, возраст"]))
df["date_of_born"]=list(map(lambda x:x.date(),df["date_of_born"]))
#df.pop("Пол, возраст")


"""
### ##########################################################################################
обработка зарплаты "ЗП"
"""



tmp = list(map(lambda x:x.split()[1],df["ЗП"]))
crncy_txt=["EUR","KGS","AZN","грн.","бел.руб.","сум","USD","KZT","руб."]

crncy_iso=["EUR","KGS","AZN","UAH","BYN","UZS","USD","KZT","RUB"]
crncy_proportion=[1,10,1,10,1,10000,1,100,1]
crncy_des=["евро",
           "киргизский сом",
           "азербайджанский манат",
           "гривна",
           "белорусский рубль",
           "узбекский сум",
           "доллар",
           "казахстанский тенге",
           "российский рубль"]
                      
crncy_rate=[98.8767,
            10.1475,
            53.3819,
            23.7151,
            28.299,
            72.5364,
            90.7493,
            20.2783,
            1 ]

crncy_df=pd.DataFrame(index=crncy_txt)
crncy_df["ISO"]=crncy_iso
crncy_df["proportion"]=crncy_proportion
crncy_df["des"]=crncy_des
crncy_df["rate"]=crncy_rate
crncy_df["rate_date"]="08/10/2024"

currncy_dict=dict(zip(crncy_txt,zip(crncy_iso,crncy_proportion,crncy_des,crncy_rate)))

df["salary"]=list(map(lambda x:float(x.split()[0]),df["ЗП"]))


def salary_crncy(s):
    key=s.split()[1]
    return currncy_dict[key][0]

df["salary_crncy"]=list(map(salary_crncy,df["ЗП"]))

def salary_crncy_proportion(s):
    key=s.split()[1]
    return currncy_dict[key][1]
df["salary_proportion"]=list(map(salary_crncy_proportion,df["ЗП"]))

def salary_crncy_rate(s):
    key=s.split()[1]
    return currncy_dict[key][3]
df["salary_crncy_rate"]=list(map(salary_crncy_rate,df["ЗП"]))



rates=pd.read_csv("ExchangeRates.csv")
rates["date"]=list(map(lambda x:pd.to_datetime(x.split(" ")[0], dayfirst= True),rates["date"]))
a=df[["Обновление резюме","salary_crncy"]]
a["Обновление резюме"]=list(map(lambda x: x.replace(".","/"),a["Обновление резюме"]))
a["Обновление резюме"]=list(map(lambda x:pd.to_datetime(x.split(" ")[0], dayfirst= True),a["Обновление резюме"]))

a=a.rename(columns={"Обновление резюме":"date","salary_crncy":"currency"})
aa=a.merge(rates, on=["date","currency"], how="left").fillna(1)

df["salary_crncy_rate"]=aa["close"]
df["ЗП (руб)"]=df["salary"]/df["salary_proportion"]*df["salary_crncy_rate"]



"""
### ##########################################################################################
опыт работы в месяцах
"""

st =	"Опыт работы 12 лет 8 месяцев  Июль 2014 — по настоящее время 4 года 11 месяцев ОАО ""Барнаульский пивоваренный завод"" Барнаул , bpz.su Продукты питания ... Безалкогольные напитки (производство) Пиво (производство) Системный администратор Поддерживаю и развиваю ИТ-инфрастуктуру предприятия, включающую в себя: Кластер Vmware Vsphere, Серверы Windows и Linux, Active Directory, Сервер 1С и MS-SQL, локальную сеть предприятия, системы видеонаблюдения и контроля доступа. Техподдержка пользователей (все уровни).  Декабрь 2008 — Июль  2014 5 лет 8 месяцев ООО ""ТД Шкуренко"" Барнаул Продукты питания ... Безалкогольные напитки (продвижение, оптовая торговля) Снеки (продвижение, оптовая торговля) Системный администратор Администрирование серверов Windows 2003 и 2012, Active Directory, серверов на Linux, мини-АТС Панасоник, поддержка пользователей.  Сентябрь 2006 — Октябрь  2008 2 года 2 месяца ООО ""Си-Трейд"" Барнаул Электроника, приборостроение, бытовая техника, компьютеры и оргтехника ... Электронно-вычислительная, оптическая, контрольно-измерительная техника, радиоэлектроника, автоматика (монтаж, сервис, ремонт) инженер по ремонту ноутбуков Ремонт ноутбуков и КПК, преимущественно гарантийный, в основном - отверточный блочный. Заказ запчастей, составление отчётов для вендоров."
s1="Опыт работы 1 год"
s2="Опыт работы 1 год 5 месяц"
s3="Опыт работы 1 лет 3 месц "
s4="Опыт работы 1 год bv sdf"
s5="Опыт работы 1 месяц"



def get_experience(s):
    if type(s)!=str:
        return np.nan
    if type(s)==np.nan:
        return np.nan
    if s=="Не указано":
        return np.nan
    
    tmp=s.split()
    month=0
    if tmp[3].startswith('мес'):
        return int(tmp[2])         
    
    if (tmp[3].startswith('го')) or (tmp[3].startswith('ле')):
         month=int(tmp[2])*12         
    
    if len(tmp)<5:
        return month
    
    if tmp[5].startswith('ме'):
        try: 
            return month+int(tmp[4])
        except:
            return month
    else:    
        return month
 

df["Опыт работы (месяц)"]=list(map(get_experience,df["Опыт работы"]))        








#########################################
###образование и вуз
#########################################
def get_institute(s):
    if type(s)!=str:
        return np.nan
    if type(s)==np.nan:
        return np.nan
    if s=="Не указано":
        return np.nan
    
    tmp=s.split()
    if tmp[0].startswith('Нео'):
        return "неоконченное высшее"
    elif tmp[0].startswith('Вы'): 
        return "высшее"
    elif tmp[0].startswith('Сре'): 
        if tmp[1].startswith('спе'):
            return "среднее специальное"
        else: 
            return "среднее"
        
df["образование"]=list(map(get_institute,df["Образование и ВУЗ"]))            



###########командировки#############
"""
 <Город , (метро) , готовность к переезду (города для переезда) , готовность к командировкам>
"""



df["Готовность к переезду"]=list(map(lambda x:  False if x.split(',')[-2].startswith(' не') else True, df["Город, переезд, командировки"]))
df["Готовность к командировкам"]=list(map(lambda x:  False if x.split(',')[-1].startswith(' не') else True, df["Город, переезд, командировки"]))
df['3']=df["Готовность к переезду"]*df["Готовность к командировкам"]
df["Город"]=list(map(lambda x:  x.split(' ')[0], df["Город, переезд, командировки"]))


tmp=df["Занятость"].values
job=["полная занятость","частичная занятость", "проектная работа","стажировка", "волонтерство"]

k=0
res=np.zeros([len(tmp),len(job)])
for i in tmp:
    for j in range(0,len(job)):
        for jj in i.split(", "):
             if jj==job[j]:
                 res[k,j]=1
    k+=1    

a=res[:,2]*res[:,4]


for i in range(0,len(job)-1):
    df[job[i]]=res[:,i]


#print(sum(res[:,2]*res[:,4]))
#a=res[:,2]+res[:,4]

tmp=df["График"].values
job=["полный день","сменный график", "удаленная работа","гибкий график", "вахтовый метод"]

k=0
res2=np.zeros([len(tmp),len(job)])
for i in tmp:
    for j in range(0,len(job)):
        for jj in i.split(", "):
             if jj==job[j]:
                 res2[k,j]=1
    k+=1    


print(sum(res2[:,3]*res2[:,4]))

for i in range(0,len(job)-1):
    df[job[i]]=res2[:,i]


print(df["Возраст"].mode())
print(df["Опыт работы (месяц)"].max())

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'

##диаграмма с ЗП более 1 млн

fig=px.histogram(df,x="ЗП (руб)")
fig.show()    



import plotly.express as px
import plotly.graph_objects as go

import plotly.io as pio
pio.renderers.default='browser'

from plotly.subplots import make_subplots


# формируем экран экран с двумя  графиками
fig = make_subplots(rows=1,cols=2,  specs=[
                                    [{"type": "box"}, {"type": "histogram"}],
                                           ]  
                    )

# добавляем даные на графики
fig.add_trace(go.Box( y=df["Возраст"] , name="Возраст", ),   row=1, col=1)
fig.add_trace(go.Histogram(x=df["Возраст"], name="Возраст"), row=1, col=2)
fig.add_vline(x=df["Возраст"].median(), line_dash = 'dash', line_color = 'firebrick',row=1, col=2) #вертикаьная линия с медианным значением


# добаялем названия осей и титлы графиков
fig.update_layout(  title="Распределение возрастов соискателей" )  #название всего

#fig.update_xaxes(title_text="Возраст", row=1, col=1)
fig.update_xaxes(title_text="Возраст", row=1, col=2)
fig.update_yaxes(title_text="Кол-во соответствующего возраста", row=1, col=2)
fig.update_yaxes(title_text="Возраст", row=1, col=1)


#fig.show()    










tmp=df[df["ЗП (руб)"]<1000000].groupby(["образование"])["ЗП (руб)"].median()
fig=px.bar(tmp, color=tmp.index)
fig.update_layout(title="Зависимость зарплатных ожиданий от уровня образования",
                  xaxis_title="Образование",
                  yaxis_title="Ожидаемая ЗП")
                 
fig.show()    


###города###



def city_cat(s):
    l1=["Москва","Санкт-Петербург"]
    l2=["Новосибирск","Екатеринбург","Нижний Новгород","Казань","Челябинск","Омск","Самара","Ростов-на-Дону","Уфа","Красноярск","Пермь","Воронеж","Волгоград"]
    
    if s in l1:
        return s
        
    if s in l2:
        return "город-миллионник"
    else:
        return "другие"

        
df["Город"]=list(map(city_cat,df["Город"]))

tmp4=df[df["ЗП (руб)"]<1000000]
fig = px.box(tmp4, x="Город", y="ЗП (руб)", color="Город")
fig.update_layout(title="Сравнение зарплатных ожиданий по городам",
                  xaxis_title="Города(категории)",
                  yaxis_title="Ожидаемая ЗП")
fig.show()    


bar_data = df.groupby(
    ['Готовность к командировкам', 'Готовность к переезду'],
    as_index=False
)['ЗП (руб)'].median()


df[(df["Готовность к переезду"]==True) & (df["Готовность к командировкам"]==True)]["ЗП (руб)"].median()
tmp5=df[(df["3"]==True)]["salary"]

tmp6=df.groupby(["Готовность к переезду","Готовность к командировкам"], as_index=False)["ЗП (руб)"].median()
fig = px.bar(
    data_frame=tmp6,
    y='Готовность к переезду',
    x='ЗП (руб)',
    barmode="group",
    color='Готовность к командировкам',
    #orientation='h',
    title='Медианная з/п по готовности к командировкам/переезду'
)
fig.show()


tmp7=df.pivot_table(columns="Возраст",index="образование",values="ЗП (руб)",aggfunc="median")
fig = px.imshow(tmp7)
fig.show()


tmp8=df[["Возраст","Опыт работы (месяц)"]]
tmp8["Опыт работы (лет)"]=(tmp8["Опыт работы (месяц)"]/12)
#fig1=px.scatter(x=tmp8["Опыт работы (месяц)"], y=tmp8["Возраст"])
fig1=px.scatter(tmp8,x="Опыт работы (лет)", y="Возраст")
x=np.arange(0,101)
y=np.arange(0,101)
fig2=px.line(x,y)
#fig2.show()
fig3 = go.Figure(data=fig1.data + fig2.data)
fig3.update_layout(title="Зависимость опыта работы и возраста",
                  xaxis_title="Возраст",
                  yaxis_title="Опыт работы (лет)")

fig3.show()

tmp8[tmp8["Опыт работы (месяц)"]>tmp8["Возраст"]]


dupl = df[df.duplicated ()] # значения не бются с эталонными, дубликатов на датасете 153 и ни каплей больше. Эталонного ответа 155 добится можно только колдоством

df1=df.copy()

df1=df1.drop_duplicates()

df1= df1.dropna(axis='index', how='any', subset=['Последнее/нынешнее место работы',"Последняя/нынешняя должность"])

df1["Опыт работы (месяц)"].fillna(value=df1["Опыт работы (месяц)"].median())
df1["Опыт работы (месяц)"].mean()
tmp=df1[(df1["ЗП (руб)"]>1000000)].index
tmp2=df1[(df1["ЗП (руб)"]<1000)].index
df1=df1.drop(tmp)
df1=df1.drop(tmp2)

tmp3=tmp8[tmp8["Опыт работы (месяц)"]>tmp8["Возраст"]].index
df1=df1.drop(tmp3)


###5.6
tmp8=df1[["Возраст","Опыт работы (месяц)"]]
def outliers_z_score_mod(data, feature, log_scale=False,left=3,right=3):
    if 0 in data[feature]:
        ddata = data[feature]+1
    else:
        ddata = data[feature]    
    
    if log_scale:
        x = np.log(ddata)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x >= lower_bound) & (x <= upper_bound)]
    return outliers, cleaned

outliers, cleaned = outliers_z_score_mod(tmp8, "Возраст", log_scale=True,left=3,right=4)

fig1=px.histogram(np.log(tmp8["Возраст"]), facet_col_spacing=0.1)
x=np.log(tmp8["Возраст"]).mean()
fig1.add_vline(x=x)
fig.update_layout(title="Сравнение зарплатных ожиданий по городам",
                  xaxis_title="Города(категории)",
                  yaxis_title="Ожидаемая ЗП")

fig1.show()

fig.write_image("images/fig1.jpeg")
fig.write_image("images/fig1.pdf")
