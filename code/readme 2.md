## To generate S[1-6].eval
* Please use command to run the code: `python EVAL.py`
* To get the S1.eval-S6.eval:
```
1 Change function read_S_results(k): with open("systems/S1.results", 'r', encoding='utf-8') as fin: with `S1.results`
2 Change function read_whole_s_results(): with open("systems/S1.results", 'r', encoding='utf-8') as fin: with `S1.results`
3 Change function write_result():  with open('S1.eval', 'w') as fout: with `S1.eval`
4 Run function write_result() in main() to get the S1.eval as the result
5 Do same step to get S2.eval, S3,eval, S4,eval, S5.eval and S6.eval
```

## For generate `All.eval`
* S1-S6.eval should be generated first.
* Then run write_all_mean() in main() to generate the `All.eval` 
* All the output file should be in a same directory
*******************

