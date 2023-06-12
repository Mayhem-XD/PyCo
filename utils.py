import numpy as np
import pandas as pd
from PIL import Image
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests,json,folium,os
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster

def find_addr(places):
    with open('D:/Workspace/03.DataAnalysis/04.지도시각화/data/roadapikey.txt') as f:
        road_key = f.read()
    base_url = 'https://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
    params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10'
    params2 = f"keyword={quote('')}&resultType=json"
    url = f'{base_url}?{params1}&{params2}'
    road_addr_list = []
    for plc in places:
        params2 = f"keyword={quote(plc)}&resultType=json"
        url = f'{base_url}?{params1}&{params2}'
        result = requests.get(url)
        if result.status_code == 200:
            res = json.loads(result.text[1:-1])
            road_addr_list.append(res['results']['juso'][0]['roadAddr'])
        else:
            print(result.status_code)
    return road_addr_list

def get_coord(addr):
    with open('D:/Workspace/03.DataAnalysis/04.지도시각화/data/roadapikey.txt') as f:
        road_key = f.read()
    base_url = 'https://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
    params1 = f'confmKey={road_key}&currentPage=1&countPerPage=10'
    params2 = f"keyword={quote(addr)}&resultType=json"
    url = f'{base_url}?{params1}&{params2}'
    result = requests.get(url)
    res = json.loads(result.text[1:-1])
    road_addr = res['results']['juso'][0]['roadAddr']
    lat_,lng_ = kakao_location(road_addr)

    return lat_,lng_


def kakao_location(place):
    with open('../04.지도시각화/data/kakaoapikey.txt') as f_:
        kakao_key = f_.read()
    base_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{base_url}?query={quote(place)}'
    header = {'Authorization':f'KakaoAK {kakao_key}'}
    result = requests.get(url, headers=header).json()
    lat_ = float(result['documents'][0]['y'])
    lng_ = float(result['documents'][0]['x'])
    return lat_,lng_


def genie_chart():
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    url = 'https://www.genie.co.kr/chart/top200'
    result = requests.get(url, headers=header)
    soup = BeautifulSoup(result.text,'html.parser')
    trs = soup.select('tr.list')
    lines = []
    base_url = 'https://www.genie.co.kr/chart/top200?ditc=D&rtm=Y'
    from datetime import datetime
    now = datetime.now()
    ymd = now.strftime('%Y%m%d') 
    hh = now.strftime('%H')
    for page in range(1,5):
        url = f'{base_url}&ymd={ymd}&hh={hh}&pg={page}'
        result = requests.get(url, headers=header)
        soup = BeautifulSoup(result.text,'html.parser')
        trs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
        for tr in trs:
            rank = tr.select_one('.number').get_text().split('\n')[0].strip()
            img = 'https:' + tr.select_one('.cover > img')['src']
            try:
                title = tr.select_one('.title.ellipsis').get_text().strip()
            except:
                title = tr.select_one('.title.ellipsis').get_text().split('\n')[-1].strip()
            artist = tr.select_one('.artist.ellipsis').string.strip()
            album = tr.select_one('.albumtitle.ellipsis').text.strip()
            lines.append({'rank':rank,'img':img,'title':title,'artist':artist,'album':album})
    return lines

def in_bs():
    base_url='http://book.interpark.com'
    sub_url='/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo=028'
    url = base_url + sub_url
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    lis = soup.select('.rankBestContentList > ol > li')

    lines = []
    for li in lis:
        rank_data = li.select('.rankBtn_ctrl')
        if len(rank_data) == 1:
            rank = int(rank_data[0]['class'][-1][-1])
        else:
            rank = int(rank_data[0]['class'][-1][-1] + rank_data[1]['class'][-1][-1])
        img = li.select_one('.coverImage').find('img')['src']
        href = li.select_one('.coverImage> label > a')['href']
        title = li.select_one('.itemName').get_text().strip() 
        author = li.select_one('.author').get_text().strip()
        company = li.select_one('.company').get_text().strip()
        price = li.select_one('.price > em').get_text().strip()
        lines.append({'순위':rank,'이미지':img,'제목':title,'저자':author,'출판사':company,'가격':price, 'href':base_url + href})

    return lines

def hot_places(places, app):

    road_addr_list = find_addr(places)

    with open('../04.지도시각화/data/kakaoapikey.txt') as f_:
        kakao_key = f_.read()
    # df = pd.DataFrame({'이름':list(map(lambda x:x.split()[-1],places)),'주소':road_addr_list})
    df = pd.DataFrame({'이름':places,'주소':road_addr_list})

    base_url = "https://dapi.kakao.com/v2/local/search/address.json"
    url = f'{base_url}?query={quote("")}'
    header = {'Authorization':f'KakaoAK {kakao_key}'}
    lat_list = []
    lng_list = []
    for i in df.index:
        url = f'{base_url}?query={quote(df.주소[i])}'
        result = requests.get(url, headers=header).json()
        lat_list.append(float(result['documents'][0]['y']))
        lng_list.append(float(result['documents'][0]['x']))
    df['위도'] = lat_list
    df['경도'] = lng_list

    places_map = folium.Map(location=[df.위도.mean(),df.경도.mean()],zoom_start=12)
    for i in df.index:
        folium.Marker(
        location=[df.위도[i], df.경도[i]],                     
        popup=folium.Popup(df.주소[i],max_width=200),
        tooltip=df.이름[i],
    ).add_to(places_map)
    filename = os.path.join(app.static_folder,'img/HotPlaces.html')
    places_map.save(filename)

