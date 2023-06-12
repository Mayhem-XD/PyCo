import numpy as np
import pandas as pd
import os,glob
from urllib.parse import quote 
import requests,json,os
import folium
from folium.plugins import HeatMap
from datetime import datetime


# 패스 선언
main_datafile_path = 'static/data/'
temp_files_path = 'static/data/temp_files/'
main_file_name = f'{main_datafile_path}metro_ridership_by_line_stn_time.csv'
xlsx_path = 'static/data/total_stn_info_20230317.xlsx'
temp_info_name = f'{temp_files_path}temp_info.csv'
key_path = 'static/key/kakaoapikey.txt'
# sk_key_path = 'static/key/sk_open_api_key.txt'
sk_key_path = os.path.join('static', 'key', 'sk_open_api_key.txt')
heatmap_data = f'{main_datafile_path}merged_lines.csv'
stn_code_file_path = os.path.join('static', 'data', 'stn_code.csv')
main_heatmap = f'{main_datafile_path}lines_4heatmap_merged_.csv'

with open(sk_key_path) as f_:
    sk_key = f_.read()

# 파일이름 입력받아 일일 데이터인지 전체기간 시간별 데이터인지 구볋 후 각각의 양식에 맞게 처리
def stn_name_modification(name=main_file_name):
    if name == main_file_name:
        df_st = pd.read_csv(name,encoding='euc-kr')
        df_st['지하철역'] = df_st['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
        for i in df_st.index:
            if df_st.loc[i, '지하철역'][-1] == '역':
                df_st.loc[i, '지하철역'] = df_st.loc[i, '지하철역'][:-1]
        return df_st
    else:
        df_st = pd.read_csv(name,encoding='euc-kr')
        df_st.drop(columns=['등록일자'],inplace=True)
        df_st.rename(columns={'역명': '지하철역'},inplace=True)
        df_st['지하철역'] = df_st['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
        for i in df_st.index:
            if df_st.loc[i, '지하철역'][-1] == '역':
                df_st.loc[i, '지하철역'] = df_st.loc[i, '지하철역'][:-1]
        return df_st

# 전체 데이터에 특정 조건의 열로 변경
# 다음 단계에서 일반적으로 사용하는 호선으로 다듬기 위해서 여기서 각 호선별로 분리
def line_sep_preproc_main():
    # 수인분당선에서 누락되는 역명들
    si_list = '오이도 정왕 신길오천 안산 초지 고잔 중앙 한대앞'.split()
    copy_list = []
    df = stn_name_modification()
    lines = df.호선명.unique().tolist()
    df_dict = {line: df[df['호선명'] == line].copy() for line in lines}
    for line, frame in df_dict.items():
        frame['새벽 승차인원'] = frame.loc[:,['04시-05시 승차인원','05시-06시 승차인원']].sum(axis=1)
        frame['새벽 하차인원'] = frame.loc[:,['04시-05시 하차인원','05시-06시 하차인원']].sum(axis=1)

        frame['출근시간 승차인원'] = frame.loc[:,['06시-07시 승차인원','07시-08시 승차인원','08시-09시 승차인원']].sum(axis=1)
        frame['09-16시 승차인원'] = frame.loc[:,['09시-10시 승차인원','10시-11시 승차인원','11시-12시 승차인원',
                                                '12시-13시 승차인원','13시-14시 승차인원','14시-15시 승차인원','15시-16시 승차인원','16시-17시 승차인원']].sum(axis=1)
        frame['퇴근시간 승차인원'] = frame.loc[:,['17시-18시 승차인원','18시-19시 승차인원','19시-20시 승차인원']].sum(axis=1)
        frame['야간 승차인원'] = frame.loc[:,['20시-21시 승차인원','21시-22시 승차인원','22시-23시 승차인원',
                                            '23시-24시 승차인원','00시-01시 승차인원','01시-02시 승차인원']].sum(axis=1)
        frame['출근시간 하차인원'] = frame.loc[:,['06시-07시 하차인원','07시-08시 하차인원','08시-09시 하차인원']].sum(axis=1)
        frame['퇴근시간 하차인원'] = frame.loc[:,['17시-18시 하차인원','18시-19시 하차인원','19시-20시 하차인원']].sum(axis=1)
        frame['09-16시 하차인원'] = frame.loc[:,['09시-10시 하차인원','10시-11시 하차인원','11시-12시 하차인원',
                                                '12시-13시 하차인원','13시-14시 하차인원','14시-15시 하차인원','15시-16시 하차인원','16시-17시 하차인원']].sum(axis=1)
        frame['야간 하차인원'] = frame.loc[:,['20시-21시 하차인원','21시-22시 하차인원','22시-23시 하차인원',
                                            '23시-24시 하차인원','00시-01시 하차인원','01시-02시 하차인원']].sum(axis=1)
        frame['총 승차인원'] = frame.loc[:,['새벽 승차인원','출근시간 승차인원','09-16시 승차인원','퇴근시간 승차인원','야간 승차인원']].sum(axis=1)
        frame['총 하차인원'] = frame.loc[:,['새벽 하차인원','출근시간 하차인원','09-16시 하차인원','퇴근시간 하차인원','야간 하차인원']].sum(axis=1)
        frame = frame[['사용월', '호선명', '지하철역', '출근시간 승차인원', '출근시간 하차인원', 
                        '09-16시 승차인원', '09-16시 하차인원', '퇴근시간 승차인원', '퇴근시간 하차인원',
                        '새벽 승차인원','새벽 하차인원','야간 승차인원', '야간 하차인원','총 승차인원','총 하차인원']]
        # 2호선 신천역이 잠실새내역으로 바뀌고 새로운 신천역 생겨서 예전 자료에서의 2호선 신천역 잠실새내 역으로 변경
        frame.loc[(frame['호선명'] == '2호선') & (frame['지하철역'] == '신천'), '지하철역'] = '잠실새내'
        # 수인분당선에서 누락된 안산선의 역들 따로 추출
        frame_copy = frame[(frame['호선명']=='안산선')&(frame['지하철역'].isin(si_list))].copy()
        frame_copy['호선명'] = frame_copy['호선명'].apply(lambda x: '수인선_누락')
        frame_copy = frame_copy.reset_index(drop=True)
        copy_list.append(frame_copy)
        frame.to_csv(f'{temp_files_path}{line}.csv',index=False,encoding='utf-8')
    pd.concat(copy_list).to_csv(f'{temp_files_path}수인선_누락.csv',index=False,encoding='utf-8')
    return None

# 미리 정해둔 양식으로 호선을 분리
# 2019 이후 자료에는 9호선 2단계가 없어서 따로 처리
def rtn_line_info(year):
    path = temp_files_path
    line_info = [
        ([f'{path}1호선.csv', f'{path}경부선.csv', f'{path}경원선.csv', f'{path}경인선.csv', f'{path}장항선.csv'], '1호선'),
        ([f'{path}2호선.csv'], '2호선'),
        ([f'{path}3호선.csv', f'{path}일산선.csv'], '3호선'),
        ([f'{path}4호선.csv', f'{path}과천선.csv', f'{path}안산선.csv'], '4호선'),
        ([f'{path}5호선.csv'], '5호선'),
        ([f'{path}6호선.csv'], '6호선'),
        ([f'{path}7호선.csv'], '7호선'),
        ([f'{path}8호선.csv'], '8호선'),
        ([f'{path}경춘선.csv'], '경춘선'),
        ([f'{path}수인선.csv',f'{path}수인선_누락.csv', f'{path}분당선.csv'], '수인분당선'),
        ([f'{path}경의선.csv', f'{path}중앙선.csv'], '경의중앙선'),
        ([f'{path}공항철도 1호선.csv'], '공항철도')
    ]
    # 19년도 이후 자료에는 9호선 2단계가 없음
    if year >= 2019:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    else:
        line_info.append(([f'{path}9호선.csv', f'{path}9호선2단계.csv', f'{path}9호선2~3단계.csv'], '9호선'))
    return line_info


# rtn_line_info(year) 함수에서 만들어진 파일들을 제거하는 함수
def rm_temp_files():
    temp_path = os.path.join('static','data', 'temp_files', '*.csv')
    for file in glob.glob(temp_path):
        os.remove(file)
    return None

# 임시로 만들어진 info 파일을 제거하는 함수
def rm_temp_info_files(year,ck_week):
    file = os.path.join('static','data',  f'{year}_{ck_week}_sub_info.csv')
    os.remove(file)
    return None

# 호선 전처리 함수
# rtn_line_info() 함수에서 불러온 line_info를 이용
# 호선명은 불러온 line_info에 있는 line_name 으로 사용
def preprocessing_lines(year=2019):
    line_list = []
    line_info = rtn_line_info(year)
    # df_copies에는 df_list에 있는 csv파일들을 불러와서 데이터프레임으로 만들고 append함
    for df_list, line_name in line_info:
        df_copies = []
        for file in df_list:
            df = pd.read_csv(file)
            df_copies.append(df.copy())
        # 모두 불러왔으면 concat 함수로 하나의 데이터프레임으로 만들고 인덱스 정리
        result = pd.concat(df_copies, axis=0)
        result = result.reset_index(drop=True)
        result.호선명 = line_name
        cols = list(result.columns)[:3]
        target = list(result.columns)[3:]
        # 그 후 groupby로 중복된 역들의 데이터 합산 ex) 1호선 서울역, 경부선 서울역
        res = result.groupby(cols)[target].agg('sum').reset_index()
        line_list.append(res)
    final = pd.concat(line_list,axis=0)
    rm_temp_files()
    return final

# 메인 데이터파일 전처리 함수
# 함수 호출시 merged_lines.csv 파일 생성
def preproc_main():
    line_sep_preproc_main()
    final = preprocessing_lines()
    final.to_csv(f'{main_datafile_path}merged_lines.csv',index=False)
    return None

# 각 년도 일일 데이터 전처리 함수
# 연도와 주중/주말 입력받아 실행
# 각 년도의 일일 데이터를 월별 데이터로 변환
def stn_sub_modification(year,ck_week):
    name = f'{main_datafile_path}{year}.csv'
    
    df1 = stn_name_modification(name)
    cols = list(df1.columns)[:3]
    target = list(df1.columns)[3:]
    df1['사용일자'] = pd.to_datetime(df1['사용일자'], format='%Y%m%d')
    # 평일과 주말 구분하는 새로운 열 생성
    df1['주중/주말'] = df1['사용일자'].apply(lambda x: '주말' if x.weekday() >= 5 else '주중')
    # 주중/주말 선택
    rtn_week = '주중' if ck_week == '주중' else '주말'
    weekday_df = df1[df1['주중/주말'] == rtn_week]
    week_df = weekday_df.copy()
    week_df['사용일자'] = pd.to_datetime(weekday_df['사용일자']).dt.strftime('%Y%m%d').astype(int)
    df_list = []
    for i in range(1, 13):
        start_date = year*10000 + i*100
        end_date = start_date + 100
        df_temp = week_df[(week_df['사용일자'] >= start_date) & (week_df['사용일자'] < end_date)].copy()
        df_temp['사용일자'] = year*100 + i
        df_temp = df_temp.groupby(cols)[target].agg('sum').reset_index()
        df_list.append(df_temp)
    df_res = pd.concat(df_list, axis=0)
    df_res.to_csv(f'{main_datafile_path}{year}_{ck_week}_sub_info.csv', index=False)
    return None

# 일일 데이터 가공
# preproc_main과 크게 다르지는 않음
def preproc_sub(year,ck_week):
    
    stn_sub_modification(year,ck_week)
    df = pd.read_csv(f'{main_datafile_path}{year}_{ck_week}_sub_info.csv')
    df = df.rename(columns={'역명': '지하철역', '노선명':'호선명', '사용일자':'사용월'})
    
    lines = df.호선명.unique().tolist()
    df_dict = {line: df[df['호선명'] == line].copy() for line in lines}
    copy_list = []
    si_list = '오이도 정왕 신길오천 안산 초지 고잔 중앙 한대앞'.split()
    for line, frame in df_dict.items():
        frame.loc[(frame['호선명'] == '2호선') & (frame['지하철역'] == '신천'), '지하철역'] = '잠실새내'
        
        frame_copy = frame[(frame['호선명']=='안산선')&(frame['지하철역'].isin(si_list))].copy()
        frame_copy['호선명'] = frame_copy['호선명'].apply(lambda x: '수인선_누락')
        frame_copy = frame_copy.reset_index(drop=True)
        copy_list.append(frame_copy)
        frame.to_csv(f'{temp_files_path}{line}.csv',index=False,encoding='utf-8')
    pd.concat(copy_list).to_csv(f'{temp_files_path}수인선_누락.csv',index=False,encoding='utf-8')

    final = preprocessing_lines(year)
    rm_temp_files()
    rm_temp_info_files(year,ck_week)
    final.to_csv(f'{main_datafile_path}{year}_{ck_week}_merged_lines.csv',index=False)
    return None

# kakao local API로 좌표를 구하는 함수
def kakao_location(place):
    with open({key_path}) as f_:
        kakao_key = f_.read()
    base_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{base_url}?query={quote(place)}'
    header = {'Authorization':f'KakaoAK {kakao_key}'}
    result = requests.get(url, headers=header).json()
    lat_ = float(result['documents'][0]['y'])
    lng_ = float(result['documents'][0]['x'])
    return lat_,lng_

# 데이터 프레임에서 역명을 입력받아 도로명주소를 반환하는 함수
def rtn_addr(df,target):
    str_addr = df[df.지하철역 == target].도로명주소.values[-1]
    return str_addr.strip()

# 전체 역사 데이터에서 사용할 부분만 추출
# 그 역사들의 위경도를 구해서 추가
# 오타/오기 등으로 잘못 된 역사 주소 수정
def get_stn_lat_lng():
    df = pd.read_excel(xlsx_path,engine='openpyxl')
    df.to_csv(temp_info_name,index=False)
    df = pd.read_csv(temp_info_name)
    df = df[['역사명','역사도로명주소','운영기관명']]
    df.rename(columns={'역사명':'지하철역','역사도로명주소':'도로명주소'},inplace=True)
    exclude_list = ['대전교통공사', '대구도시철도공사', '부산광역시 부산교통공사', '부산-김해경전철㈜','광주광역시 도시철도공사']
    for exclude in exclude_list:
        df = df[df['운영기관명'] != exclude]
    df.drop(columns=['운영기관명'],inplace=True)
    df['지하철역'] = df['지하철역'].str.replace('(', ' ',regex=False,).str.split().str[0]
    for i in df.index:
        if df['지하철역'][i][-1] == '역':
            df['지하철역'][i] = df['지하철역'][i][:-1]
    df.drop_duplicates(subset=['지하철역'],keep='first',inplace=True)
    df = df[~df['도로명주소'].str.contains('부산|울산')]
    df.reset_index(drop=True,inplace=True)
    
    temp1 =[]
    for i in df.index:
        try:
            target = df['지하철역'][i].strip()
            temp1.append(kakao_location(rtn_addr(df,target)))
        except:
            print(i, df.지하철역[i])
            
    df_test = pd.DataFrame(temp1,columns=('lat','lng'))
    df2 = pd.concat([df, df_test], axis=1)
    df2.to_csv(f'{main_datafile_path}stn_r_addr_final.csv',index=False)
    return None

# 히트맵을 사용하기 위해 get_stn_lat_lng()에서 구한 역사별 위경도 자료와 merge함
def add_lat_lng(name=heatmap_data):
    df_latlng = pd.read_csv(f'{main_datafile_path}stn_r_addr_final.csv')
    df_latlng.drop(columns=['도로명주소'], inplace=True)

    df_main = pd.read_csv(name)
    res = pd.merge(df_main, df_latlng, on='지하철역', how='left')
    res.to_csv(f'{main_datafile_path}lines_4heatmap_{name[5:12]}.csv', index=False)
    return None
# sk_open_api를 사용하기 위해 역명 고유코드들을 구하는 함수
def create_stn_code():
    url = "https://apis.openapi.sk.com/puzzle/subway/meta/stations?type=train"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": sk_key
    }
    response = requests.get(url, headers=headers).json()
    re = response['contents']
    df = pd.DataFrame(re)
    df.to_csv(f'{main_datafile_path}stn_code.csv',index=False)
    return None
# 역명을 입력하면 고유코드를 반환하는 함수
def get_stn_code(station):
    df_read = pd.read_csv(f'{main_datafile_path}stn_code.csv')
    stn = station  # 입력할 역
    stn_code = df_read[df_read['stationName'] == stn]['stationCode'].values[0]
    return stn_code
# 역명, 요일, 시간, 분(10분단위)를 입력하면 입력한 시간에 해당되는 상하행별 최대 혼잡도 반환
def get_cong(station,hh,mm):
    # 고유코드들을 구한 csv파일이 없으면 고유코드들을 구하는 함수 실행
    if not os.path.exists(stn_code_file_path):
        create_stn_code()
    station_code = get_stn_code(station)
    weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    today = datetime.today().weekday()
    dow = weekdays[today]
    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/train/stations/{station_code}?dow={dow}&hh={hh}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "appkey": sk_key
    }

    response = requests.get(url, headers=headers).json()
    # data1에는 상행선들의 데이터
    # data2에는 하행선들의 데이터
    data1 = [pd.DataFrame(stat['data']) for stat in response['contents']['stat'] if stat['updnLine'] == 1]
    data2 = [pd.DataFrame(stat['data']) for stat in response['contents']['stat'] if stat['updnLine'] == 0]
    # 리스트에 저장된 데이터프레임들을 하나로 만듬
    df = pd.concat(data1)
    df['updn'] = 1
    df_ = pd.concat(data2)
    df_['updn'] = 0
    # 합쳐진 상하행선 데이터들을 합침
    df = pd.concat((df,df_))
    # 특수한 사유로 혼잡도 0을 갖는 데이터들이 있는데 이 데이터들은 포함하지 않음
    df_res = df[df['congestionTrain'] != 0].copy()
    # 그 시간대에서 원하는 분(10분단위)를 고름
    df_res = df_res[df_res['mm'] == mm].copy()
    # 필요없는 부분을 제거하고 그룹바이
    df_res.drop(columns=['dow','hh','mm'],inplace=True)
    df_res = df.groupby('updn')['congestionTrain'].agg('max').reset_index().round(2)
    return df_res.values

