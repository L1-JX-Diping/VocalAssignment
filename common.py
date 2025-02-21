import random
from part import Part

# HTML用のカラーコード
COLORS = [
    "red", "green", "yellow", "blue", "magenta", "cyan",
    "lightcoral", "lightgreen", "lightyellow",
    "lightblue", "violet", "lightcyan"
]

class Common:
    @staticmethod
    def get_random_colors_list(color_count: int):
        """ ランダムに色を color_count 色選ぶ """
        return random.sample(COLORS, min(color_count, len(COLORS)))
        
    @staticmethod
    def get_divided_lyrics_list(whole_lyrics: str, min_len: int, max_len: int):
        """ 歌詞をランダムな長さで分割 """
        index = 0
        lyrics_len = len(whole_lyrics)
        divided_lyrics_list = []
        
        while index < lyrics_len:
            count = random.randint(min_len, max_len)
            count = min(count, lyrics_len - index)
            part_text = whole_lyrics[index: index + count]
            index += count
            divided_lyrics_list.append(part_text)

        return divided_lyrics_list

    @staticmethod
    def get_colored_lyrics(file_path: str, player_count: int, consecutive_limit: int):
        """ 歌詞をランダム分割し、パートにランダムに色を割り当て、表示 """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lyrics = file.read()
            
            divided_lyrics = Common.get_divided_lyrics_list(lyrics, 4, 8)
            part_list = Common.role_assignment(divided_lyrics, player_count, consecutive_limit)
            # print(f"lyrics:\n{lyrics}\ndivided_lyrics:\n{divided_lyrics}\n")

            # HTML形式に変換
            return "".join([f'<span style="color: {part.color}">{part.text}</span>' for part in part_list])

        except FileNotFoundError:
            return "ファイルが見つかりません"
        except Exception as e:
            return f"エラー: {str(e)}"

    @staticmethod
    def role_assignment(divided_lyrics: list, player_count: int, consecutive_limit: int):
        """ 分割された歌詞(パート)に色を割り当て """
        part_list = []
        current_color = None
        repeat_count = 0
        colors = Common.get_random_colors_list(player_count)

        for part_text in divided_lyrics:
            color = random.choice(colors)
            if repeat_count >= consecutive_limit or current_color is None:
                while color == current_color:
                    color = random.choice(colors)
                current_color = color
                repeat_count = 1
            else:
                repeat_count += 1

            part_list.append(Part(part_text, color))

        return part_list
