import datetime as dt
import json
import os
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="TIME FOR YOURSELF", page_icon="🌙", layout="centered")

st.markdown("""<style>
    .stApp { background-color: #faf7f2; }
    h1,h2,h3,p,label,.stMarkdown,div,span { color: #2b3532 !important; font-family: sans-serif; letter-spacing: 0.04em; }
    .main-title { font-size: 1.6rem; font-weight: 300; text-align: center; color: #1e2623; margin-top: 30px; }
    .sub-title { font-size: 0.8rem; text-align: center; color: #6b7571; margin-bottom: 40px; }
    div[data-baseweb="tab-list"] { background-color: transparent; border-bottom: 1px solid #e1e6e2; padding: 0; margin-bottom: 30px; }
    div[data-baseweb="tab"] { color: #8c9692 !important; background-color: transparent !important; font-size: 0.9rem; }
    div[data-baseweb="tab"][aria-selected="true"] { color: #1e2623 !important; border-bottom: 2px solid #1e2623 !important; }
    .stRadio, .calendar-box, div[data-baseweb="select"], div[data-baseweb="base-input"], input, textarea { background-color: #ffffff !important; color: #2b3532 !important; }
    .stRadio, .calendar-box { padding: 25px; border-radius: 8px; border: 1px solid #c8d0cb !important; margin-bottom: 20px; }
    .stTextInput input, .stTextArea textarea { background-color: #ffffff !important; color: #2b3532 !important; border: 1px solid #c8d0cb !important; border-radius: 6px !important; padding: 12px 14px !important; font-size: 0.95rem !important; height: auto !important; }
    .stButton>button { background-color: #4a5951 !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 14px 24px !important; width: 100%; font-weight: 600 !important; }
    .section-card { background-color: #ffffff !important; padding: 30px; border-radius: 8px; margin-top: 20px; margin-bottom: 20px; border: 1px solid #e8ede9 !important; }
    .routine-box { border-left: 6px solid #a4c2b9 !important; }
    .tea-box { border-left: 6px solid #8ca69e !important; }
    .spot-box { border-left: 6px solid #c9b097 !important; }
    .card-label { font-size: 0.7rem; color: #8c9692; text-transform: uppercase; margin-bottom: 4px; }
    .card-title { font-weight: 500; color: #1e2623; font-size: 1.05rem; margin-bottom: 6px; }
    .card-desc { font-size: 0.85rem; color: #4a5450; line-height: 1.75; }
</style>""", unsafe_allow_html=True)

F = "user_app_data_v15.json"

def load():
    if os.path.exists(F):
        try:
            with open(F, "r", encoding="utf-8") as f:
                d = json.load(f)
                if "diary" in d and isinstance(d["diary"], list): return d
        except: pass
    return {"diary": [
        {"date": "2026-10-11", "score": "心地よい時間", "text": "自分のペースで穏やかに過ごせた一日。"},
        {"date": "2026-10-12", "score": "いつも通り", "text": "少し慌ただしかったけれど、夜にリセットできた。"},
        {"date": "2026-10-13", "score": "穏やかな時間", "text": "洗練された美しいデザインが完成した日！"}
    ]}

if "app_data" not in st.session_state: st.session_state.app_data = load()

tab1, tab2, tab3 = st.tabs(["JOURNEY", "DIARY", "ANALYTICS"])

