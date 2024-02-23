# MK8DX-AutoWarRecordSender
Sorry, README.md and program comment out is all Japanese program...

This bot support English !

## 概要
このBotはMK8DXの150ccラウンジで行われる模擬やSQの戦績が更新された際にDiscordに通知を出すBotです。

## Special Thanks!!
※敬称略

* 星尾ながる☄️⛈️ → アイディアをもらった上で、作らせていただきました！

  Twitter：[https://twitter.com/Nagaru_ST7](https://twitter.com/Nagaru_ST7)

* ふゆねこ さん → 相談にのっていただきました！ありがとうございます！🙇🏻՞

  Twitter：[https://twitter.com/wintercatmk8dx](https://twitter.com/wintercatmk8dx)

## 招待URL
* [Invite](https://discord.com/api/oauth2/authorize?client_id=1100466211403333694&permissions=8&scope=bot%20applications.commands)

## Download
* [Download Link](https://github.com/Ay2416/MK8DX-AutoWarRecordSender/archive/refs/heads/main.zip)

## 注意
* このbotには<!--Discrod api-->とMK8DX 150ccラウンジのサイト（[https://www.mk8dx-lounge.com/](https://www.mk8dx-lounge.com/)）のapiを使用しています。そのため、main.pyの19行目の値をいじることで更新間隔を短くしたりすることができますが、あまりにも小さくし過ぎるとapiサーバーに負荷をかけすぎてしまう可能性があるため、そこに注意してご使用していただけると幸いです。

~~* そして今回Botをホストしない理由として、あまり１つのBotに人数が偏ってしまうと処理が集中し、apiのサーバーへ負荷をかけてしまうのではないかという懸念があるからです。（現在の自分の技量ではどうしたら良いかわからなかったのもあります。）~~

→色々な方に確認をしたため、英語対応をさせた上で公開しました！

## 使い方（Discord上）
下記のスラッシュコマンドを使用して使うことができます。

* /send add
  * [ラウンジ名]
  * [投稿チャンネル（「#○○○」の形）]]
  * [通常メンションの有無（on/off）]
  * [ランクアップ通知の有無（on/off）]
  * [ランクアップ通知のメンションの有無（on/off）] → 戦績を送信するプレイヤーを追加します。

* /send delete [ラウンジ名] → 戦績を送信するプレイヤーの削除を行います。

* /send list → 戦績を送信する登録があるプレイヤーの一覧を表示します。

* /help → このBotのコマンドの簡単な使い方を出します。

# ↓ここから先はプログラムについての話になります↓

## 動作確認済み環境
* Ubuntu 20.04

python 3.8.16

* Windows11

python 3.10.11

## 使い方（プログラムの動作のさせ方）
※DiscordのBotの作成やトークンの取得はできている前提で説明させていただきます。

※Botをプログラム側で起動できたことが確認できるまで、サーバーへBotの招待を行わないでください。
* これは、英語対応をさせた時にサーバーの入退出でそれを判定するファイルが生成される仕様にしたためです。
そのため、先にBotが起動していない状態でサーバーへ招待を行うとコマンドの仕様ができません。
申し訳ないです。

1. 最初にPythonをインストールしてください。（導入済みの方は飛ばしていただいて結構です。）

※もしかしたら導入済みの可能性もありますので、Windowsの場合はコマンドプロンプト、Linuxの場合はターミナルで「python --version」と打ち、「Python 〇.〇.〇」みたいな表記がでれば導入されているかが確認できます。
* Windows：[Link](https://www.javadrive.jp/python/install/index1.html)

* Linux(Ubuntu)：[Link](https://self-development.info/ubuntu%E3%81%AB%E6%9C%80%E6%96%B0%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E3%81%AEpython%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB%E3%81%99%E3%82%8B/)

2. 次にこのページの１番上の方にある、「Download」を押して、「MK8DX-AutoWarRecordSender-main.zip」をダウンロードします。（Linuxでターミナルで行っている場合はwget等を使用して、ダウンロードしてください。）

3. そしてそのファイルを解凍し、「.env」をテキストエディタで開き、「your_discord_bot_token」という部分にDiscordのBotトークンを入れてください。

  ※「.env」が見えない場合、隠しファイル扱いとなっている可能性が高いため、下記を参考に表示できるようにしてください。

* Windows10：[Link](https://pc-karuma.net/windows-10-show-hidden-files-folders/)

* Windows11：[Link](https://www.fmworld.net/cs/azbyclub/qanavi/jsp/qacontents.jsp?PID=8511-2971)

* Linux(Ubuntu かつ デスクトップ画面からの操作の場合)：[Link](https://linuxfan.info/show-hidden-files-in-nautilus#toc_id_3)

4. コマンドプロンプトまたは、ターミナルで「main.py」があるディレクトリまで移動し、「pip install -r requirements.txt
」を打ってから、「python main.py」と打つことでプログラムを開始し、使用することが可能になります。

※ディレクトリの移動方法

* Windowsの場合は簡単な操作でそのディレクトリからコマンドプロンプトを起動する方法があります。 → [Link](https://qiita.com/windows222/items/2ac133a244f4a9527022)

* Linux(Ubuntu)の場合：[Link](https://uxmilk.jp/27431)（簡単に行けそうな方法を見つけようとしたのですが、自分の力では見つけることができませんでした...。）


### Botを作成する際、必要となる権限は以下の通りです。
~~* Read Messages/View Channels~~

~~* Send Messages~~

~~* Embed Links~~

* 通知のメッセージを送信する際に、設定された投稿先のチャンネルを全て標準で見えるようにするためAdministratorを標準の権限にすることにしました！

## ライセンス
MIT LICENCE↓

[https://github.com/Ay2416/MK8DX-AutoWarRecordSender/blob/main/LICENSE](https://github.com/Ay2416/MK8DX-AutoWarRecordSender/blob/main/LICENSE)

## 利用させていただいたライブラリ
* discord.py：[https://github.com/Rapptz/discord.py](https://github.com/Rapptz/discord.py)

* python-dotenv：[https://pypi.org/project/python-dotenv/](https://pypi.org/project/python-dotenv/)

* ndjson：[https://pypi.org/project/ndjson/](https://pypi.org/project/ndjson/)

* python-dateutil：[https://pypi.org/project/python-dateutil/](https://pypi.org/project/python-dateutil/)

* requests：[https://pypi.org/project/requests/](https://pypi.org/project/requests/)

* glob：[https://pypi.org/project/glob2/](https://pypi.org/project/glob2/)

## 参考にさせていただいたサイト
* PythonでAPIを呼び出すサンプルプログラムをご紹介：[https://rainbow-engine.com/python-api-call-sample/](https://rainbow-engine.com/python-api-call-sample/)

* 図解！PythonのRequestsを徹底解説！(インストール・使い方)：[https://ai-inter1.com/python-requests/](https://ai-inter1.com/python-requests/)

* Pythonのrequestsを利用してRest API(json形式)でファイルダウンロードする方法：[https://qiita.com/5zm/items/d62df0e7b1d98348f983](https://qiita.com/5zm/items/d62df0e7b1d98348f983)

* Pythonでファイル名・ディレクトリ名の一覧をリストで取得：[https://note.nkmk.me/python-listdir-isfile-isdir/](https://note.nkmk.me/python-listdir-isfile-isdir/)

* Pythonでディレクトリ（フォルダ）を作成するmkdir, makedirs：[https://note.nkmk.me/python-os-mkdir-makedirs/](https://note.nkmk.me/python-os-mkdir-makedirs/)

* Pythonでパス文字列からファイル名・フォルダ名・拡張子を取得、結合：[https://note.nkmk.me/python-os-basename-dirname-split-splitext/](https://note.nkmk.me/python-os-basename-dirname-split-splitext/)

* 【discord bot】タスクを使って処理を定期実行する：[https://tenomeuonome.hateblo.jp/entry/2022/11/27/230409](https://tenomeuonome.hateblo.jp/entry/2022/11/27/230409)

* discord.pyでbotに一定時間ごとに発言させる【async版】 ：[https://qiita.com/rareshana/items/76d9c9d0fa68ec242d13](https://qiita.com/rareshana/items/76d9c9d0fa68ec242d13)

* 「分かりそう」で「分からない」でも「分かった」気になれるIT用語辞典-UNIX時間（ユニックス時間）：[https://wa3.i-3-i.info/word18474.html](https://wa3.i-3-i.info/word18474.html)

* 【python】rangeやリストのfor文を逆順に回す方法：[https://kuma-server.com/python-for-reversed/](https://kuma-server.com/python-for-reversed/)

* [Python]for文のrange()を逆順にするには？：[https://www.choge-blog.com/programming/pythonforstatetmenetreverseorder/](https://www.choge-blog.com/programming/pythonforstatetmenetreverseorder/)

* python for文を初心者向けに解説！for文基礎はこれで完璧：[https://udemy.benesse.co.jp/development/python-work/python-for.html](https://udemy.benesse.co.jp/development/python-work/python-for.html)

* Discord Embed Editor：[https://cog-creators.github.io/discord-embed-sandbox/](https://cog-creators.github.io/discord-embed-sandbox/)

* Discord.pyでEmbedを扱う(メモ)：[https://qiita.com/Poteto143/items/bbc61d3adf9b6b72f75f](https://qiita.com/Poteto143/items/bbc61d3adf9b6b72f75f)

* 初心者に捧ぐDiscordのEmbed入門：[https://qiita.com/hisuie08/items/5b63924156080694fc81](https://qiita.com/hisuie08/items/5b63924156080694fc81)

* Pythonで文字列を抽出（位置・文字数、正規表現）：[https://note.nkmk.me/python-str-extract/](https://note.nkmk.me/python-str-extract/)

* Python で JSON 書き込みをする：[https://shikaku-mafia.com/python-json-write/](https://shikaku-mafia.com/python-json-write/)

* PythonのTypeError: list indices must be integers or slices, not strは何ですか？：[https://blog.pyq.jp/entry/2017/08/03/100000](https://blog.pyq.jp/entry/2017/08/03/100000)

* 【Python】’method’ object is not subscriptable エラー対処方法：[https://kirinote.com/python-method-error/](https://kirinote.com/python-method-error/)

* Pythonで数字の文字列strを数値int, floatに変換：[https://note.nkmk.me/python-str-num-conversion/](https://note.nkmk.me/python-str-num-conversion/)

* ［解決！Python］if文にand／or演算子を使って複数の条件を記述するには」：[https://atmarkit.itmedia.co.jp/ait/articles/2205/17/news023.html](https://atmarkit.itmedia.co.jp/ait/articles/2205/17/news023.html)

* discord.py V2のスラッシュコマンドを使えるようにする：[https://qiita.com/Luapy/items/3abff9575e132e2955ec](https://qiita.com/Luapy/items/3abff9575e132e2955ec)

* discord.pyでスラッシュコマンドを実装する。：[https://qiita.com/beatbox4108/items/0d28619bb49e86f58ace](https://qiita.com/beatbox4108/items/0d28619bb49e86f58ace)

* discord.py APIリファレンス - await fetch_user()：[https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel](https://discordpy.readthedocs.io/ja/latest/api.html#discord.Client.fetch_channel)

* Pythonの例外処理！try-exceptをわかりやすく解説！：[https://www.sejuku.net/blog/23044](https://www.sejuku.net/blog/23044)
