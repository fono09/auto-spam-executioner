from mastodon import Mastodon, StreamListener
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime, timezone, timedelta
from time import sleep
import os
import time
import urllib.error
import urllib.request
import asyncio

# .envの読み込み
load_dotenv()
pprint(os.environ)

# Mastodonのクライアント生成
client = Mastodon(api_base_url = os.environ['API_BASE_URL'], access_token = os.environ['ACCESS_TOKEN'])

# 連合タイムラインをListenするためのクラスを定義
class PublicStreamListener(StreamListener):

    # 引数に生成したMastodonのクライアントが必須
    def __init__(self, client):
        super(PublicStreamListener, self).__init__()
        self.client = client

    def handle_stream(self, response):
        try:
            super().handle_stream(response)
        except:
            pass

    def on_update(self, status):
        print(f"status recieved: {status.id}")
        try:
            # メンション数が規定数より多く、かつ外部からの投稿の場合
            if len(status.mentions) > int(os.environ['MEMTION_COUNT']) and status.account.acct.find('@') > 0:
                statusID = status.id
                account = status.account
                pprint(status)

                # 作成から7日以上経過したアカウントは対象としない
                if account.created_at - datetime.now(timezone.utc) > timedelta(days=7):
                    return

                # フォロワー数を数え、規定数より多い場合は対象としない
                if account.following_count > int(os.environ['FOLLOWER_COUNT']):
                    return

                # スパムの通報(リモートサーバにも転送)を投げ、アカウントを停止させる
                report = self.client.report(
                    account.id,
                    status_ids=[statusID],
                    forward=True,
                    category='spam'
                )
                pprint(report)

                # レプリケーション遅延を考慮する
                sleep(1)

                # アカウントの停止
                self.client.admin_account_moderate(
                    account.id,
                    action='suspend',
                    report_id=report.id,
                    send_email_notification=False
                )


        except Exception as e:
            pprint(e)
            pass

# 連合タイムラインのListenerを生成            
public_stream_listener = PublicStreamListener(client)

# 連合タイムラインをListen
while True:
    client.stream_public(public_stream_listener, remote=True)
    print("restart litening client.stream_public")
    sleep(10)
