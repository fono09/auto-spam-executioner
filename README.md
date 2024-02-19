# MastodonのStreamingAPIでリアルタイムでスパムを処すやつ

## License

[AGPL License](https://opensource.org/licenses/AGPL).

## Original Author

[rosylilly](https://github.com/rosylilly)

## Original Code

[S-H-GAMELINKS/auto-spam-executioner](https://github.com/S-H-GAMELINKS/auto-spam-executioner)

[Reject spammer](https://github.com/best-friends/mastodon/pull/1941)

[mastodon/mastodon](https://github.com/mastodon/mastodon)

## 使い方

APIキーの権限は下記があれば十分です
(adminが必要なのでチェックを忘れないように。怖ければ適当に削ってください)
`read, write, admin:read, admin:write`

`cp .env.sample .env` として、`.env` を編集してください
