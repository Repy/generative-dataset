import pandas as pd
import random

# 再現性のためのシード値固定（ランダムな結果を楽しみたい場合はコメントアウトしてください）
random.seed(42)

# --- 1. 名前の準備 (80種類) ---
# 「山」「佐」「木」「中」が含まれる名字をそれぞれ20種類ずつ用意
last_names_yama = ["山田", "山本", "山下", "山口", "山崎", "小山", "大山", "中山", "杉山", "丸山", 
                   "秋山", "村山", "青山", "横山", "平山", "内山", "片山", "畠山", "松山", "高山"]
last_names_sa = ["佐藤", "佐々木", "佐野", "佐伯", "佐久間", "佐川", "佐竹", "佐渡", "佐原", "佐宗", 
                 "佐々", "佐倉", "佐村", "佐橋", "阿佐", "遊佐", "佐賀", "宇佐美", "佐古", "佐波"]
last_names_ki = ["鈴木", "木村", "青木", "高木", "八木", "荒木", "三木", "茂木", "黒木", "松木", 
                 "柏木", "木下", "木内", "木本", "柚木", "木田", "木幡", "木俣", "木島", "木崎"]
last_names_naka = ["中村", "中島", "中野", "中川", "中田", "中西", "中尾", "中井", "中澤", "中根", 
                   "中原", "中谷", "中林", "畑中", "野中", "山中", "田中", "中丸", "中本", "中塚"]

last_names = last_names_yama + last_names_sa + last_names_ki + last_names_naka

# 下の名前のリスト
first_names = ["太郎", "次郎", "健太", "翔太", "大樹", "花子", "恵子", "明子", "結衣", "さくら", "蓮", "陽菜"]

# 名字をシャッフルして下の名前とランダムに結合
random.shuffle(last_names)
names = [f"{last_name} {random.choice(first_names)}" for last_name in last_names]

# --- 2. 点数生成関数の定義 ---
def generate_base_score(grade, cls):
    # 基準点: 学年が上がるごとに基礎学力が上がると仮定 (1年:45, 2年:50, 3年:55, 4年:60)
    base_score = 40 + (grade * 5)
    
    # ばらつきの追加: 標準偏差を25と大きくとり、クラス内での点差を開かせる
    base_score = int(random.gauss(base_score, 15))
    
    # 10〜95の範囲に強制的に収める
    return max(10, min(95, base_score))

def generate_score(grade, cls, subject, base_score):
    # クラス・科目ごとの傾向
    if cls == 'F':
        # Fクラスは文系科目が得意な傾向
        if subject in ['英I', '現国', '公民']:
            base_score += 10
        elif subject in ['数I', '情報']:
            base_score -= 10
    elif cls == 'M':
        # Mクラスは理系科目が得意な傾向
        if subject in ['数I', '情報']:
            base_score += 10
        elif subject in ['英I', '現国', '公民']:
            base_score -= 10
            
    # ばらつきの追加: 標準偏差を25と大きくとり、クラス内での点差を開かせる
    score = int(random.gauss(base_score, 7))
    
    # 10〜95の範囲に強制的に収める
    return max(2, min(100, score))

# --- 3. データ生成 ---
data = []
name_index = 0
subjects = ['数I', '英I', '現国', '公民', '情報']

for grade in range(1, 5):
    for cls in ['F', 'M']:
        for num in range(1, 11):
            row = {
                '年次': grade,
                'クラス': cls,
                '番号': num,
                '名前': names[name_index]
            }

            base_score = generate_base_score(grade, cls)
            for subj in subjects:
                row[subj] = generate_score(grade, cls, subj, base_score)
                
            data.append(row)
            name_index += 1

df = pd.DataFrame(data)

print(df.head(20).to_string(index=False))

df.to_csv('data.csv', index=True)
