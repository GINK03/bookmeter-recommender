# 以下の三つのレコメンド系アルゴリズムを使ってみたいと思います
1. userベースの協調フィルタリング
2. fasttextでのアイテムベースのproduct2vec(skipgram)

# 1. userベースの協調フィルタリング
協調フィルタリング自体は簡潔なアルゴリズムで、実装しようと思えば、簡単にできる類のものであるように思えるのですが、製品と製品の類似度を計算するのに、その製品を購入したユーザをベクトル列としてみなすと割と簡単に計算できることがわかりました  

例えば、今回はbookmeter.comさまのユーザの読んだ本情報を用いて、一人のユーザを一つの特徴量としてみなすことで、本同士の関連度が計算可能になります  

Albertさんなどのブログなどを参考し、今回の問題に当てはめると、このようなことであると言えそうです。  

<p align="center">
  <img width="700px" src="https://user-images.githubusercontent.com/4949982/33258093-c83903ca-d39b-11e7-8c4d-0ca9622f6d91.png">
</p>
<div align="center"> 図1. 今回用いた協調フィルタリング </div>

今回用いさせていただいた、bookmeter.comさんから作成したデータセットは[こちら](https://storage.googleapis.com/nardtree/bookmeter-scraping-20171127/htmls.tar.gz)です。27GByte程度あるので、覚悟してダウンロードしてください  

また、必要なユーザと読んだ本とその時のタイムスタンプの情報のみをまとめたものは、[こちら](https://storage.googleapis.com/nardtree/bookmeter-scraping-20171127/mapped.jsonp)からダウンロードできます。  

## 結果.
**氷菓(1)(角川コミックス・エース)**との類似度  
当然、その本地身とシリーズが出て欲しいのですが、例えば、コミック版氷菓を読むユーザは、「我妻さんは俺のヨメ」シリーズも読むことがわかりました。  
氷菓が好きな人は、このシリーズもきっとおすすめです
```console
氷菓(1)(角川コミックス・エース) 1.0
氷菓(3)(角川コミックス・エース) 0.6324555320336759
氷菓(2)(角川コミックス・エース) 0.565685424949238
氷菓(4)(角川コミックス・エース) 0.5477225575051661
氷菓(5)(角川コミックス・エース) 0.4743416490252569
我妻さんは俺のヨメ（８） 0.4472135954999579
キン肉マン60(ジャンプコミックスDIG… 0.4472135954999579
弱虫ペダル　51(少年チャンピオン・コミッ… 0.4472135954999579
魔法遣いに大切なこと～夏のソラ～(1)(角… 0.4472135954999579
人生はまだ長いので(FEELCOMICS… 0.4472135954999579
キン肉マン59(ジャンプコミックスDIG… 0.4472135954999579
お前はまだグンマを知らない　1巻(バンチコ… 0.4472135954999579
我妻さんは俺のヨメ（５） 0.4472135954999579
トリニティセブン　７人の魔書使い(1)(ド… 0.4472135954999579
このお姉さんはフィクションです！？：4… 0.4472135954999579
我妻さんは俺のヨメ（６）(週刊少年マガジン… 0.4472135954999579
ナナマルサンバツ(7)(角川コミックス・… 0.4472135954999579
夏の前日（４） 0.4472135954999579
我妻さんは俺のヨメ（９）(週刊少年マガジン… 0.4472135954999579
お前はまだグンマを知らない　2巻(バンチコ… 0.4472135954999579
塩田先生と雨井ちゃん２ 0.4472135954999579
```

# 2. fasttextでのアイテムベースのproduct2vec(skipgram)

一部でproduct2vecと呼ばれる技術のようですが、同名のRNNを用いた方法も提案されており、何が何だかわからないですが、購買鼓動を一連の時系列として文章のように捉えることで、似た購買行動をするユーザの購買製品が似たようなベクトルになるという、大まかな筋道と仮説があります  

今までスクレイピングがまともにできなかったサイト様に関して、いくつかできるようになったという背景があり、bookmeter様のサイトをスクレイピングして、データを集めさせていただきました  

## 期待される結果
- 流行があり、時代によってある本が読まれやすい場合、同じ時代に同じ本の流れで、読まれやすい本のタイトルの抽出
- 本のコンテンツの類似度ではなく、同じような本を読む人が同じ時代にどういった方も、また読んでいたか、という解釈
- 時系列的な影響を考慮した協調フィルタリングのようなものとして働くと期待できる

## 学習アルゴリズム
- fasttext
- skipgram
- 512次元
- n-chargramは無効化

## 前処理
bookmeterさんからスクレイピンしたデータからユーザ名とIDで読んだ本を時系列順に紐づけます
```console
$ python3 parse_user_book.py --map1
$ python3 parse_user_book.py --fold1
```
bookmeterさんのデータをpythonで扱うデータ型に変換します
```console
$ python3 reduce.py --fold1
$ python3 reduce.py --label1 > recoomender-fasttext/dump.jsonp
```
fasttext(skipgramを今回計算するソフト)で処理できる形式に変換します
```console
$ cd recoomender-fasttext
$ python3 mkdataset.py
```
## SkipGramでベクトル化と、本ごとのcosime similarityの計算
```console
$ sh run.sh
$ python3 ranking.py --to_vec
$ mkdir sims
$ python3 ranking.py --sim
```


## 定性的な結果
1. 近年、本は大量に出版されて、その時に応じて売れ行きなどが変化するため、その時代に同じような本を買う傾向がある人が同じような買うというプロセスで似た傾向の本を買うと家庭ができそうである  
2. 本は、趣味嗜好の内容が似ている系列で似る傾向があり、コンテンツの内容では評価されない  

以上の視点を持ちながら、私が知っている書籍では理解しやすいので、いくつかピックアップした  

**聖☆おにいさん(11)(モーニングKC)** と同じような購買の行動で登場する本
```json
聖☆おにいさん(11)(モーニングKC) 聖☆おにいさん(11)(モーニングKC) 1.0 
聖☆おにいさん(11)(モーニングKC) 富士山さんは思春期(1)(アクションコミッ… 0.8972133709829763
聖☆おにいさん(11)(モーニングKC) 血界戦線4―拳客のエデン―(ジャンプコ… 0.8880415759167462
聖☆おにいさん(11)(モーニングKC) 闇の守り人2(Nemuki+コミックス) 0.874690584963135
聖☆おにいさん(11)(モーニングKC) 高台家の人々1(マーガレットコミックス) 0.8739713568492584
聖☆おにいさん(11)(モーニングKC) よりぬき青春鉄道(MFコミックスジーンシ… 0.8654563200372407
聖☆おにいさん(11)(モーニングKC) MUJIN―無尽―2巻(コミック(Y… 0.864354621889988
聖☆おにいさん(11)(モーニングKC) 日日べんとう8(オフィスユーコミックス) 0.8642825499104115
聖☆おにいさん(11)(モーニングKC) Baby,ココロのママに!(1)(ポラリ… 0.8633512045595658
聖☆おにいさん(11)(モーニングKC) 僕とおじいちゃんと魔法の塔（１）(怪CO… 0.8599349055581674
```

**ボールルームへようこそ(5)** と同じような購買の行動で登場する本
```json
ボールルームへようこそ(5)(講談社コミッ… ボールルームへようこそ(5)(講談社コミッ… 0.9999999999999999
ボールルームへようこそ(5)(講談社コミッ… 乙女座・スピカ・真珠星―タカハシマコ短編集… 0.9209695753657776
ボールルームへようこそ(5)(講談社コミッ… 微熱×発熱(少コミフラワーコミックス) 0.9200136951145198
ボールルームへようこそ(5)(講談社コミッ… 銀魂-ぎんたま-52(ジャンプコミックス) 0.9192139559710213
ボールルームへようこそ(5)(講談社コミッ… ボールルームへようこそ(3)(講談社コミッ… 0.9185994617714857
ボールルームへようこそ(5)(講談社コミッ… リメイク5(マッグガーデンコミックスE… 0.9178462840921753
ボールルームへようこそ(5)(講談社コミッ… カラダ探し2(ジャンプコミックス) 0.9133800737256051
ボールルームへようこそ(5)(講談社コミッ… エンジェル・ハート1STシーズン4(ゼノ… 0.9131301530550904
ボールルームへようこそ(5)(講談社コミッ… モテないし・・・そうだ、執事を召喚しよう。… 0.912900126682059
ボールルームへようこそ(5)(講談社コミッ… IPPO1(ヤングジャンプコミックス) 0.9127181876031607
```

**バーナード嬢曰く。(REXコミックス)** と同じような購買の行動で登場する本
```json
バーナード嬢曰く。(REXコミックス) バーナード嬢曰く。(REXコミックス) 0.9999999999999999
バーナード嬢曰く。(REXコミックス) 宝石の国(7)(アフタヌーンKC) 0.8471396900305308
バーナード嬢曰く。(REXコミックス) 宝石の国(5)(アフタヌーンKC) 0.8382072129764407
バーナード嬢曰く。(REXコミックス) 里山奇談 0.816403634050381
バーナード嬢曰く。(REXコミックス) ファイブスター物語(12)(ニュータイプ… 0.8158735339937038
バーナード嬢曰く。(REXコミックス) 汐の声(山岸凉子スペシャルセレクション2) 0.813237955152229
バーナード嬢曰く。(REXコミックス) ゴールデンカムイ5(ヤングジャンプコミッ… 0.8124194507560973
バーナード嬢曰く。(REXコミックス) サンドマン(1)(DCCOMICSV… 0.8063562786141018
バーナード嬢曰く。(REXコミックス) ナチュン(5)(アフタヌーンKC) 0.8062792077739434
バーナード嬢曰く。(REXコミックス) めぞん一刻15(ビッグコミックス) 0.8050153883069142
```

34万冊にも及ぶ購買行動関連スコアを計算したので、きっとあなたの好きな本を広げるにも役に立つはずです。参考にしていただければ幸いです  

## 読んでる人が多い本ランキング
読んでる人が多い本(2017年11月時点)
```json
永遠の0(講談社文庫) 6805
ビブリア古書堂の事件手帖―栞子さんと奇妙な客… 6551
舟を編む 6500
イニシエーション・ラブ(文春文庫) 6158
火花 5988
阪急電車(幻冬舎文庫) 5979
夜は短し歩けよ乙女(角川文庫) 5964
君の膵臓をたべたい 5504
コンビニ人間 5134
ビブリア古書堂の事件手帖2栞子さんと謎め… 5075
レインツリーの国(新潮文庫) 4994
その女アレックス(文春文庫) 4792
ぼくは明日、昨日のきみとデートする(宝島社… 4631
氷菓(角川文庫) 4606
ビブリア古書堂の事件手帖3~栞子さんと消え… 4590
```
6ヶ月以上、連続で本を読んでいる人の読んでる本ランキング
```json
1 舟を編む 5419 
1 永遠の0(講談社文庫) 5296
1 ビブリア古書堂の事件手帖―栞子さんと奇妙な客… 5277
1 火花 5081 
1 イニシエーション・ラブ(文春文庫) 4784
1 阪急電車(幻冬舎文庫) 4570
1 夜は短し歩けよ乙女(角川文庫) 4427
1 君の膵臓をたべたい 4422
1 コンビニ人間 4225
1 その女アレックス(文春文庫) 4186
```
6ヶ月間、連続で本を読むことができなかった人の読んでる本ランキング
```json
0 夜は短し歩けよ乙女(角川文庫) 1537
0 永遠の0(講談社文庫) 1509
0 阪急電車(幻冬舎文庫) 1409
0 イニシエーション・ラブ(文春文庫) 1374
0 ビブリア古書堂の事件手帖―栞子さんと奇妙な客… 1274
0 ぼくは明日、昨日のきみとデートする(宝島社… 1143
0 レインツリーの国(新潮文庫) 1120
0 君の膵臓をたべたい 1082
0 舟を編む 1081
0 西の魔女が死んだ(新潮文庫) 1004
```

## 参考
[1] [Instacart Product2Vec & Clustering Using word2vec](https://www.kaggle.com/goodvc/instacart-product2vec-clustering-using-word2vec)  
[2] [MRNet-Product2Vec: A Multi-task Recurrent Neural Network for Product Embeddings](https://arxiv.org/pdf/1709.07534.pdf)  
[3] [Deep Learning at AWS: Embedding & Attention Models](https://www.slideshare.net/AmazonWebServices/deep-learning-at-aws-embedding-attention-models)
