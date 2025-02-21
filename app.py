from flask import Flask, render_template, request, jsonify
import os
from common import Common

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # デフォルト値を設定
    player_count = 2
    consecutive_limit = 3
    song_title = "冬のはなし"
    colored_lyrics = None

    if request.method == "POST":
        # フォームからデータを取得
        player_count = int(request.form["playerCount"])
        consecutive_limit = int(request.form["consecutiveLimit"])
        song_title = request.form["songTitle"]

        lyrics_file_path = f"Lyrics/{song_title}.txt"

        # 歌詞が存在しない、またはファイルが空の場合に歌詞入力フィールドを表示
        if not os.path.exists(lyrics_file_path) or os.stat(lyrics_file_path).st_size == 0:
            if "lyrics" in request.form and request.form["lyrics"]:
                lyrics = request.form["lyrics"]
                with open(lyrics_file_path, "w", encoding="utf-8") as file:
                    file.write(lyrics)
            else:
                return render_template(
                    "index.html",
                    lyrics=None,
                    songTitle=song_title,
                    playerCount=player_count,
                    consecutiveLimit=consecutive_limit,
                    showLyricsInput=True  # 歌詞入力フィールドを表示
                )

        # 色付き歌詞を生成
        colored_lyrics = Common.get_colored_lyrics(lyrics_file_path, player_count, consecutive_limit)

    return render_template(
        "index.html",
        lyrics=colored_lyrics,
        songTitle=song_title,
        playerCount=player_count,
        consecutiveLimit=consecutive_limit
    )

@app.route("/register_song", methods=["POST"])
def register_song():
    data = request.get_json()
    song_title = data["songTitle"]
    lyrics = data["lyrics"]

    lyrics_file_path = f"Lyrics/{song_title}.txt"

    if os.path.exists(lyrics_file_path):
        return jsonify({"message": "この曲はすでに登録されています"}), 400

    with open(lyrics_file_path, "w", encoding="utf-8") as file:
        file.write(lyrics)

    return jsonify({"message": "新しい曲が登録されました"})

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
