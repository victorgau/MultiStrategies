# 量化投資 - 多策略回測結果比較

[![Build Status](https://travis-ci.org/victorgau/MultiStrategies.svg?branch=master)](https://travis-ci.org/victorgau/MultiStrategies)

這個專案主要在比較多個策略在多張股票上的回測結果，但是這裡我們沒有考慮投資組合的情況。

所有的策略會被寫入 all_strategies.py，然後執行下面的指令產生結果：

```python
python analysis.py
```

結果會以 HTML 檔案的格式被存放在 docs 目錄底下，同時 GitHub 會打開使用 docs 目錄做為專案網頁的模式。

.travis.yml 裡面會撰寫自動化的流程，其中包含環境的架設、分析程式的執行、以及分析結果推回 GitHub 的部份。

* 環境架設的部分，須注意 ta-lib 的安裝的問題。從 ta-lib 的安裝包會出錯，需要使用原始碼安裝。
* 分析結果要推回 GitHub 的部分，也有一些細節需要注意，詳情請參考原始碼。
