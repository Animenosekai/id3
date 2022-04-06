from id3.lyrics import LyricsProvider, Lyrics

DEFAULT = """夢の坂道は　木の葉模様の石畳
まばゆく長い白い壁
足跡も影も残さないで
たどりつけない山の中へ
続いているものなのです

夢の夕陽は　コバルト色の空と海
交わってただ遠い果て
輝いたという記憶だけで
ほんの小さな一番星に
追われて消えるものなのです

背中の夢に浮かぶ小舟に
あなたが今でも手をふるようだ
背中の夢に浮かぶ小舟に
あなたが今でも手をふるようだ

夢の語らいは　小麦色した帰り道
畑の中の戻り道
ウォーターメロンの花の中に
数えきれない長い年月
うたたねをするものなのです

背中の夢に浮かぶ小舟に
あなたが今でも手をふるようだ
背中の夢に浮かぶ小舟に
あなたが今でも手をふるようだ"""


class Manual(LyricsProvider):
    def search(self, query: str) -> str:
        return Lyrics(DEFAULT, "jpn")

    def get(self, track) -> str:
        return Lyrics(DEFAULT, "jpn")
