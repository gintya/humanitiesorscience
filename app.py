from flask import Flask, render_template, request

app = Flask(__name__)

# 36問の質問データ（各軸9問×4軸）
questions_36 = [
    # A / L（Art / Logic）
    {"id": 1, "text": "古文書を手にしたときの興味は？", "options": ["A", "L"], "labels": ["文字の美しさに目を奪われる", "内容の論理性に注目する"]},
    {"id": 2, "text": "研究室に飾るなら？", "options": ["A", "L"], "labels": ["芸術作品", "方程式が描かれたポスター"]},
    {"id": 3, "text": "美術館と科学館、どちらに行く？", "options": ["A", "L"], "labels": ["美術館", "科学館"]},
    {"id": 4, "text": "楽譜を見た時の興味は？", "options": ["A", "L"], "labels": ["感情が動く", "音の構造に注目"]},
    {"id": 5, "text": "映画の感想は？", "options": ["A", "L"], "labels": ["演出の美しさ", "筋書きの整合性"]},
    {"id": 6, "text": "抽象画を見たら？", "options": ["A", "L"], "labels": ["自由に解釈する", "分析したくなる"]},
    {"id": 7, "text": "ノートの取り方は？", "options": ["A", "L"], "labels": ["カラフルで自由", "整然と構造化"]},
    {"id": 8, "text": "プレゼン資料の作成で重視するのは？", "options": ["A", "L"], "labels": ["デザイン", "論理の構成"]},
    {"id": 9, "text": "本を選ぶ基準は？", "options": ["A", "L"], "labels": ["感性に訴えるもの", "論理的に知識が得られるもの"]},

    # C / I（Concrete / Imaginative）
    {"id": 10, "text": "何かを学ぶとき？", "options": ["C", "I"], "labels": ["現実的に使えるかを考える", "夢が広がることを期待"]},
    {"id": 11, "text": "説明を受けた時？", "options": ["C", "I"], "labels": ["具体例があると安心", "抽象的な概念が楽しい"]},
    {"id": 12, "text": "空想小説を読むと？", "options": ["C", "I"], "labels": ["現実味がないと興味が薄れる", "想像力がかき立てられる"]},
    {"id": 13, "text": "授業で扱う題材は？", "options": ["C", "I"], "labels": ["実用的なものがいい", "発想力が求められるものがいい"]},
    {"id": 14, "text": "旅行の計画では？", "options": ["C", "I"], "labels": ["綿密な行程を立てる", "その場の雰囲気で動きたい"]},
    {"id": 15, "text": "説明書を読む時？", "options": ["C", "I"], "labels": ["手順通りに実行", "全体を理解してから動く"]},
    {"id": 16, "text": "目標設定では？", "options": ["C", "I"], "labels": ["達成可能な範囲で", "理想から逆算する"]},
    {"id": 17, "text": "話し合いで好む話題は？", "options": ["C", "I"], "labels": ["現実的な課題解決", "未来の可能性"]},
    {"id": 18, "text": "好きな映画のタイプは？", "options": ["C", "I"], "labels": ["リアルなヒューマンドラマ", "幻想的なファンタジー"]},

    # R / S（Rational / Sensitive）
    {"id": 19, "text": "友達が悩んでいたら？", "options": ["R", "S"], "labels": ["解決方法を探る", "共感して寄り添う"]},
    {"id": 20, "text": "失敗したとき？", "options": ["R", "S"], "labels": ["原因を分析する", "自分を慰める"]},
    {"id": 21, "text": "相談されたら？", "options": ["R", "S"], "labels": ["冷静な意見を述べる", "気持ちに共感する"]},
    {"id": 22, "text": "恋愛について語るなら？", "options": ["R", "S"], "labels": ["理屈で考える", "感情で語る"]},
    {"id": 23, "text": "仲間に裏切られた時？", "options": ["R", "S"], "labels": ["理由を知ろうとする", "深く傷つく"]},
    {"id": 24, "text": "プロジェクトの意見対立時？", "options": ["R", "S"], "labels": ["最適解を探る", "感情面を調整する"]},
    {"id": 25, "text": "人に怒られたら？", "options": ["R", "S"], "labels": ["指摘内容を受け止める", "感情を引きずる"]},
    {"id": 26, "text": "本を読んだとき？", "options": ["R", "S"], "labels": ["論点を整理する", "感情の起伏に注目"]},
    {"id": 27, "text": "チーム内での役割？", "options": ["R", "S"], "labels": ["判断役", "気遣い役"]},

    # D / F（Decisive / Flexible）
    {"id": 28, "text": "計画の進め方？", "options": ["D", "F"], "labels": ["予定通り進めたい", "臨機応変に動きたい"]},
    {"id": 29, "text": "問題が起きたとき？", "options": ["D", "F"], "labels": ["すぐに判断する", "様子を見る"]},
    {"id": 30, "text": "提出期限が近いとき？", "options": ["D", "F"], "labels": ["前もって準備する", "ぎりぎりに集中する"]},
    {"id": 31, "text": "新しい仕事が来たら？", "options": ["D", "F"], "labels": ["手順を立てる", "とりあえず始める"]},
    {"id": 32, "text": "仕事のやり方に対して？", "options": ["D", "F"], "labels": ["自分なりの方法にこだわる", "その場に合わせる"]},
    {"id": 33, "text": "目標達成の姿勢？", "options": ["D", "F"], "labels": ["一貫した姿勢で", "柔軟に方向転換"]},
    {"id": 34, "text": "優先するのは？", "options": ["D", "F"], "labels": ["達成までの道筋", "その時の状況"]},
    {"id": 35, "text": "複数の仕事を抱えたとき？", "options": ["D", "F"], "labels": ["優先順位で管理", "気分で取り組む"]},
    {"id": 36, "text": "旅行中にトラブルがあったら？", "options": ["D", "F"], "labels": ["即対応策を考える", "その場で流れに乗る"]}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html", questions=questions_36)

@app.route("/result", methods=["POST"])
def result():
    answers = request.form
    score = {"A": 0, "L": 0, "C": 0, "I": 0, "R": 0, "S": 0, "D": 0, "F": 0}

    for answer in answers.values():
        if answer in score:
            score[answer] += 1

    result_type = ""
    result_type += "A" if score["A"] >= score["L"] else "L"
    result_type += "C" if score["C"] >= score["I"] else "I"
    result_type += "R" if score["R"] >= score["S"] else "S"
    result_type += "D" if score["D"] >= score["F"] else "F"

    return render_template("result.html", result=result_type)

if __name__ == "__main__":
    app.run(debug=True)
