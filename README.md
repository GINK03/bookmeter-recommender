# 

## ユーザ行動時系列を意識したskip gram

## 期待される結果
- 流行があり、時代によってある本が読まれやすい場合、同じ時代に同じ本の流れで、読まれやすい本のタイトルの抽出
- 本のコンテンツの類似度ではなく、同じような本を読む人が同じ時代にどういった方も、また、読んでいたかという解釈
- 時系列的な影響を考慮した協調フィルタリングのようなものとして働くと期待できる

## 学習アルゴリズム
- fasttext
- skipgram
- 512次元
- n-chargramは無効化

## 定性的な結果

## 参考
[1] [Instacart Product2Vec & Clustering Using word2vec](https://www.kaggle.com/goodvc/instacart-product2vec-clustering-using-word2vec)  
[2] [MRNet-Product2Vec: A Multi-task Recurrent Neural Network for Product Embeddings](https://arxiv.org/pdf/1709.07534.pdf)  
[3] [Deep Learning at AWS: Embedding & Attention Models](https://www.slideshare.net/AmazonWebServices/deep-learning-at-aws-embedding-attention-models)
