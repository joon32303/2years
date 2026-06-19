import streamlit as st
import time
from PIL import Image, ImageOps  # 👈 이미지 회전 방지를 위해 이 줄을 꼭 추가해 주세요!
# ==========================================
# ⚙️ 1. 페이지 기본 설정 및 상태 관리
# ==========================================
st.set_page_config(page_title="2주년 편지함", page_icon="💌", layout="centered")

if "stage" not in st.session_state:
    st.session_state.stage = 0
# 💡 숫자 1 대신, 편지 화면 번호인 'len(stages) + 1'로 강제 세팅!
#if "stage" not in st.session_state:
#    st.session_state.stage = 24
# ==========================================
# 📝 2. 추억 퀴즈 데이터 (여기서 정답을 수정하세요!)
# ==========================================
# 사진 파일들은 반드시 이 파이썬 파일과 같은 폴더에 photo1.jpg, photo2.jpg... 이름으로 넣어주세요.
stages = [
    {
        "success": "",
        "desc": "젊다 젊어… 처음 문제니깐 쉬운거",
        "img": "photo1.jpg",
        "q": "과연 이때 형준 서연은 몇살일까요?",
        "type": "text",
        "ans": "2321",  # 💡 수정 필요: 띄어쓰기 없이 '2321'로 적을 경우 "2321"로 설정
        "hint": ""
    },
    {
        "desc": "팔찌 색깔 진한거 보소.. 서연이는 이미 이거 잃어버린거 같지만…",
        "img": "photo2.jpg",
        "q": "과연 몇일 기념으로 팔찌를 맞췄을까아아아요?",
        "type": "text",
        "ans": "22", # 💡 수정 필요 (예: 11, 22 등 숫자만)
        "hint": "11,22,33,44,55,66,77,88"
    },
    {
        "desc": "와.. 이때 공연 재밌다가 마지막에 아줌마들 난동 때문에… 핸드폰 케이스도 녹색인거 보소~ 진짜 똥띠박…",
        "img": "photo3.jpg",
        "q": "그렇다면…. 이때 우리가 시킨 음식은?",
        "type": "radio",
        "options": ["선택하세요", "1. 치킨", "2. 나쵸", "3. 피자", "4. 오징어"],
        "ans": "2. 나쵸", # 💡 정답 번호를 options에 적힌 글자와 완전히 똑같이 맞춰주세요.
        "hint": ""
    },
    {
        "desc": "이주 유명한 데이트 코스.. 아쿠아리움! 생각보다 너무 짧게 끝나서… 근데 뭘 그렇게 귀엽게 구경하는거얌..? 귀여워서 넣어봐똥..",
        "img": "photo4.jpg",
        "q": "이날 간 아쿠아리움은?",
        "type": "radio",
        "options": ["선택하세요", "1. 코엑스", "2. 롯데월드", "3. 아쿠아플라넷", "4. 씨라이프부산"],
        "ans": "1. 코엑스" 
    },
# 5번째 문제 (photo5 사진이 보이고, 정답을 맞추면 다음으로 넘어감)
    {
        "desc": "뿅 이븐거 보소~", # 👈 photo5 사진 위에 뜨는 설명글!
        "img": "photo5.jpg",
        "q": "이 사진에서 가장 예쁜 부분은 어디일까요?", # 💡 혹시 5번 문제 질문이 따로 있다면 여기를 수정하세요!
        "type": "text",
        "ans": "다", # 💡 5번 문제의 진짜 정답을 적어주세요.
        "hint": "da"
    },
    
    # 6번째 문제 (5번을 맞추고 넘어오면 photo6 사진과 함께 퀴즈 시작!)
    {
        "desc": "", 
        "img": "photo6.jpg", 
        "q": "왜 이리 신났을까요?", # 👈 photo6 사진 밑에 뜨는 질문!
        "type": "radio",
        "options": ["선택하세요", "1. 밥먹을 시간 돼서", "2. 서연이랑 같이 있어서", "3. 잘시간 돼서", "4. 날씨가 좋아서"],
        "ans": "2. 서연이랑 같이 있어서",
        "hint": " 이 문제에 사진이 없으면... 내가 코딩을 하면서 문제를 못찾았어.. 사진으로 보여줄겡!"
    },
    {
        "desc": "내가 좋아하는 사진 중 하나… 이쁜거 보소…. 이날 진짜 좋았는데..",
        "img": "photo7.jpg",
        "q": "이날 먹는 음식을 모두 고르시오.",
        "type": "text",
        "ans": "치킨 만두",
        "hint": "치킨?만두?피자?나쵸?오징어?(답을 작성할때는 힌트로 주어진 음식 순서대로)"
    },
{
        "desc": "눈부시다… 앙! 이때도 진짜 재밌었던 하루…",
        "img": "photo8.jpg",
        "q": "여기는 과연 어디일까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 금강", "2. 압록강", "3. 한강", "4. 낙동강"],
        "ans": "3. 한강",
        "success": "정답! 하트 뿅~❤️",
        "success_img": "photo9.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {

        "desc": "이사진이ㅋㅋㅋ 다시보면 진짜 웃겨 누가 누가 목 길게 하냐인데 서연이 입 보면 조금이라도 더 길게 하려구 입 삐죽 내민거 봐ㅋㅋㅋ 귀여워 이제 문제!",
        "img": "photo10.jpg",
        "q": "누가 더 목이 길까요?",
        "type": "text",
        "ans": "이서연",
        "hint": "이서연.. 흥"
    },
    {
        "desc": "이날 서연이 기차의 재미를 알아버린 날… 턱살 보오오소~ 이날 밤 새고 와서 힘들어 했잖아… ㅠㅠ 이날 게임도 하고 재밌게 놀았지?",
        "img": "photo11.jpg",
        "q": "그렇다면 이날 우리를 데려다 준 외국인 아저씨 이름은?",
        "type": "radio",
        "options": ["선택하세요", "1. 도", "2. 레", "3. 미", "4. 파"],
        "ans": "1. 도"
    },
    {
        "desc": "여기도 진짜 내가 좋아했던 마라탕 집인네… 음료수가 공짜였나? 아무튼… 여기 또 가고 싶어…",
        "img": "photo12.jpg",
        "q": "여기 식당 이름은?",
        "type": "text",
        "ans": "마라정도",
        "hint": "창문을 보시오!",
        "success": "정답! 오~~~하트 뿅~❤️쪽!",
        "success_img": "photo13.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {
        "desc": "ㅋㅋㅋㅋㅋㅋ 이중 누가 서연이고 누가 나일까요?ㅋㅋㅋㅋ 이때 진짜 웃겼엉…",
        "img": "photo14.jpg",
        "q": "정답을 순서대로 적어주세요 (예: 서준 형연)",
        "type": "text",
        "ans": "서연 형준", # 💡 사진에 맞게 답을 적어주세요
        "hint": "",
        "success_img": "photo15.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {

        "desc": "이건 영상으로 봐야 더 귀야운데.. 전날 또 잠 잘 안자고 왔다고 버스에서 정신없이 잤잖아..",
        "img": "photo16.jpg",
        "q": "어디를 가고 있는걸까아아아요?",
        "type": "radio",
        "options": ["선택하세요", "1. 평택", "2. 부여", "3. 공주", "4. 속초"],
        "ans": "4. 속초",
        "success": "정답! 신난거 보오오오소오오오오!",
        "success_img": "photo17.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {
        "desc": "난 이때부터 젠몬에 빠졌었지.. 아직도 못샀지만….",
        "img": "photo18.jpg",
        "q": "여기 젠몬 매장은?",
        "type": "radio",
        "options": ["선택하세요", "1. 명동", "2. 성수", "3. 잠실", "4. 의정부"],
        "ans": "3. 잠실",
        "success": "정답! 훗",
        "success_img": "photo19.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {
        "desc": "치즈 범벅인거 보소… 와… 너무 맛있겠다…",
        "img": "photo20.jpg",
        "q": "여기는 어디일까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 서울랜드", "2. 애버랜드", "3. 경주월드", "4. 롯데월드"],
        "ans": "4. 롯데월드",
        "success": "정답!다리꼬고 훗2",
        "success_img": "photo21.jpg"  # 👈 정답 시 띄우고 싶은 축하 사진/GIF 파일명 입력!
    },
    {

        "desc": "",
        "img": "photo22.jpg",
        "q": "누가 더 입술이 길까요~?",
        "type": "text",
        "ans": "이서연",
        "hint": "이서연…흥2, 여기도 사진이 없을수도... 뭐가 이상해... 코딩이랑 파일은 문제 없는데.... ㅠㅠ"
    },
    {
        "desc": "고오오급 스키복 대여에 고급 헬멧쓰고 재밌게 스키장! 나중에 또 타러가자!",
        "img": "photo23.jpg",
        "q": "이때 어디 스키장일까요~~",
        "type": "radio",
        "options": ["선택하세요", "1. 비발디", "2. 평창", "3. 무주", "4. 휘닉스"],
        "ans": "1. 비발디",
        "hint": "헬멧을 자세히 관찰해보세용",
        "success": "이날 먹은 하이디라오...",
        "success_img": "photo24.jpg"
    },
    {
        "desc": "이날 진짜 너무 재밌었어.. 우리 다시 한번 또 가자!근데 누가... 입술!! 누가....",
        "img": "photo25.jpg",
        "q": "이때 왔던 게스트는?",
        "type": "radio",
        "options": ["선택하세요", "1. 지드래곤", "2. 비비", "3. 다듀", "4. 성시경"],
        "ans": "3. 다듀",
        "success": "사람 많은거 보소~ 이빨 미뇨다....",
        "success_img": "photo26.jpg"
    },
    {
        "desc": "머리 정갈한거 보소 ㅋㅋㅋ 귀여워..",
        "img": "photo27.jpg",
        "q": "이날 본 연애인은 누굴까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 벤츠", "2. 벤틀리", "3. 람보르기니", "4. 아우디"],
        "ans": "2. 벤틀리",
        "success": "정답! 훗3",
        "success_img": "photo28.jpg"
    },
    {
        "desc": "광기의 산타…어디가 머리거 어디가 수염이지? 하지만 맛있었다!",
        "img": "photo29.jpg",
        "q": "이날은 무슨 날일까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 크리스마스", "2. 크리스에반스", "3. 크리스헴스워스", "4. 크리스 토퍼놀란"],
        "ans": "1. 크리스마스",
        "success": "다 내꺼어어어어어ㅓ!!!!",
        "success_img": "photo30.jpg"
    },
    {
        "desc": "단아한거 보소… 이쁘다… 저게 혹시 내 잃어버린 장갑…?",
        "img": "photo31.jpg",
        "q": "여기는 어디일까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 첨성대", "2. 동궁과 월지", "3. 대릉원", "4. 천마총"],
        "ans": "2. 동궁과 월지"
    },
    {
        "desc": "",
        "img": "photo32.jpg",
        "q": "뿅! 여기는 공주~? 시일까 님일까?",
        "type": "radio",
        "options": ["선택하세요", "1. 시", "2. 님"],
        "ans": "2. 님",
        "success": "막이러시구~~",
        "success_img": "photo33.jpg",
        "success": "귀여미... 내꼬"
    },
    {
        "desc": "ㅋㅋㅋ 머리 짧은거봐… 훈련소를 다녀와 버렸다….",
        "img": "photo34.jpg",
        "q": "난 몇일에 훈련소을 갔을까요?",
        "type": "radio",
        "options": ["선택하세요", "1. 2.19", "2. 12.34", "3. 24.38", "4. 600000.60000000000"],
        "ans": "1. 2.19"
    },
    {
        "desc": "마지막 단계...",
        "img": "photo32.jpg",
        "q": "총 우리가 만난 날은?(사귀기 시작한 날부터 오늘까지)",
        "type": "text",
        "ans": "733", # 💡 실제 만난 날짜 숫자로 수정
        "hint": "진짜 혼나.... 누가.... 혼난다...",
        "success": "끄으으읕!"
    },

    {
        "desc": """✨ 2주년 편지 ✨
        
사실 끝으으으읕은 뻥… 이번 아이디어는 어땠어..? 웹사이트 만드는 공부 잠깐 했었는데 그걸로 편지를 써보자 라는 생각이 딱 들었어… 괜찮았어? ㅠㅠ 별로지…. 

원래는 방탈출 느낌으로 편지로 참여형 페이지로 만들어서 비밀번호 찾고 힌트 얻어서 다음 사진이나 편지로 넘어가려고 했었는데.. 어느정도 구상 했지만 방탈출 싫어한다고 해서… 포기했어… 

이걸 준비하면서 지금까지 찍었던 사진들을 전부 봤엉.. 우리 진짜 이것저것 많이 해 봤더라.. 기념일도 재밌게 챙겼고.. 시험기간마다 법도 데이트 하고.. 고급진 식당도 가보고… 한강 데이트.. 놀이공원 데이트.. 집콕 데이트.. 똥디박… 

우리 처음 사진 봤어? 난 23.. 서연이는 21… 완전 어렸지.. 이젠 서연이가 23살이라니… 어떠신가?? 드디어 내 나이를 서연이가 넘어섰다….ㅠㅠ 나는 21살때랑 23살때 느끼는 감정, 사고 방식이 엄청 변했는데 서연이는 어떨라나…? 내가 느끼기에는 서연이는 21살때도 성숙했던거 같아.. 23살이었던 그때의 나랑 지금의 나는 서연이가 변하지 않은거 같다고 느껴.. 

그리고 진짜로 21살때도 지금도 서연이 사진을 보는데 정말 서연이는 항상 내 이상형이었어.. 사진 보면서 계속 그런 생각이 들었어! 어쩜 그렇게 이쁘고 귀여워…. 완전 내 이상형……. 진짜로…  

앞으로도 내 이상형인 서연이랑 맛있는곳 좋은곳 많이 다닐 수 있다는 생각에.. 벌써 기대돼!! 

좀 걱정되는것도 있어… 우리 상황이 좀 많이 변했잖아.. 나는 안산에서 2년간 근무하고.. 서연이는 이제 4학년이라 바쁘고.. 내년에는 또 취직도 하겠지? 서로 이해하지 못하는 상황도 많이 생길거 같아서 좀 걱정돼.. 그래도 서로 이해해주면서 아껴주자… 많이 노력할게! 

사실 아직 구현 아이디어만 세우고 있어서 내가 계획한 웹페이지로 구현이 될지는 모르겠지만 최선을 다 해볼게.. 조금 이상하고 어설퍼도 이해해줘.. 이쪽 분야는 전전인 나로서 완전 새로운 도전이라….. 

2주년 준비한건 여기까지야.. 오늘 하루 행복한 하루였으면 좋겠다.. 성공적인 데이트를 보내고 서로 더 가까워진 하루가 되길…. 사랑해 서연아❤️""",
        
        "img": "photo35.jpg",  # 💡 마지막 하이라이트 사진 이름 (없으면 "" 로 비워두세요!)
        "q": "편지 다 읽었어? 어땠어?? ❤️",
        "type": "radio",
        "options": ["선택하세요", "1. 사랑해...! 똥띠박 감동..", "2. 뭐하묘?"],
        "ans": "1. 사랑해...! 똥띠박 감동..",
        "hint": "힌트 보는게 대박..인거지..... 흥",
        "success": "앞으로도 예쁜 사랑 하자! 우리의 2주년을 축하해 🥂❤️"
    }
    ,
    {
        "desc": "진짜 끝",
        "img": "",
        "q": "끝",
        "type": "text",
        "ans": "끝", # 💡 실제 만난 날짜 숫자로 수정
        "hint": "끝",
        "success": "끄으으읕!"
    }

]

