# Pyco

<h1>파이썬과 플라스크를 이용해서 웹 개발</h1>

<h3>프로젝트 소개</h3>

> 내용 </br>
> 추후 수정예정<br>
> MySQL DB 연동<br>
> 게시판, 댓글, api, <br>
> Ajax로 기능 수정예정 <br>
> 튜플로 받아온 xxxxx_list dict로 변경 <br>  
> oracle DB 추가 예정 <br>  
<h3>개발 과정</h3>

>   * 협업툴<br>
>   ![gicon1](https://github.com/Mayhem-XD/Project_p1/assets/116787370/395b6da2-606f-450e-8ded-f01f406e1e64) ![gd](https://github.com/Mayhem-XD/Project_p1/assets/116787370/150ffdc3-049c-47ba-b3d6-81a49b8c2b5c)<br>
>   * 기본 라우팅 테이블<br>
>   ![table](https://github.com/Mayhem-XD/Project_p1/assets/116787370/2dcdfcd6-3465-4c5e-95a0-f4922cc8c841)
>   * 개발도구<br>
>   ![python](https://github.com/Mayhem-XD/Project_p1/assets/116787370/8b7153e0-e96e-42c8-97da-dac77852ea70)
>   ![flask](https://github.com/Mayhem-XD/Project_p1/assets/116787370/ad564b8b-287a-4444-bfb5-d554668e546e)
>   ![vscode](https://github.com/Mayhem-XD/Project_p1/assets/116787370/5c1215e8-01f9-4f42-8d02-aed1e5842c24)<br>
>   * 웹 화면<br>
>   

<h3> check update page </h3>


프로젝트 코드 일부  

~~~ python

# sql 연결문
# dao, service

~~~

~~~ javascript
<script>
// timepicker를 사용하고 10분 단위,24시간 단위로 입력을 받고 시작 시간을 04:00 하기 위한 옵션을 줌
    $(document).ready(function () {
        $('input.timepicker').timepicker({
                timeFormat: 'HH:mm',
                interval: 10,
                startTime: '04:00',
                dynamic: false,
                dropdown: true,
                scrollbar: true
                });
});
</script>
~~~

~~~ javascript
    function send_val() {
        let timep = $('#timep').val();
        let stn = $('#input_stn').val();
        $.ajax({
            type: 'POST',
            url: '/index',
            data: { timep: timep, stn: stn },
            // ajax가 정상적으로 동작하면 실행되는 부분
            success: function (result) {
            $('#init_img').css('display', 'none');
            $('#show_img').css('display', 'block');
            let dn = result.dn;
            let up = result.up;
            $('#i1').attr('src', '/static/img/stage_' + dn + '.png');
            $('#i2').attr('src', '/static/img/stage_' + up + '.png');
        }
      });
    }
               
~~~

~~~ python
# 전체 데이터와 일일 데이터 두 가지의 타입의 데이터를 구분해서 전처리 시작하는 함수
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
~~~


~~~ python
# rtn_line_info(year) 함수에서 만들어진 임시파일들을 일괄제거하는 함수
def rm_temp_files():
    temp_path = os.path.join('static','data', 'temp_files', '*.csv')
    for file in glob.glob(temp_path):
        os.remove(file)
    return None
~~~

~~~ python

# 로그인

@user_bp.route('/login', methods=['GET','POST'])
def login():
    menu = {'ho':0,'nb':0,'us':1,'cr':0,'sc':0,'py':0}
    if request.method == 'GET':
        return render_template('/prototype/user/login.html',menu=menu)
    else:
        uid = request.form['uid']
        pwd = request.form['pwd']
        # userService login check
        result = us.login(uid,pwd)
        if result == us.WRONG_PASSWORD:
            flash('잘못된 pwd')
            return redirect('/user/login')
        elif result == us.UID_NOT_EXIST:
            flash('id가 존재하지 않습니다.')
            return redirect('/user/register')
        elif result == us.CORRECT_LOGIN:
            # user 정보 가져옴
            user_info = us.get_user(uid)
            flash(f'{user_info[2]}님 환영합니다.')
            # session 값 
            session['uid'] = uid
            session['uname'] = user_info[2]
            session['email'] = user_info[3]
            if user_info[6]:
                session['profile'] = user_info[6]
            session['addr'] = user_info[7]
            session['currentUserPage'] = math.ceil(us.count_users()[0]/10)
            return redirect('/')
        

~~~


<h5>참조</h5>

Link: [GoogleDriver][googledriverlink]

Link: [공공데이터포탈][datalink]


[googledriverlink]: https://google.com "Go google](https://drive.google.com/drive/folders/14KeS5I5Wr6hWilykOGmXlK5aB1wZ73js"

[datalink]: https://www.data.go.kr/
