from flask import Flask, render_template, session, request, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'secret_key_for_session'

# ------------------------------------------------------------------
# 1. 도전과제 목록
# ------------------------------------------------------------------
achievement_list = [
    {"id": "ach_start", "title": "지옥으로의 첫걸음", "desc": "게임을 처음 시작했다.", "hidden": False},
    {"id": "ach_beomjun", "title": "통곡의 벽", "desc": "김범준에게 가로막혔다.", "hidden": False},
    {"id": "ach_noise", "title": "고막 파괴자", "desc": "노래팀의 소음을 견뎌냈다.", "hidden": False},
    {"id": "ach_director", "title": "컷! 오케이!", "desc": "최유혁 감독의 눈에 들었다.", "hidden": False},
    {"id": "ach_coding", "title": "코딩 노예", "desc": "조율희의 징징거림을 들었다.", "hidden": False},
    {"id": "ach_muscle", "title": "3대 500", "desc": "유승후의 근육 자랑을 목격했다.", "hidden": False},
    {"id": "ach_mood", "title": "조울증 주의보", "desc": "권재현의 급격한 감정 변화를 겪었다.", "hidden": False},
    {"id": "ach_art", "title": "피카소의 재림", "desc": "정이현의 난해한 예술 세계를 접했다.", "hidden": False},
    {"id": "ach_thumb", "title": "썸네일 각", "desc": "이예준과 정태겸에게 장난을 당했다.", "hidden": False},
    {"id": "ach_posi", "title": "무한 긍정교", "desc": "나기찬의 긍정 에너지를 받았다.", "hidden": False},
    {"id": "ach_polit", "title": "정치질의 서막", "desc": "박재윤의 연설을 들었다.", "hidden": False},
    {"id": "ach_sound", "title": "괴음 수집가", "desc": "한진환의 욕망의 소리를 들었다.", "hidden": False},
    {"id": "ach_fight", "title": "평화주의자", "desc": "싸움을 말리려고 시도했다.", "hidden": False},
    {"id": "ach_curious", "title": "호기심 천국", "desc": "개발팀의 상황을 엿보았다.", "hidden": False},
    {"id": "ach_end1", "title": "엔딩: 소음 공해", "desc": "고음 대결의 희생양이 되었다.", "hidden": False},
    {"id": "ach_end2", "title": "엔딩: 무한 야근", "desc": "영원히 퇴근하지 못하게 되었다.", "hidden": False},
    {"id": "ach_end3", "title": "엔딩: 파국", "desc": "동아리가 공중분해 되었다.", "hidden": False},
    {"id": "ach_end4", "title": "엔딩: 흑역사 생성", "desc": "괴작 영화의 주연이 되었다.", "hidden": False},
    {"id": "ach_end5", "title": "엔딩: 정신 붕괴", "desc": "정신이 혼미해져 생각을 그만두었다.", "hidden": False},
    {"id": "ach_reset", "title": "도르마무", "desc": "게임을 리셋했다.", "hidden": False},
    {"id": "ach_hidden", "title": "???", "desc": "메인 화면의 비밀을 풀었다.", "hidden": True} 
]

# ------------------------------------------------------------------
# 2. 캐릭터 데이터
# ------------------------------------------------------------------
characters = {
    "minchan": {"name": "구민찬", "desc": "거만함, 자존감MAX, 에겐남 (노래)", "img": "minchan.png"},
    "jaehyun": {"name": "권재현", "desc": "감정기복 심함, 오타쿠 (디자인)", "img": "jaehyun.png"},
    "kichan":  {"name": "나기찬", "desc": "긍정맨, 불도저 (기획)", "img": "kichan.png"},
    "geunwoo": {"name": "박근우", "desc": "알파메일, 고음 발사 (노래)", "img": "geunwoo.png"},
    "jaeyoon": {"name": "박재윤", "desc": "정치 관심, 선동가 (애늙은이)", "img": "jaeyoon.png"},
    "seunghu": {"name": "유승후", "desc": "듬직함, 헬창, 겜덕후 (개발)", "img": "seunghu.png"},
    "yejun":   {"name": "이예준", "desc": "편집 장인, 장난꾸러기 (방송부)", "img": "yejun.png"},
    "yihyun":  {"name": "정이현", "desc": "목표 확고, 경험 많은 줄쟁이 (그림)", "img": "yihyun.png"},
    "taegyeom":{"name": "정태겸", "desc": "여사친 많음, 놀리기 장인", "img": "taegyeom.png"},
    "yulhee":  {"name": "조율희", "desc": "동네북, 관종 (코딩)", "img": "yulhee.png"},
    "yuhyuk":  {"name": "최유혁", "desc": "영화 기획, 샤우팅 (기획)", "img": "yuhyuk.png"},
    "jinhwan": {"name": "한진환", "desc": "욕망의 항아리, 괴음 발사 (디자인)", "img": "jinhwan.png"},
    "beomjun": {"name": "김범준", "desc": "최장신, 통나무, 전학생 (공부)", "img": "beomjun.png"},
}

