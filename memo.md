## yfinance

---

- yfinance で start,end を指定してイントラデイデータを取得すると一部欠損が生じた
  - 原因は正確には不明
  - yfinance は start と end を unix time に変換して API に渡している、その辺が上手く行っていない？
  - もしかしたらローソクの間隔とピッタリ合うように start,end を指定したりしないといけない？？
  - yfinance は多分与えた%Y-%m-%d 型の str を UTC で unix time に変換してる
    - EST の必要な時間まで取得しているか注意が必要
- yfinance というか api 側がうまく扱えていないかも
- **結論**<div style="color:red">イントラデイでは start,end を使用しない</div>

---

## 修正記録

- python anywhere 環境は UTC で動いている見たい、日付の取り扱いを変更
