# あつたまちゃんのおはらじお

![あつたまちゃんのおはらじお](logo-wide.svg)

にじさんじ・VTuberの公式ニュースを紹介する、おためしWebラジオです。

- 公開先：https://namako4696.github.io/myradio/
- 現在は**手動試運転**モードです。自動ニュース取得・定期更新・有料APIは使いません
- 言語は日本語のみです
- ニュースは公式発表・一次情報に基づき、出典URLを各回に付けます。非公式な噂は扱いません
- 初回の台本・音声が用意できるまでは、番組一覧は空です（プレーヤーは開けます）

## キャスター：あつたまちゃん

キャスターは「あつやきたまごちゃん」（原案：なまこ）です。今回はMuse版の3D風ポーズ画像を使っています。

- **目・口は描かれていません。口パク・まばたきもしません**
- 感情は全身ポーズの切り替えで表します。通常＝座りポーズ／挨拶＝手を振る／強調＝ガッツポーズ／終わり＝お辞儀、など8ポーズ
- ポーズは番組の進行（オープニング・ニュース・エンディング）に合わせて自動で切り替わります。カメラ左下のボタンでも手動で切り替えられます（手動で選ぶと約8秒そのポーズのままになります）
- 画像は白背景の切り出しを透過化したもので、生成し直すときは `python3 tools/make_pose_images.py <切り出しフォルダ> character/poses` を使います

ポーズ方式はこの局で追加した `"type": "poses"` のキャラパックです。形式は [docs/formats.md](docs/formats.md) の「poses」の節を見てください。元の口・目差分方式（sprites）と動画方式（clips）もプレーヤーに残してあります。

## 試運転の進め方（手動）

1. **台本を作る**：公式情報から台本JSONを作り、`episodes/<YYYY-MM-DD>-ja.json` に置いて、`episodes.json` の一覧（新しい順）にその回の題と長さを足します。形は [docs/formats.md](docs/formats.md)。事実とURLは創作せず、実在を確認した出典だけを使います
2. **声を作る**：利用規約を確認した無料の音声合成でMP3を作り、`audio/<YYYY-MM-DD>-ja.mp3` に置きます（音声はmainにコミットしません）。台本の `lines_timed` と `segments` を音声のタイミングに合わせ、使用した声のクレジットを `station.json` の `credits`（「声：未定」の行）に書きます
3. **公開する**：`tools/publish.sh` を実行して `gh-pages` ブランチへ出し、リポジトリの Settings → Pages で配信元を `gh-pages` / (root) に設定します

## 中身

```
station.json          局の自己紹介（名前・内容・ロゴ・クレジット）
index.html            プレーヤー
episodes.json         回の一覧（現在は空）
episodes/             台本JSONを置く場所
audio/                声（mainにはコミットしない。publish.shが直近30日分だけgh-pagesに載せる）
character/            キャスター（character.json と、透過済みポーズ画像 poses/）
logo.svg              局のマーク（プレーヤーが黄色のシルエットとして使う形）
logo-wide.svg         横長のロゴ（このREADMEやSNS用）
tools/publish.sh      GitHub Pagesへの公開
tools/share.py        共有カード（ポーズ方式では default のポーズが載る）
tools/make_pose_images.py  ポーズ画像の透過化
docs/formats.md       JSONの形
```

## ライセンス・クレジット

- プログラム（`index.html`、`tools/`）：MIT License。元のプログラムは [monoradio102/myradio](https://github.com/monoradio102/myradio) です
- 台本（`episodes/`、`episodes.json`）：CC0
- キャスター「あつやきたまごちゃん」は なまこ のオリジナルキャラクターです。ポーズ画像はMuse版3D風画像をもとにしています
- 声のクレジットは、試運転で使う音声合成が決まったら `station.json` に明記します
