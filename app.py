import streamlit as st
import pandas as pd
import time

# ---------------------------------------------------------
# 1. 商品データ（「画像URL」も入れると本格的になります）
# ---------------------------------------------------------
data = [
    {"name": "クリスタル楯", "price": 8000, "style": "モダン", "material": "ガラス", "desc": "透明度が高く洗練されたデザイン"},
    {"name": "最高級ブラックウッド楯", "price": 15000, "style": "重厚", "material": "木製", "desc": "社長賞などに適した威厳ある黒木目"},
    {"name": "イタリア製デザインカップ", "price": 25000, "style": "モダン", "material": "金属", "desc": "欧州デザインの芸術的な金属カップ"},
    {"name": "エコノミー木製楯", "price": 4500, "style": "和風", "material": "木製", "desc": "温かみのある木の質感"},
    {"name": "3Dレーザー彫刻キューブ", "price": 9800, "style": "モダン", "material": "ガラス", "desc": "内部に立体的な彫刻が可能"},
    {"name": "伝統的鷲（ワシ）ブロンズ", "price": 12000, "style": "重厚", "material": "金属", "desc": "THE・表彰という定番のブロンズ像"},
    {"name": "アクリル製フルカラー楯", "price": 6000, "style": "ポップ", "material": "アクリル", "desc": "写真やイラストを鮮やかに印刷可能"},
    {"name": "純金メッキ・ビッグカップ", "price": 45000, "style": "豪華", "material": "金属", "desc": "優勝にふさわしい巨大カップ"},
]
df = pd.DataFrame(data)

# ---------------------------------------------------------
# 2. アプリの画面構成
# ---------------------------------------------------------
st.set_page_config(page_title="記念品シェルパ", page_icon="🧞‍♂️")

st.title("🧞‍♂️ 記念品シェルパ")
st.write("いくつかの質問に答えるだけで、最適な商品を提案します。")
st.divider()

# --- Step 1: 予算を聞く ---
st.subheader("Q1. ご予算の上限は？")
budget_option = st.radio(
    "当てはまるものを選んでください",
    ["5,000円以内", "10,000円以内", "30,000円以内", "予算制限なし"],
    horizontal=True,
    index=None # 最初は未選択にする
)

# 選択されるまではここでストップ
if budget_option is None:
    st.stop()

# 予算の金額を数値に変換するロジック
budget_map = {
    "5,000円以内": 5000,
    "10,000円以内": 10000,
    "30,000円以内": 30000,
    "予算制限なし": 999999
}
limit_price = budget_map[budget_option]

# データを絞り込む
candidates = df[df['price'] <= limit_price]

# 候補が0件になった場合の処理
if len(candidates) == 0:
    st.error("申し訳ありません。その予算内の商品が見つかりませんでした。")
    if st.button("最初からやり直す"):
        st.rerun()
    st.stop()

# 候補数を表示（アキネーター風演出）
st.success(f"ふむふむ... {len(candidates)}件の候補がありますね。")
time.sleep(0.5) # 少し「考えている感」を出す

# --- Step 2: 雰囲気を聞く ---
st.divider()
st.subheader("Q2. どんな雰囲気が良いですか？")

# 「残っている候補」の中から、選べるスタイルだけを取り出す
available_styles = candidates['style'].unique().tolist()

style_option = st.radio(
    "イメージに近いものを選んでください",
    available_styles,
    horizontal=True,
    index=None
)

if style_option is None:
    st.stop()

# さらに絞り込む
candidates = candidates[candidates['style'] == style_option]
st.info(f"なるほど、「{style_option}」ですね。残り{len(candidates)}件です。")


# --- Step 3: 素材を聞く（候補が複数ある場合のみ） ---
if len(candidates) > 1:
    st.divider()
    st.subheader("Q3. 素材の好みはありますか？")
    
    available_materials = candidates['material'].unique().tolist()
    # 「こだわらない」という選択肢を追加
    material_option = st.radio(
        "素材を選んでください",
        ["こだわらない"] + available_materials,
        horizontal=True,
        index=None
    )
    
    if material_option is None:
        st.stop()
        
    if material_option != "こだわらない":
        candidates = candidates[candidates['material'] == material_option]

# --- 結果発表 ---
st.divider()
st.header("🎉 あなたへの提案はこちら！")

if len(candidates) == 0:
    st.warning("条件が厳しすぎて見つかりませんでした...")
else:
    for index, row in candidates.iterrows():
        # カード形式で綺麗に表示
        with st.container(border=True):
            st.subheader(f"🏆 {row['name']}")
            st.caption(f"{row['style']} / {row['material']}")
            st.markdown(f"**価格:** ¥{row['price']:,}")
            st.write(row['desc'])
            st.button("詳細を見る", key=index) # ダミーボタン

st.divider()
if st.button("🔄 最初から診断しなおす"):
    st.rerun()
