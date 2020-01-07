# ブックカレンダー
## 概要
本アプリケーションは、いくつかの出版社の新刊情報を自動で収集し、タイトルや著者、発売日などの情報を一覧にして表示するものです。ユーザー登録をすることもでき、その場合は、ユーザーが設定するキーワードとeメール通知日に基づいて新刊情報をeメールで通知します。

## アプリケーションURL
https://books-date.herokuapp.com/

## テストアカウント
メールアドレス：test@mail.com

パスワード：12rt34jk

## 工夫したポイント
- キーワード登録に際しては、その新規登録、更新、削除を逐一ページを切り替えなくてもできるように、非同期通信で行うようにしました。また、キーワード削除時は、削除するためのボタンが設置されていますが、それとは別に、キーワード更新フォームを空にした状態で更新ボタンを押す事によってもキーワードを削除できるようにしました。


- キーワードに半角、全角のスペースも含めると、スペースと、スペースを含む本のタイトルなどが合致してしまい、検索として意味をなさなくなってしまうので、キーワード登録時にスペースは自動的に消されるようにしました。また、本の情報の自動収集に失敗した部分については<取得失敗>と登録されるようになっていますが、これが検索に引っかからないようにしました。


- eメールは、自動収集した本のタイトルまたは著者名に対してユーザーが登録したキーワードが部分一致し、かつその本の発売日がユーザーが登録したeメール通知日の条件を満たしている場合に送られるようになっています。このキーワードと本の情報の照らし合わせ、それに基づくメールの送信は、毎日午前８時に行うように設定しています。このとき、複数のキーワードが1つの本に合致した場合に重複して本の情報を送らないようにしました。また、eメール送信判定は毎日行われますが、一度送った本の情報が繰り返し送られる事がないようにしました。


- 本アプリケーションでは本の情報の自動収集（スクレイピング）やeメールの送信など、エラーが発生しやすい動作を行っていますが、もしそれらに失敗してもプログラム自体が止まらないような工夫を行いました。スクレイピングに関しては、収集した本の情報はデータベースに保存されるのですが、この時データベースのいくつかのカラムにNull値を入れようとするとエラーが起きてしまうので、もしスクレイピングに失敗した場合には、そのカラムに<取得失敗>という文字列を入れる事でエラーを防ぎます。eメールに関しても、ユーザーが有効でないメールアドレスを入力するなどが原因で送信に失敗する可能性があるので、例外処理のコードを用いて、送信が失敗してもプログラムが止まらないようにしています。

## 使用技術
- Python, フレームワーク(Django)
- html, css(sass), javascript(jQuery)
- スクレイピング(BeautifulSoup), メール送信(SendGrid)
- github
- デプロイ(heroku), herokuのCustom clock processを使ったjobの定期実行

## 今後実装していきたい機能
- <機械学習を使った本の情報の自動収集>  
現状、本アプリケーションで本の情報の収集対象になっている出版社は２社のみです。スクレイピングは収集先のwebページの構造に合わせてコードを書く必要があるので、多数の出版社(webページ)から情報を収集しようとするとそれぞれに対応した別個のコードを書かなければなりません。それでは対応できる出版社の数にも限度がありますし、出版社がwebページの構造を変更したら、その度にこちらもコードを書き直す必要が出てきます。  
そこで、機械学習を用いて、出版社のwebページの画像情報から、新刊の情報を自動的に抽出できるようにしたいと思っています。


- <新刊情報のSNSを使った通知>  
LineやtwitterなどのSNSを介して新刊情報の通知を行えるようにしようと思っています。