def show_heatmap(app,line,target,smonth,emonth,heatmap_name=main_heatmap):
    df = pd.read_csv(heatmap_name)
    df_test = df[(df.호선명 == line)&(df.사용월 >= smonth)&(df.사용월 < emonth)].copy()
    df_test.drop(columns=['호선명','사용월'],inplace=True)
    df_test = df_test[['지하철역','lat','lng',target]]
    df_test.groupby(['지하철역'])[['lat','lng',target]].agg('mean').reset_index()
    # 처음 보여 줄 곳은 데이터프레임에 있는 역들의 위경도 평균치
    mean_lat = df_test['lat'].mean()
    mean_lng = df_test['lng'].mean()
    df_test.drop(columns=['지하철역'],inplace=True)
    m = folium.Map(location=[mean_lat, mean_lng], zoom_start=10)
    data = df_test
    HeatMap(data).add_to(m)
    title_html = f'<h3 align="center" style="font-size:20px">{line} {smonth} - {emonth} 기간 {target}</h3>'
    m.get_root().html.add_child(folium.Element(title_html))
    heatmap = os.path.join(app.static_folder,'img/heatmap.html')
    m.save(heatmap)
    return '../static/img/heatmap.html'
    
def show_tour_map(app,station_name,cat):
    tour = pd.read_csv(f'{main_datafile_path}수도권.csv')
    stn = pd.read_csv(f'{main_datafile_path}stn_r_addr_final.csv')
    df = tour[tour.분류 == cat]
    lat = stn[stn.지하철역 == station_name].lat.iloc[0]
    lng = stn[stn.지하철역 == station_name].lng.iloc[0]
    print(tour.shape, df.shape)

    m = folium.Map(location=[lat, lng],zoom_start=15, width='100%', height='100%')
    for i in df.index:
        logo = folium.CustomIcon(f'{main_datafile_path}/icons/{df.분류[i]}.png', icon_size=(30,30))
        folium.Marker(
            location=[df.lat[i],df.lng[i]],
            popup=folium.Popup(df.도로명주소[i], max_width=200),
            tooltip=df.관광지명[i],
            icon=logo
        ).add_to(m)

    folium.Circle(
        location=[lat,lng],
        tooltip=station_name,
        radius=500,
        color="#ff7800",
        fill_color='#ffff00',
        fill_opacity=0.1
    ).add_to(m)
    show_map = os.path.join(app.static_folder,'img/station.html')
    m.save(show_map)

    return '../static/img/station.html'

def show_cong(timep, target):
    hh, mm = timep.split(":")
    cong = get_cong(station=target, hh=hh, mm=mm)
    dn = int(cong[0][1])
    up = int(cong[1][1])
    dn_img = 'a' if dn < 20 else 'b' if dn < 40 else 'c' if dn < 80 else 'd' if dn < 140 else 'e'
    up_img = 'a' if up < 20 else 'b' if up < 40 else 'c' if up < 80 else 'd' if up < 140 else 'e'
    return dn_img,up_img
    # return target

# 0-20 20-40 40-80 80-140 140-