def draw_scatter(num,mean,std,min,max,app):

    xs= np.random.normal(loc=mean,scale=std,size=num)
    ys= np.random.uniform(min,max,num)
    plt.figure()
    plt.scatter(xs,ys)
    filename = os.path.join(app.static_folder,'img/scatter.png')
    plt.savefig(filename)
    return None

def siksin_search(place):
    base_url = 'https://www.siksinhot.com/search'
    url = f'{base_url}?keywords={quote(place)}'
    result = requests.get(url)
    soup = BeautifulSoup(result.text,'html.parser')
    lis = soup.select('.localFood_list > li')
    temp_list = []
    for li in lis:
        a_tags = li.select('.cate > a')
        temp_dict = {
            'img':li.find('img')['src'],
            'title':li.select_one('.textBox > h2').get_text(),
            'score':li.select_one('.textBox > span').get_text(),
            'location':a_tags[0].get_text(),
            'menu':a_tags[1].get_text()
        }
        temp_list.append(temp_dict)
    return temp_list

# Pillow Format의 img를 읽어서 중심부의 이미지를 Pillow format으로 반환
def center_image(img):
    h,w,_ = np.array(img).shape
    diff = abs(h - w) // 2
    if w > h:
        final_img = np.array(img)[:,diff:diff+h,:]
    # portrait
    else:
        final_img = np.array(img)[diff:diff+w:]
    new_img = Image.fromarray(final_img)
    return new_img

def change_profile(app, filename):
    img = Image.open(filename)
    new_fname = os.path.join(app.static_folder,'data/profile.png')
    center_image(img).save(new_fname, format='png')
    return os.stat(new_fname).st_mtime      # 마지막으로 파일이 수정된 시각(type int)

def rtn_addr(target,df_st):
    str_addr = df_st[df_st.역명 == target].도로명주소.values[-1]
    return str_addr.strip()

def get_stnar(target):
    with open('data/sub_arr_info_key.txt') as f:
        info_key = f.read()
    df_st = pd.read_csv('data/st_addr_20230518.csv')
    target = target
    target = target[:-1] if target[-1] == '역' else target
    base_url = "http://swopenAPI.seoul.go.kr/api/subway/"
    params1 = f"{info_key}/json/realtimeStationArrival/0/16/"
    params2 = quote(target)
    url = f"{base_url}{params1}{params2}"
    response = requests.get(url)
    res = json.loads(response.text)
    df = pd.DataFrame(res['realtimeArrivalList'])
    df = df[['updnLine','trainLineNm','statnNm','bstatnNm','arvlMsg2','arvlMsg3','subwayId','arvlCd']]
    df.subwayId = df.subwayId.astype(int)
    df1 = df[df.updnLine == '상행'].head(4).copy()
    df2 = df[df.updnLine == '하행'].head(4).copy().reset_index(drop=True)

    temp1 =[]
    for i in df1.index:
        bst = df1.arvlMsg3[i].strip()
        temp1.append(kakao_location(rtn_addr(bst,df_st)))
    df_test = pd.DataFrame(temp1,columns=('lat','lng'))
    df1 = pd.concat([df1, df_test], axis=1)
    temp1 =[]
    for i in df2.index:
        bst = df2.arvlMsg3[i].strip()
        temp1.append(kakao_location(rtn_addr(bst,df_st)))
        
    df_test = pd.DataFrame(temp1,columns=('lat','lng'))
    df2 = pd.concat([df2, df_test], axis=1)
    lat,lng = kakao_location(rtn_addr(target,df_st))

    return df1, df2, lat,lng

def get_rtstnar_map(app,df1,df2,lat,lng):
    
    stn_map = folium.Map(location=[lat,lng],zoom_start=13)
    marker_cluster = MarkerCluster().add_to(stn_map)

    for i in df1.index:
        icon_image = f'data/icons/sb-{df1.subwayId[i]%1000}.png'
        if not os.path.exists(icon_image):
            icon_image = f'data/icons/sb-init.png'
        pushpin = folium.CustomIcon(icon_image=icon_image, icon_size=(40,40))
        popup_text = f"{df1.arvlMsg2[i]}<br>{df1.updnLine[i]}"
        folium.Marker(
            location=[df1.lat[i], df1.lng[i]], 
            popup=folium.Popup(popup_text,max_width=300),
            tooltip=df1.arvlMsg3[i],
            icon=pushpin
        ).add_to(marker_cluster)

    for i in df2.index:
        icon_image = f'data/icons/sb-{df2.subwayId[i]%1000}.png'
        if not os.path.exists(icon_image):
            icon_image = f'data/icons/sb-init.png'
        pushpin = folium.CustomIcon(icon_image=icon_image, icon_size=(40,40),)
        popup_text = f"{df2.arvlMsg2[i]}<br>{df2.updnLine[i]}"
        folium.Marker(
            location=[df2.lat[i], df2.lng[i]], 
            popup=folium.Popup(popup_text,max_width=300),
            tooltip=df2.arvlMsg3[i],
            icon=pushpin
        ).add_to(marker_cluster)

    title_html = '<h3 align="center" style="font-size:20px">지하철 실시간 도착정보</h3>'
    stn_map.get_root().html.add_child(folium.Element(title_html))
    filename = os.path.join(app.static_folder,'img/rtstn.html')
    stn_map.save(filename)
    # 
    return None