with tab1:
    st.write("##### ROUTE / 通勤ルート")
    start = st.text_input("🏢 出発駅 (Optional)", placeholder="例：立川駅、新宿駅など")
    end = st.text_input("🏠 到着駅 (Optional)", placeholder="例：東京駅、中野駅など")
    mood = st.radio("状態", ["身体的な疲労が強く、休息を優先したい", "神経が昂っており、思考が落ち着かない", "精神的なストレスや、心のモヤモヤを感じる", "時間やタスクに追われ、焦燥感がある", "エネルギーが不足し、少し気分が沈んでいる", "心身ともに比較的落ち着いており、余力がある"], label_visibility="collapsed")

    t_db = {
        "身体的な疲労が強く、休息を優先したい": {"title": "🌿 リラックス・ベースティー", "desc": "カモミール 1 : ルイボス 1 の等倍ブレンド。身体の強張りを緩めます。"},
        "神経が昂っており、思考が落ち着かない": {"title": "💤 ナイト・レストティー", "desc": "カモミール 1 : ラベンダー 1 のブレンド。脳のスイッチを静かにオフにします。"},
        "精神的なストレスや、心のモヤモヤを感じる": {"title": "🍃 リフレッシュ・ミントティー", "desc": "ペパーミント 1 : カモミール 1 のブレンド。滞った気分を通します。"},
        "時間やタスクに追われ、焦燥感がある": {"title": "🌸 プレッシャー緩和ティー", "desc": "お茶に含まれるテアニンとカモミールの安定作用が、焦る心にブレーキをかけます。"},
        "エネルギーが不足し、少し気分が沈んでいる": {"title": "☀️ クリーン・ルイボスブレンド", "desc": "ルイボス 1 : ペパーミント 1 のブレンド。明日への活力を満たします。"},
        "心身ともに比較的落ち着いており、余力がある": {"title": "✨ デイリー・キープティー", "desc": "ルイボス 1 : ローズヒップ 1 のブレンド。健やかな目覚めをサポートします。"}
    }

    if st.button("PROPOSAL / 提案を受け取る"):
        now = dt.datetime.now()
        r_db = {
            "身体的な疲労が強く、休息を優先したい": "今夜はお風呂をシャワーで済ませ、パジャマに着替えてベッドへ直行しましょう。服を選ぶ元気も今夜は使わなくて大丈夫です。",
            "神経が昂っており、思考が落ち着かない": "部屋の照明を少し暗くして、スマホを手の届かない場所に置き、ゆっくり5回深呼吸をしてみましょう。",
            "精神的なストレスや、心のモヤモヤを感じる": "お気に入りのアイスを食べ、大好きな音楽をイヤホンで少し大きめの音量で聴きましょう。",
            "時間やタスクに追われ、焦燥感がある": "明日のタスクを一度すべて紙に書き出し、頭の外のノートに預けてから目を閉じましょう。",
            "エネルギーが不足し、少し気分が沈んでいる": "お気に入りの香りを部屋に少しだけ振るか、ぬるめのお湯にゆっくり10分浸かりましょう。",
            "心身ともに比較的落ち着いており、余力がある": "ちょっと贅沢な入浴剤を使って、スマホを持ち込まずにお風呂の時間をのんびり楽しみましょう。"
        }
        tx = start + end
        if any(x in tx for x in ["立川", "東京", "新宿", "中野", "吉祥寺", "中央線"]):
            if now.hour >= 22: spot = "📍東京駅八重洲口周辺：マクドナルド 八重洲通り店<br>⏰ 24時間営業<br>💡深夜でも明かりが灯る落ち着いたスペース。温かいミルクを飲みスマホをオフにする時間を確保しましょう。"
            else:
                if "立川" in tx: spot = "📍立川駅北口下車：温浴スパ『湯楽の里』、または駅前夜カフェ<br>⏰ 23:00まで営業<br>💡広い炭酸泉や露天風呂に15分以上浸かることで、自律神経が副交感神経へと確実に切り替わります。"
                else: spot = "📍東京駅丸の内北口前：丸の内オアゾ内『丸善・カフェ』<br>⏰ 21:00まで営業<br>💡淹れたてのお茶を飲みながら今日一日を静かにリセットする時間を過ごせます。"
        elif any(x in tx for x in ["皆野", "長瀞", "秩父"]): spot = "📍奥長瀞 秩父温泉 満願の湯 / 露天風呂で疲れをリセット（21:00まで営業）"
        else: spot = "🏡 自宅ベッドでの簡易マインドフルネス / 仰向けになり呼吸に意識を向ける3分間を作ってみてください。"

        st.markdown('<div style="text-align:center; font-size:0.8rem; color:#4a5951 !important; letter-spacing:0.15em; margin-bottom:10px;">* 静かに夜の時間が始まります *</div>', unsafe_allow_html=True)
        st.write(f"⏱️ **判定時刻 {now.strftime('%H:%M')}**")
        st.markdown(f'<div class="section-card routine-box"><div class="card-label">01 / Routine</div><div class="card-title">今夜、お家ですること</div><div class="card-desc">{r_db[mood]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-card tea-box"><div class="card-label">02 / Home Blend Tea</div><div class="card-title">{t_db[mood]["title"]}</div><div class="card-desc">{t_db[mood]["desc"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="section-card spot-box"><div class="card-label">03 / Recommendation</div><div class="card-title">今夜のおすすめ</div><div class="card-desc">{spot}</div></div>', unsafe_allow_html=True)