# ==========================================
# 🚪 3. 로그인 화면 (Stage 0)
# ==========================================
if st.session_state.stage == 0:
    st.title("🔒 웹페이지 비밀번호 입력")
    st.write("비밀번호 입력시 볼수있음")
    
    PASSWORD = st.secrets["MY_PASSWORD"]
    
    with st.expander("💡 비밀번호 힌트"):
        st.write("사귀기 시작한 날짜 8자리 비밀번호")
    
        
    pwd = st.text_input("비밀번호", type="password")
    
    if st.button("입장하기 🔑"):
        if pwd == PASSWORD:
            st.success("로그인 성공! 추억 여행을 시작합니다...")
            time.sleep(1)
            st.session_state.stage = 1
            st.rerun()
        else:
            st.error("비밀번호가 틀렸어! 혼난다 진짜로... 🥺")

# ==========================================
# 🧩 4. 퀴즈 진행 화면 (Stage 1 ~ 22)
# ==========================================
elif 1 <= st.session_state.stage <= len(stages):
    # 현재 단계의 문제 데이터 가져오기
    current_q = stages[st.session_state.stage - 1]
    
    st.title(f"📸 {st.session_state.stage}번째 추억")
    st.write("---")
    
    # 이전 문제 맞췄을 때 나오는 리액션 텍스트 (안전하게 수정)
    #if current_q.get("success"):
    #    st.success(current_q["success"])
        
    # 사진 위에 들어갈 텍스트
    if current_q["desc"]:
        st.write(current_q["desc"])
        
    # [수정된 사진 띄우기 구역] 사진 파일이 있으면 회전 정보를 바로잡고 화면에 출력합니다.
        try:
            # 사진을 그냥 읽지 않고, 회전 각도(EXIF)를 계산해서 똑바로 세운 뒤 가져옵니다.
            img_file = Image.open(current_q["img"])
            corrected_img = ImageOps.exif_transpose(img_file)
            
            st.image(corrected_img, use_container_width=True)
        except Exception as e:
            st.info(f"👉 폴더에 '{current_q['img']}' 파일이 필요합니다!")
        
    # 문제 질문 텍스트
    st.markdown(f"**{current_q['q']}**")
    
    # 힌트가 있으면 열어주기
    if "hint" in current_q and current_q["hint"]:
        with st.expander("💡 힌트 보기"):
            st.write(current_q["hint"])
            
    # 정답 입력창 (주관식 vs 객관식)
    ans_input = None
    if current_q["type"] == "text":
        ans_input = st.text_input("정답 입력", key=f"ans_{st.session_state.stage}")
    else:
        ans_input = st.radio("정답 선택", current_q["options"], key=f"ans_{st.session_state.stage}")
        
