# CIRKIT-5

CIRKIT所有ロボット5号機のリポジトリ

## 仕様
- 開発環境は ROS Kinetic Kameを推奨
- ハードウェア要件は i-cart mini に準ずるものとする: [公式](http://t-frog.com/products/icart_mini/)

## テスト記録
- 旧ハードについてはROS Indigo にて動作確認済み
- 新ハード(本番用)については後日調査(以降は, Kinetic Kameによって開発を行う)

## 続報20161018
ipアドレスをスタティックに振り分ける必要があるために
 - sudo ifconfig enp7s0 192.168.0.15
 - sudo route add default gw 192.168.0.1
 - rosrun urg\_node urg\_node \_ip\_address:=192.168.0.10

これは kinetic 版についてなので, 14.04で走らせたいときは eth0 / wlan0 と言った名前の振り分けにしてください.



## ソフト構成
- navigation
- gmappping
- yp-spur(公式)
- urg\_node(LRFドライバ)
Note. hokuyo\_node は古くて非推奨なのですが, laserprocなどの必要な部品がkineticにおいて揃っておらず,現行使えないということでhokuyo\_nodeを使うことにしました.
必要なdriverを追加で導入することにしましたので, ひょっとしたらurg\_nodeでも稼働しそうですが, 使ったことのある方を使うようにします.

laserProcが先日のアプデで入りましたので urg\_node を使います. eth がほしいのでこれも.

## 各ノードの提携図  
Updated  10/8

走行モード 
![runnning](https://github.com/CIR-KIT/fifth_robot_pkg/blob/images/images/new_pkgs_drafting20161005.jpg)
 
地図モード 
![mapmaking](https://github.com/CIR-KIT/fifth_robot_pkg/blob/images/images/new_pkgs_drafting20161005-mapmaker.jpg)

## 詳細
- urg\_node
 + subscribing : none
 + publishing  : /Laserscan Sensor\_msgs/Laserscan
- map-saver
 + subscribing : none(reading map bags)
 + publishing  : /map nav\_smgs/Getmap
- yp-spur
 + subscribing : /cmd\_vel geometry\_msgs/twist
 + publishing  : /odom nav-msgs/Odometory
- move\_base
 + subscribing : /Laserscan Sensor\_msgs/Laserscan
 + subscribing : /map nav\_smgs/Getmap
 + subscribing : /odom nav-msgs/Odometory
 + publishing  : /cmd\_vel geometry\_msgs/twist

goal/waypoint提供者を実装する必要があります.

## メモ
- セットアップについて,__yp-spur,ssmのインストール__を忘れずに行ってください: [公式](http://www.roboken.iit.tsukuba.ac.jp/platform/wiki/yp-spur/how-to-install)  
Note : もう必要ないかもしれませんがインストール環境で開発が進んでいます. 使ってない状況での挙動報告は歓迎.  
- contributer を募集しています

Note : モータがなんか変だこれ...極性逆っぽいけれどソフト的に対応してるから注意.(可搬性はないのだ)

## Installation
`git clone` する際に `--recursive` を付ければsubmoduleごと引っ張ってこれます。

catkin workspace のソース内(`src`)にクローンした場合はそのまま。
それ以外のところにクローンした場合は`src`ディレクトリ上で`catkin_init_workspace`を行えばリポジトリをcatkin workspaceにできます。

必要な packeage を確保してください.
筑波大学の公式から
ssm
yp-spur
を,

third\_party内のインストールシェルより
joy
joy\_teleop
navigation

をaptからバイナリで（でかいので)

必要に応じ

tf
urg\_node

apt より バイナリで

そうすれば `catkin_make` が通るはずです。

## 起動
各部接続して,(PC-spur, PC-PS3コン)
roslaunch mapping.launch
これで, path が適切に通っていればドライバ起動・通信開始・入力受付をやってくれます.
困ったことがあるときは 2 回生とかに質問くれてもいいですし, issue 飛ばしてくれることを期待します.