with tab2:
    st.write("##### DIARY / 今日見つけた「幸せな記憶」")
    score = st.select_slider("今日の心地よさは？", options=["強いストレス", "少し疲れ気味", "いつも通り", "心地よい時間", "穏やかな時間"], value="いつも通り", key="diary_score")
    text = st.text_area("心に残ったほっこりした瞬間を記録しましょう", key="diary_text")
    
    if st.button("SAVE / 記憶を保存する"):
        if text:
            today_str = dt.date.today().strftime("%Y-%m-%d")
            st.session_state.app_data["diary"] = [l for l in st.session_state.app_data["diary"] if l["date"] != today_str]
            st.session_state.app_data["diary"].append({"date": today_str, "score": score, "text": text})
            with open(F, "w", encoding="utf-8") as f:
                json.dump(st.session_state.app_data, f, ensure_ascii=False, indent=4)
            st.rerun()
            
    st.markdown('<br><hr style="border:0; border-top:1px solid #e1e6e2; margin:20px 0;"><br>', unsafe_allow_html=True)
    st.write("##### 📅 ARCHIVE / 過去の記録を読み返す")
    sel_date = st.date_input("カレンダーから日付を選択してください", value=dt.date.today())
    log = next((l for l in st.session_state.app_data["diary"] if l["date"] == sel_date.strftime("%Y-%m-%d")), None)
    if log: st.markdown(f'<div class="section-card" style="border-left-color: #c9b097;"><div class="card-label">📅 {sel_date.strftime("%Y年%m月%d日")} の記憶</div><div class="card-title">{log["score"]}</div><div class="card-desc" style="background:#fcfbf9; padding:15px; border-radius:6px; border:1px solid #f0eae1;">{log["text"]}</div></div>', unsafe_allow_html=True)
    else: st.caption("選択された日付の記録はまだありません。")

with tab3:
    st.write("##### ANALYTICS / 過去の心の波（メンタルリズム）")
    st.write("直近の調子の波（ハーブグリーン）と、理想的な休息サイクルを示す「理想のヒーリング曲線（ゴールド）」を表示しています。")
    logs = st.session_state.app_data["diary"]
    if len(logs) > 0:
        d_logs = logs[-7:]
        dates = [l["date"][-5:] for l in d_logs]
        s_map = {"穏やかな時間": 5, "心地よい時間": 4, "いつも通り": 3, "少し疲れ気味": 2, "強いストレス": 1}
        scores = [s_map.get(l["score"], 3) for l in d_logs]
        
        fig, ax = plt.subplots(figsize=(7, 3.5))
        fig.patch.set_facecolor('#faf7f2')
        ax.set_facecolor('#ffffff')
        ax.plot(dates, scores, color='#4a5951', marker='o', linewidth=2.5, label='Your Wave')
        
        ideal_base = [3.5, 4.2, 2.8, 4.5, 3.2, 4.8, 4.0]
        ideal_scores = [ideal_base[i % len(ideal_base)] for i in range(len(scores))]
        ax.plot(dates, ideal_scores, color='#c9b097', linestyle='--', linewidth=1.5, marker='x', label='Ideal Cycle')
        
        ax.set_ylim(0.5, 5.5)
        ax.grid(axis='y', linestyle='--', alpha=0.4, color='#e1e6e2')
        for s in ["top", "right", "left", "bottom"]: ax.spines[s].set_visible(False)
        ax.tick_params(colors='#4a5450', labelsize=9)
        ax.legend(facecolor='#ffffff', edgecolor='#e8ede9', loc='lower right', fontsize=8)
        st.pyplot(fig)
        
        st.markdown("""<div class="section-card spot-box">
            <div class="card-label" style="color:#c9b097;">🧭 理想のヒーリング曲線（ゴールド）の理由</div>
            <div class="card-title">自然な生体バイオリズムに基づく休息サイクル</div>
            <div class="card-desc">
                <b>1. 自律神経の交互リズム</b><br>夕方以降は緊張（交感神経）から休息（副交感神経）へと切り替わる時間です。一時的にスコアが低下し、セルフケアを経て就寝前に最高値へ向かう「U字型回復」が健康的な生体バイオリズムです。<br><br>
                <b>2. 週の中だるみの肯定</b><br>毎日100点のコンディションを維持するのは不可能です。週の中盤（水〜木）に一度スコアが下がるのは正常な防衛反応であり、週末にかけて回復していく自然なサイン波を基準としています。
            </div>
        </div>""", unsafe_allow_html=True)
    else: st.write("データが蓄積されると、ここに心のバイオリズムグラフが描画されます。")
# ─── 【バグ予防・対策済】Google AdMob 広告表示コード ───
import streamlit as st
import streamlit.components.v1 as components

# 1. 広告の裏にボタンが隠れるのを防ぐための「空地（クッション）」をアプリの最下部に作る
st.write("<div style='margin-bottom: 80px;'></div>", unsafe_allow_html=True)

# 2. 広告を画面最下部に固定表示する（数字をご自身のAdMobのものに書き換えてください）
admob_html = """
<div style="text-align:center; position:fixed; bottom:0; left:0; width:100%; background:#FAF7F2; z-index:9999; padding: 5px 0; border-top: 1px solid #C8D0CB;">
    <script async src="https://googlesyndication.com" crossorigin="anonymous"></script>
    <ins class="adsbygoogle"
         style="display:inline-block;width:320px;height:50px"
         data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
         data-ad-slot="XXXXXXXXXX"></ins>
    <script>
         (adsbygoogle = window.adsbygoogle || []).push({});
    </script>
</div>
"""
components.html(admob_html, height=65)
