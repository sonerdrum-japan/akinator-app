import streamlit as st
import pandas as pd

# データ
data = [
    {"name": "クリスタル楯", "price": 8000, "style": "モダン", "material": "ガラス"},
    {"name": "高級ブラックウッド楯", "price": 15000, "style": "重厚", "material": "木製"},
    {"name": "デザインカップ", "price": 25000, "style": "モダン", "material": "金属"},
    {"name": "木製楯(小)", "price": 4500, "style": "和風", "material": "木製"},
    {"name": "3Dクリスタル", "price": 9800, "style": "モダン", "material": "ガラス"},
]
df = pd.DataFrame(data)

# 画面
st.title("🏆 記念品提案アプリ")

# 予算スライダー
budget = st.slider("予算の上限 (円)", 1000, 30000, 10000)
st.write(f"予算: {budget}円")

# フィルタリング
candidates = df[df['price'] <= budget]

# 結果表示
st.subheader(f"提案数: {len(candidates)}件")
if len(candidates) > 0:
    for index, row in candidates.iterrows():
        st.info(f"■ {row['name']} ({row['price']}円) - {row['material']}")
else:
    st.error("条件に合う商品がありません")