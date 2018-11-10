import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
t_data = pd.read_csv("Trans_data.csv")
t_data.info()
t_data.describe()
t_data.head()
tsample_date = t_data.sampled_date.unique()
result_df = pd.DataFrame({
    'Sample_number': [],
    'Text_id': [],
    'Sampled_date': [],
    'T_site': [],
    'T_plant': [],
    'Sampling_point': [],
    'CH4(ppm)': [],
    'H2(ppm)': [],
    'C2H2(ppm)': [],
    'C2H4(ppm)': [],
    'C2H6(ppm)': [],
    'CO(ppm)': [],
    'CO2(ppm)': [],
    'TDCG(ppm)': [],
    'Condition': [],
    'Fault': []
})
for udate in tsample_date:
    tunique_s_p=t_data[t_data.sampled_date==udate].sampling_point.unique()
    for tu_s_p in tunique_s_p:
        fault=[]
        condition=""
        execute=True
        Sample_number=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p)].sample_number.unique())
        Text_id=t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p)].text_id.unique()
        Sampled_date=udate
        T_site=t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p)].t_site.unique()
        T_plant=t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p)].t_plant.unique()
        Sampling_point=tu_s_p
        CH4=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Methane - CH4')].reported_value)
        H2=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Hydrogen - H2')].reported_value)
        C2H2=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Acetylene- C2H2')].reported_value)
        C2H4=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Ethylene - C2H4')].reported_value)
        C2H6=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Ethane - C2H6')].reported_value)
        CO=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Carbon Monoxide - CO')].reported_value)
        CO2=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='Carbon Dioxide - CO2')].reported_value)
        TDCG=float(t_data[(t_data.sampled_date==udate) & (t_data.sampling_point==tu_s_p) & (t_data.name=='TDCG')].reported_value)
        if((H2<=100) and (CH4<=120) and (C2H2<=1) and (C2H4<=50) and (C2H6<=65) and (CO<=350) and (CO2<=2500) and (TDCG<=720)):
            condition='Condition 1'
        else:
            if(((H2>=101) and (H2<=700)) or ((CH4>=121) and (CH4<=400)) or ((C2H2>=2) and (C2H2<=9)) or ((C2H4>=51) and (C2H4<=100)) or ((C2H6>=66) and (C2H6<=100)) or ((CO>=351) and (CO<=570)) or ((CO2>=2500) and (CO2<=4000)) or ((TDCG>=721) and (TDCG<=1920))):
                condition='Condition 2'
                execute=False
            if(((H2>=701) and (H2<1800)) or ((CH4>=401) and (CH4<1000)) or ((C2H2>=10) and (C2H2<35)) or ((C2H4>=101) and (C2H4<200)) or ((C2H6>=101) and (C2H6<150)) or ((CO>=571) and (CO<1400)) or ((CO2>=4001) and (CO2<10000)) or ((TDCG>=1921) and (TDCG<4630))):
                condition='Condition 3'
                execute=False
            elif((H2>= 1800) or (CH4>=1000) or (C2H2>=35) or (C2H4>=200) or (C2H6>=150) or (CO>=1400) or (CO2>=10000) or (TDCG>=4360)):
                condition='Condition 4'
                execute=False
        if(H2>=1000):
            fault.append(('Corona,Arching'))
        elif(CH4>=80):
            fault.append(('Sparking'))
        elif(C2H2>=70):
            fault.append(('Arching'))
        elif(C2H4>=150):
            fault.append(('Severe Overheating'))
        elif(C2H6>=35):
            fault.append(('Local Overheating'))
        elif(CO>1000):
            fault.append(('Severe Overheating'))
        elif((CO2>15000)):
            fault.append(('Severe Overheating'))
        elif((TDCG>4630)):
            fault.append(('High TDCG'))
        elif((condition!='Condition 1') and (condition!='Condition 4')):
            fault.append('Need Resampling')
        elif(execute):
            fault.append(('No fault'))
        temp_df=pd.DataFrame({
            'Sample_number':[Sample_number],
            'Text_id':[" ".join(Text_id)],
            'Sampled_date':[Sampled_date],
            'T_site':[" ".join(T_site)],
            'T_plant':[" ".join(T_plant)],
            'Sampling_point':[Sampling_point],
            'CH4(ppm)':[CH4],
            'H2(ppm)':[H2],
            'C2H2(ppm)':[C2H2],
            'C2H4(ppm)':[C2H4],
            'C2H6(ppm)':[C2H6],
            'CO(ppm)':[CO],
            'CO2(ppm)':[CO2],
            'TDCG(ppm)':[TDCG],
            'Condition':[condition],
            'Fault':[" ".join(fault)] 
        })
        result_df=result_df.append(temp_df,ignore_index=True)
result_df.to_csv('res.csv')