# ------------------------------------------------------------------
# 3. 시나리오 데이터 (6장 + 효과음/진동/파국게이지 포함)
# ------------------------------------------------------------------
scenes = {
    # [제1장: 혼돈의 서막]
    "start": {
        "text": "동아리방 문 앞... 안에서 심상치 않은 기운이 느껴진다. 들어갈까?",
        "images": ["bg_office.png"], "speaker": "나",
        "choices": [{"text": "용기 내어 문을 연다.", "next": "chapter1_intro"}],
        "achievement": "ach_start"
    },
    "chapter1_intro": {
        "text": "문을 열자마자 거대한 통나무 같은 남자가 앞을 가로막는다. (쿵!)",
        "images": ["beomjun.png"], "speaker": "김범준",
        "choices": [{"text": "비켜달라고 한다.", "next": "chapter1_gatekeeper"}],
        "shake": True, "sfx": "thud.mp3", "doom": 10 # 효과 추가
    },
    "chapter1_gatekeeper": {
        "text": "공부... 하러 왔나? 아니면 놀러 왔나... (무표정하게 내려다본다)",
        "images": ["beomjun.png"], "speaker": "김범준",
        "choices": [
            {"text": "시끄러운 소리가 나는 쪽으로 뚫고 간다.", "next": "route_enter_ent"},
            {"text": "컴퓨터가 모여있는 구석으로 피신한다.", "next": "route_enter_dev"}
        ],
        "achievement": "ach_beomjun"
    },

    # [제2장 A: 예능팀]
    "route_enter_ent": {
        "text": "방 한복판에서 두 남자가 마이크를 잡고 성대를 혹사시키고 있다.",
        "images": ["minchan.png", "geunwoo.png"], "speaker": "나",
        "choices": [{"text": "귀를 막으며 다가간다.", "next": "ch2_ent_battle"}],
        "achievement": "ach_noise"
    },
    "ch2_ent_battle": {
        "text": "내 고음이 더 완벽해! 넌 감성이 부족해, 이 에겐남아! (고음 발사)",
        "images": ["minchan.png", "geunwoo.png"], "speaker": "박근우",
        "choices": [{"text": "지켜본다.", "next": "ch2_ent_battle_2"}],
        "shake": True, "sfx": "scream.mp3", "doom": 10 # 효과 추가
    },
    "ch2_ent_battle_2": {
        "text": "흥, 웃기는군. 내 노래는 자존감 그 자체다. 네가 뭘 알아?",
        "images": ["minchan.png", "geunwoo.png"], "speaker": "구민찬",
        "choices": [
            {"text": "싸움을 말린다.", "next": "ch2_ent_prank"},
            {"text": "같이 노래를 부른다.", "next": "bad_end_concert"}
        ]
    },
    "ch2_ent_prank": {
        "text": "그때, 카메라를 든 두 명이 낄낄거리며 나타난다.",
        "images": ["yejun.png", "taegyeom.png"], "speaker": "이예준 & 정태겸",
        "choices": [{"text": "뭐 하는 거야?", "next": "ch2_ent_prank_2"}],
        "achievement": "ach_fight"
    },
    "ch2_ent_prank_2": {
        "text": "야, 이거 편집각이다 ㅋㅋㅋ 방금 민찬이 표정 봤냐? 썸네일 뽑았다.",
        "images": ["yejun.png", "taegyeom.png"], "speaker": "이예준",
        "choices": [{"text": "태겸에게 도움을 요청한다.", "next": "ch2_ent_prank_3"}],
        "achievement": "ach_thumb"
    },
    "ch2_ent_prank_3": {
        "text": "도와달라고? ㅋㅋㅋ 네 반응이 재밌어서 더 놀리고 싶은데? 어쩔티비?",
        "images": ["taegyeom.png"], "speaker": "정태겸",
        "choices": [
            {"text": "화낸다.", "next": "ch2_ent_movie_start"},
            {"text": "무시한다.", "next": "ch2_ent_movie_start"}
        ]
    },
    "ch2_ent_movie_start": {
        "text": "갑자기 조명이 켜지며 누군가 메가폰을 들고 난입한다. 컷!!! 컷!!!",
        "images": ["yuhyuk.png"], "speaker": "최유혁",
        "choices": [{"text": "넌 또 누구야?", "next": "ch2_ent_movie_2"}]
    },
    "ch2_ent_movie_2": {
        "text": "방금 그 감정선 아주 좋았어! 내 영화 <절규하는 동아리>의 주연으로 캐스팅한다! 액션!!",
        "images": ["yuhyuk.png"], "speaker": "최유혁",
        "choices": [
            {"text": "도망친다.", "next": "ch2_bulldozer"},
            {"text": "거절한다.", "next": "ch2_bulldozer"}
        ],
        "achievement": "ach_director"
    },

    # [제2장 B: 개발팀]
    "route_enter_dev": {
        "text": "구석진 자리... 한 명은 울고 있고 한 명은 근육을 과시 중이다.",
        "images": ["yulhee.png", "seunghu.png"], "speaker": "나",
        "choices": [{"text": "무슨 상황이지?", "next": "ch2_dev_cry"}],
        "achievement": "ach_curious"
    },
    "ch2_dev_cry": {
        "text": "형님... 나 너무 불쌍하지? 나 좀 봐줘...",
        "images": ["yulhee.png", "seunghu.png"], "speaker": "조율희",
        "choices": [{"text": "승후에게 말을 건다.", "next": "ch2_dev_tank"}],
        "achievement": "ach_coding",
        "doom": 5 # 파국 살짝 증가
    },
    "ch2_dev_tank": {
        "text": "걱정 마. 내 근육을 봐. 그냥 탱크처럼 밀어붙여.",
        "images": ["seunghu.png"], "speaker": "유승후",
        "choices": [{"text": "그때, 옆자리에서 한숨 소리가 들린다.", "next": "ch2_dev_art"}],
        "achievement": "ach_muscle"
    },
    "ch2_dev_art": {
        "text": "진지한 표정으로 그림을 그리고 있는 남자가 있다.",
        "images": ["yihyun.png"], "speaker": "정이현",
        "choices": [{"text": "뭘 그리는 거야?", "next": "ch2_dev_art_2"}]
    },
    "ch2_dev_art_2": {
        "text": "이건 단순한 그림이 아니야. 내 야망과 10년 뒤의 미래가 담긴 '선'이다. 이해하겠어?",
        "images": ["yihyun.png"], "speaker": "정이현",
        "choices": [
            {"text": "이해 못 하겠다고 한다.", "next": "ch2_dev_design"},
            {"text": "멋있다고 해준다.", "next": "ch2_dev_design"}
        ],
        "achievement": "ach_art",
        "shake": False, "sfx": "ch_dev_art_2.mp3", "doom": 50
    },
    "ch2_dev_design": {
        "text": "으아악! 이 그림 완전 별로야! 아니? 다시 보니 천재적인가? 아니 쓰레기야!",
        "images": ["jaehyun.png", "yihyun.png"], "speaker": "권재현",
        "choices": [{"text": "재현이 머리를 쥐어뜯고 있다.", "next": "ch2_dev_design_2"}],
        "achievement": "ach_mood"
    },
    "ch2_dev_design_2": {
        "text": "내 스텔라이브 컬렉션이랑 색감이 안 맞아! 감정 기복이 멈추질 않아!!",
        "images": ["jaehyun.png"], "speaker": "권재현",
        "choices": [
            {"text": "진정하라고 한다.", "next": "new_art_movie_1"},
            {"text": "무시한다.", "next": "new_art_movie_1"}
        ]
    },

    # [추가씬 1]
    "new_art_movie_1": {
        "text": "그때, 메가폰을 든 남자가 그림을 훔쳐보더니 소리를 지른다. 컷!!!!",
        "images": ["yihyun.png", "yuhyuk.png"], "speaker": "최유혁",
        "choices": [{"text": "깜짝 놀라 쳐다본다.", "next": "new_art_movie_2"}],
        "sfx": "scream.mp3" # 소리 추가
    },
    "new_art_movie_2": {
        "text": "아니 이 그림엔 소울이 없어! 폭발! 굉음! 클라이막스가 어디 갔어?! 다시 그려!!",
        "images": ["yihyun.png", "yuhyuk.png"], "speaker": "최유혁",
        "choices": [{"text": "정이현의 표정이 싸늘하게 식는다.", "next": "new_art_movie_3"}]
    },
    "new_art_movie_3": {
        "text": "이 '선'은 내면의 폭발을 형상화한 거다... 얄팍한 상업 영화 감독 따위가 예술을 알겠나?",
        "images": ["yihyun.png", "yuhyuk.png"], "speaker": "정이현",
        "choices": [{"text": "분위기가 험악해진다.", "next": "new_art_movie_4"}],
        "shake": False, "sfx": "new_art_movie_3", "doom": 50
    },
    "new_art_movie_4": {
        "text": "뭐?! 상업? 야!! 내 영화는 블록버스터야!! 당장 내 콘티에서 나가!!",
        "images": ["yihyun.png", "yuhyuk.png"], "speaker": "최유혁",
        "choices": [{"text": "둘을 피해 도망간다.", "next": "ch2_bulldozer"}]
    },

    # [제3장]
    "ch2_bulldozer": {
        "text": "혼란스러운 와중에, 엄청나게 긍정적인 에너지를 뿜는 남자가 등장한다.",
        "images": ["kichan.png"], "speaker": "나기찬",
        "choices": [{"text": "넌 또 뭐야?", "next": "ch3_planning"}],
        "achievement": "ach_posi"
    },
    "ch3_planning": {
        "text": "얘들아! 싸우지 마! 우리 이 아이디어 전부 다 섞어서 출시하자! 할 수 있어! 무조건 돼!",
        "images": ["kichan.png"], "speaker": "나기찬",
        "choices": [{"text": "그게 무슨 소리야?", "next": "new_posi_desire_1"}]
    },

    # [추가씬 2]
    "new_posi_desire_1": {
        "text": "그때, 기찬의 뒤에서 끈적한 시선이 느껴진다. <s>(검열됨)</s>",
        "images": ["kichan.png", "jinhwan.png"], "speaker": "한진환",
        "choices": [{"text": "기찬이 소름 돋아 한다.", "next": "new_posi_desire_2"}],
        "achievement": "ach_sound"
    },
    "new_posi_desire_2": {
        "text": "<s>섞어야지... 서로의 욕망을... (검열됨)...</s>",
        "images": ["kichan.png", "jinhwan.png"], "speaker": "한진환",
        "choices": [{"text": "기찬이 뒷걸음질 친다.", "next": "new_posi_desire_3"}]
    },
    "new_posi_desire_3": {
        "text": "으악! 아니야! 열정! 꿈! 희망! 왜 자꾸 이상한 소리를 내는 거야!",
        "images": ["kichan.png", "jinhwan.png"], "speaker": "나기찬",
        "choices": [{"text": "진환이 혀를 낼름거린다.", "next": "new_posi_desire_4"}]
    },
    "new_posi_desire_4": {
        "text": "<s>꿈도... 욕망이지... 이리 와...(검열됨)</s>",
        "images": ["jinhwan.png", "kichan.png"], "speaker": "한진환",
        "choices": [{"text": "개판 오분 전이다.", "next": "ch3_politic"}]
    },

    # [3장 마무리]
    "ch3_politic": {
        "text": "잠깐. 그렇게 주먹구구식으로 하면 안 되지. 이 동아리엔 '권력과 상식'이 필요해.",
        "images": ["jaeyoon.png", "kichan.png"], "speaker": "박재윤",
        "choices": [{"text": "재윤이 진지하게 안경을 추어올린다.", "next": "ch3_politic_2"}]
    },
    "ch3_politic_2": {
        "text": "저는!! <s>드럼통따위 알바 아닙니다!!</s> 확실하게 찢어버리겠습니다! 저를 따르십시오!",
        "images": ["jaeyoon.png"], "speaker": "박재윤",
        "choices": [{"text": "사태가 점점 심각해진다.", "next": "ch4_intro"}],
        "achievement": "ach_polit"
    },

    # [제4장]
    "ch4_intro": {
        "text": "동아리방이 아수라장이 된 순간, 플래시가 터진다. 찰칵! 찰칵!",
        "images": ["yejun.png", "taegyeom.png"], "speaker": "이예준 & 정태겸",
        "choices": [{"text": "너희들 아까부터 뭐해?", "next": "ch4_viral"}]
    },
    "ch4_viral": {
        "text": "제목: 동아리 망해가는 과정 실황 중계 ㅋㅋㅋ 조회수 떡상이다!!",
        "images": ["yejun.png", "taegyeom.png"], "speaker": "이예준",
        "choices": [{"text": "카메라를 치우라고 한다.", "next": "ch4_viral_2"}]
    },
    "ch4_viral_2": {
        "text": "왜? 너도 출연료 줘? 아~ 관종이라 끼고 싶구나? 어쩔티비 저쩔티비~",
        "images": ["yejun.png", "taegyeom.png"], "speaker": "정태겸",
        "choices": [
            {"text": "방송부 녀석들과 말싸움한다.", "next": "ch5_intro"},
            {"text": "구석에서 조용히 나가는 정이현을 따라간다.", "next": "hidden_yihyun_start"} 
        ]
    },

    # [제5장]
    "ch5_intro": {
        "text": "그때, 교탁쪽에서 최유혁이 아무이유없이 소리지른다.",
        "images": ["yuhyuk.png", "beomjun.png"], "speaker": "최유혁",
        "choices": [{"text": "깜짝 놀라 쳐다본다.", "next": "ch5_slave_revolt"}],
        "shake": True, "sfx": "crash.mp3", "doom": 20 # 효과 추가
    },
    "ch5_slave_revolt": {
        "text": "으아아악!! 우쿠렐레 줄이 끊어졌어!!!",
        "images": ["yujyuk.png"], "speaker": "최유혁",
        "choices": [{"text": "유혁이가 울분을 토한다.", "next": "ch5_gatekeeper_angry"}]
    },
    "ch5_gatekeeper_angry": {
        "text": "(벌떡 일어나며) ...조용히 해라. 소음 측정 결과 90데시벨 초과. 공부에 방해된다.",
        "images": ["beomjun.png", "yulhee.png"], "speaker": "김범준",
        "choices": [{"text": "범준의 눈빛이 살벌하다.", "next": "ch5_chaos_climax"}]
    },
    "ch5_chaos_climax": {
        "text": "범준이 거대한 한진환을 집어 들었다. 이건 흉기다. (위기감지)",
        "images": ["beomjun.png"], "speaker": "김범준",
        "choices": [{"text": "살려주세요!", "next": "ch6_intro"}],
        "shake": True, "sfx": "thud.mp3", "doom": 30 # 효과 추가
    },

    # [제6장]
    "ch6_intro": {
        "text": "노래, 영화, 정치, 욕망, 렉카, 폭력... 모든 혼돈이 한자리에 모였다.",
        "images": ["bg_office.png"], "speaker": "나",
        "choices": [{"text": "이제 결정을 내려야 한다.", "next": "final_choice"}]
    },
    "final_choice": {
        "text": "이 미친 동아리에서 나의 운명을 결정할 시간이다.",
        "images": ["bg_office.png"], "speaker": "나",
        "choices": [
            {"text": "나기찬의 긍정론을 믿는다.", "next": "bad_end_working"},
            {"text": "박재윤의 선동에 동참한다.", "next": "bad_end_prison"},
            {"text": "최유혁의 영화에 출연한다.", "next": "bad_end_movie"},
            {"text": "그냥 기절한다.", "next": "bad_end_chaos"}
        ]
    },

    # [히든 페이즈]
    "hidden_yihyun_start": {
        "text": "소란스러운 동아리방을 빠져나와, 옥상에 있는 정이현을 발견했다.",
        "images": ["yihyun.png"], "speaker": "정이현",
        "choices": [{"text": "여기서 뭐 해?", "next": "hidden_yihyun_2"}]
    },
    "hidden_yihyun_2": {
        "text": "...소음은 영감을 죽이지. 하지만 저 아래의 혼돈도 멀리서 보면 하나의 색채일 뿐이야.",
        "images": ["yihyun.png"], "speaker": "정이현",
        "choices": [{"text": "무슨 뜻이야?", "next": "hidden_yihyun_3"}],
        "shake": False, "sfx": "hidden_end.mp3", "doom": 50
    },
    "hidden_yihyun_3": {
        "text": "너는 저들과 달라. 내 그림의 [빈 공간] 이 되어줄 수 있을 것 같군. 나와 함께 심연을 그려보지 않겠나?",
        "images": ["yihyun.png"], "speaker": "정이현",
        "choices": [{"text": "그의 손을 잡는다.", "next": "hidden_end_museum"}],
        "shake": False, "sfx": "hidden_2.mp3", "doom": 50
    },
    "hidden_end_museum": {
        "text": "[히든 엔딩] 나는 정이현의 전속 모델이 되었다. \n내 얼굴은 추상적으로 왜곡되어 100년 뒤 미술관에 걸렸다.\n기쁜 건가? 슬픈 건가? 알 수 없지만, 적어도 시끄럽진 않다.",
        "images": ["yihyun.png"], "speaker": "엔딩: 불멸의 뮤즈",
        "choices": [{"text": "처음으로 돌아가기", "next": "start"}]
    },

    # [엔딩 목록]
    "bad_end_concert": {
        "text": "민찬과 근우의 고음 대결 사이에 끼어 고막이 영구 손상되었다. 그들은 멈추지 않는다...",
        "images": ["minchan.png", "geunwoo.png"], "speaker": "배드 엔딩: 소음 공해",
        "choices": [{"text": "처음으로", "next": "start"}],
        "achievement": "ach_end1"
    },
    "bad_end_working": {
        "text": "나기찬의 '할 수 있다'는 말에 속아 365일 야근을 하게 되었다. 유승후가 도망가지 못하게 감시한다.",
        "images": ["kichan.png", "seunghu.png"], "speaker": "배드 엔딩: 무한 야근",
        "choices": [{"text": "처음으로", "next": "start"}],
        "achievement": "ach_end2"
    },
    "bad_end_prison": {
        "text": "박재윤의 정치질에 휘말려 동아리가 파벌 싸움으로 번졌다. 결국 동아리는 공중분해 되었다.",
        "images": ["jaeyoon.png"], "speaker": "배드 엔딩: 파국",
        "choices": [{"text": "처음으로", "next": "start"}],
        "achievement": "ach_end3"
    },
    "bad_end_movie": {
        "text": "최유혁의 괴작 영화에 주연으로 데뷔했다. 이예준이 악마의 편집을 해서 나는 전국적인 놀림감이 되었다.",
        "images": ["yuhyuk.png", "yejun.png"], "speaker": "배드 엔딩: 흑역사 생성",
        "choices": [{"text": "처음으로", "next": "start"}],
        "achievement": "ach_end4"
    },
    "bad_end_chaos": {
        "text": "한진환의 괴음, 조율희의 징징거림, 정이현의 난해함... 정신이 혼미해져 나는 영원히 생각하기를 그만두었다.",
        "images": ["jinhwan.png", "yulhee.png", "yihyun.png"], "speaker": "배드 엔딩: 정신 붕괴",
        "choices": [{"text": "처음으로", "next": "start"}],
        "achievement": "ach_end5"
    }
}

