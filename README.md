# なにこれ
[SAPPORO OPEN DATA HACK](https://connpass.com/event/298303/)のチームCIeaSTのバックエンドリポジトリです。

# 環境
本体はFastAPI+SQLite3です。

dockerコンテナ上で動かしたい場合は、docker環境を用意してください。
また、makeコマンドも整備しておいたので、dockerを使う場合は[makeコマンドの環境](https://zenn.dev/genki86web/articles/6e61c167fbe926)を作っておくと便利です。

## ファイル分割
- エンドポイントの実装は関心事について分けてください
    - つまり、関心事ごとに`routers`配下に新しくファイルを作って、そこにエンドポイントの実装をしてください
- エンドポイントを増やした場合は増やしたエンドポイントを[スプレッドシート](https://docs.google.com/spreadsheets/d/1p-ekWgXCH7r2whsdslvnZv7JpNiDOHjwrCaEofOoII8/edit?usp=sharing)に明記してください

## テーブルを作るとき
`create table`をするときは`app/migrations`下に`YYYYMMDDHH_hogehoge`の形式でファイルを新しく作成してください

# 進め方
以下の手順を繰り返していく形で進めます。
1. issueをつくる
2. `feature/{issue番号}`の形でブランチを作り、issue分の開発をする
3. `feature/{issue番号}`ブランチをpushする
4. `feature/{issue番号}`ブランチのPull Request(PR)を作成する
5. ほかのメンバーにPRのレビューを依頼する
6. レビューが通ったらマージ

なお、PRのマージ先は原則`develop`ブランチにしてください