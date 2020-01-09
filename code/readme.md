## For generate `index.txt`
* Install Porter stemmer:`pip install stemming==1.0`
* Please download `trec.5000.xml`, [englishST.txt](http://members.unine.ch/jacques.savoy/clef/englishST.txt) into `code` directory. 
* Please use command to run the code: `python index.py > index.txt` 
* The `index.txt` will created in `code` 

## For generate `results.boolean.txt`
* Please download `queries.boolean.txt` into `code`
* `queries.boolean.txt` for boolean search, in the following format:  
```
1 term1 AND term1         
2 "term1 term2"           
3 #10(term1, term2)
```
* Run:`python search.py`
* The `results.boolean.txt` will created in `code`

## For generate `results.ranked.txt`
* Please download `queries.ranked.txt` into `code`
* `queries.ranked.txt` for ranked search based TFIDF, in the following format:  
```
1 term1 term1 term3 term4         
```
* Run:`python rank.py`
* The `results.ranked.txt` will created in `code`
* In `main()` model, change function `rank_in_or()` into `rank_in_and()` will get `results.ranked.and.txt`

*******************