# ------------------------------------------------------------------
# 4. 라우팅
# ------------------------------------------------------------------

@app.route('/')
def main_menu():
    return render_template('main_menu.html', achievement_list=achievement_list, characters=characters)

@app.route('/start_game')
def start_game():
    session.clear()
    session['current_scene'] = 'start'
    session['doom_gauge'] = 0
    session['visited_scenes'] = [] 
    return redirect(url_for('game_screen'))

@app.route('/game')
def game_screen():
    if 'current_scene' not in session:
        return redirect(url_for('main_menu'))

    current_scene_id = session['current_scene']
    scene_data = scenes.get(current_scene_id, scenes['start'])
    
    current_char_info = None
    speaker_name = scene_data.get('speaker', '')
    speaker_key = None
    for key, val in characters.items():
        if val['name'] in speaker_name:
            current_char_info = val
            speaker_key = key
            break

    current_achievement = scene_data.get('achievement', None)
    achievement_info = None
    if current_achievement:
        for ach in achievement_list:
            if ach['id'] == current_achievement:
                achievement_info = ach
                break
    
    # 파국 게이지 처리
    if 'visited_scenes' not in session:
        session['visited_scenes'] = []

    if current_scene_id not in session['visited_scenes']:
        doom_add = scene_data.get('doom', 0)
        session['doom_gauge'] = min(100, session.get('doom_gauge', 0) + doom_add)
        session['visited_scenes'].append(current_scene_id)
        session.modified = True

    effect_data = {
        'shake': scene_data.get('shake', False),
        'sfx': scene_data.get('sfx', None),
        'doom': session.get('doom_gauge', 0)
    }

    return render_template('index.html', 
                           scene=scene_data, 
                           current_char=current_char_info,
                           speaker_key=speaker_key,
                           achievement_info=achievement_info,
                           effect_data=effect_data)

@app.route('/action/<next_scene>')
def action(next_scene):
    session['current_scene'] = next_scene
    return redirect(url_for('game_screen'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('main_menu'))

if __name__ == '__main__':
    app.run(debug=True)