# ------------------ [여기서부터 통째로 덮어씌우세요] ------------------
    # session_state에 정답 맞춤 여부 기록용 변수 초기화
    if f"solved_{st.session_state.stage}" not in st.session_state:
        st.session_state[f"solved_{st.session_state.stage}"] = False

    # 아직 정답을 맞추기 전일 때만 [정답 확인] 버튼을 보여줌
    if not st.session_state[f"solved_{st.session_state.stage}"]:
        if st.button("정답 확인 🔑"):
            is_correct = False
            
            # 주관식 정답 체크
            if current_q["type"] == "text":
                user_ans = ans_input.replace(" ", "")
                correct_ans = current_q["ans"].replace(" ", "")
                if user_ans == correct_ans and ans_input != "":
                    is_correct = True
            
            # 객관식(라디오) 정답 체크
            elif current_q["type"] == "radio":
                if ans_input == current_q["ans"]:
                    is_correct = True
                elif ans_input != "선택하세요":
                    st.error("앗 틀렸어! 다시 골라봐! 🥺")
            
            # 멀티셀렉트 정답 체크
            elif current_q["type"] == "multiselect":
                if sorted(ans_input) == sorted(current_q["ans"]):
                    is_correct = True
                elif len(ans_input) > 0:
                    st.error("앗, 빠뜨린 게 있거나 틀린 게 있어! 다시 잘 생각해봐! 🔍")
            
            # 정답일 때 처리
            if is_correct:
                st.session_state[f"solved_{st.session_state.stage}"] = True
                st.rerun()
            elif current_q["type"] == "text": # 주관식 오답일 때만 에러창
                st.error("땡! 다시 생각해봐! 🥺")

    # 🎉 정답을 맞춘 상태일 때 나오는 특별 리액션 화면!
    else:
        # 1. 초록색 정답 문구 출력
        if current_q.get("success"):
            st.success(current_q["success"])
        else:
            st.success("🎉 정답이야! 대단한데?")
        
        # 2. 💡 형준님이 원한 [정답 축하 사진] 출력!
        if current_q.get("success_img"):
            try:
                succ_img = Image.open(current_q["success_img"])
                succ_img_corrected = ImageOps.exif_transpose(succ_img)
                st.image(succ_img_corrected, caption="우리의 예쁜 추억 ✨", use_container_width=True)
            except:
                pass # 지정한 축하 사진 파일이 폴더에 없으면 에러 없이 그냥 패스합니다.
        
        # 3. 다음 페이지로 넘어가는 버튼 (누르면 축하 사진들은 사라지고 다음 스테이지로!)
        if st.button("다음 문제로 넘어가기 ➡️"):
            st.session_state.stage += 1
            st.rerun()
    # ------------------ [여기까지 덮어씌우기 끝] ------------------


