- [ work2exp](#head1)
	- [Run algorithms **](#head2)
	- [Plot exp **](#head3)
		- [one figure each budget ](#head4)
		- [one figure each epsilon](#head5)
		- [fixied epsilon, vary pricing scheme](#head6)
	- [Plot net](#head7)
		- [curve p(v) and q(v) under different gamma for each dataset](#head8)
		- [distributions of vis deg for each dataset,](#head9)
		- [distributions of p and q under different gamma for each dataset](#head10)
	- [Auto documentation](#head11)
		- [usages table](#head12)
		- [generate doc via sphinx:](#head13)
	- [ Utils](#head14)
		- [clean history pkl](#head15)
		- [extrat content tree](#head16)
	- [ Statements](#head17)
		- [ datasets](#head18)
		- [naming issues with paper](#head19)
# <span id="head1"> work2exp</span>



## <span id="head2">Run algorithms **</span>
```   
python main.py algo -d d1 -bl 1 2 3 4 -g 20 -o rev  -m brute  --gamma 3    
python main.py algo -d d2 -bl 1 2 3   -g 20 -o rev  -m brute  --gamma 3    
python main.py algo -d d4 -bl 1 2     -g 20 -o rev  -m brute  --gamma 3
                                                                 
python main.py algo -d d1 -bl 1 2 3 4 -g 20 -o rev  -m greedy --gamma 3
python main.py algo -d d2 -bl 1 2 3   -g 20 -o rev  -m greedy --gamma 3
python main.py algo -d d4 -bl 1 2     -g 20 -o rev  -m greedy --gamma 3

python main.py algo -d d1 -bl 1 2 3 4 -g 20 -o sw  -m h1 --gamma 1  
python main.py algo -d d2 -bl 1 2 3   -g 20 -o sw  -m h1 --gamma 1  
python main.py algo -d d4 -bl 1 2     -g 20 -o sw  -m h1 --gamma 1  

```


## <span id="head3">Plot exp **</span>

### <span id="head4">one figure each budget </span>

```angular2html
# each dataset generate |bl| figures for revenue  
# '_budget' in plot_from_axisvalue_budget means one figure each budget... 
python main.py pre -d d1 -f plot_from_axisvalue_budget -bl 1 2 3 4 -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 3
python main.py pre -d d2 -f plot_from_axisvalue_budget -bl 1 2 3   -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 3
python main.py pre -d d4 -f plot_from_axisvalue_budget -bl 1 2     -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 3
                                                                                           
# each dataset generate |bl| figures for sw                                                           
python main.py pre -d d1 -f plot_from_axisvalue_budget -bl 1 2 3 4 -o sw -ml brute greedy -gl 5 10 20    --gamma 3
python main.py pre -d d2 -f plot_from_axisvalue_budget -bl 1 2 3   -o sw -ml brute greedy -gl 5 10 20    --gamma 3  
python main.py pre -d d4 -f plot_from_axisvalue_budget -bl 1 2     -o sw -ml brute greedy -gl 5 10 20    --gamma 3


python main.py pre -d d1 -f generate_csv_from_pkl -bl 1 2 3 4 -o sw  -ml brute greedy h1 -g 20
python main.py pre -d d1 -f generate_csv_from_pkl -bl 1 2 3 4 -o rev -ml brute greedy -g 20
```


### <span id="head5">one figure each epsilon</span>

```angular2html                                                                                                       
# each dataset generate |bl| figures for revenue                                                                      
# '_budget' in plot_from_axisvalue_budget means one figure each budget...                                             
python main.py pre -d d1 -f plot_from_axisvalue_epsilon -bl 1 2 3 4 -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 1    
python main.py pre -d d2 -f plot_from_axisvalue_epsilon -bl 1 2 3   -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 1    
python main.py pre -d d4 -f plot_from_axisvalue_epsilon -bl 1 2     -o rev -ml brute greedy h1 -gl 5 10 20   --gamma 1    
                                                                                                                     
# each dataset generate |bl| figures for sw                                                                          
python main.py pre -d d1 -f plot_from_axisvalue_epsilon -bl 1 2 3 4 -o sw -ml brute greedy h1  -gl 5 10 20    --gamma 1    
python main.py pre -d d2 -f plot_from_axisvalue_epsilon -bl 1 2 3   -o sw -ml brute greedy h1  -gl 5 10 20    --gamma 1    
python main.py pre -d d4 -f plot_from_axisvalue_epsilon -bl 1 2     -o sw -ml brute greedy h1  -gl 5 10 20    --gamma 1    
                                                                                                                      
                                                                                                                      
python main.py pre -d d1 -f generate_csv_from_pkl -bl 1 2 3 4 -o sw  -ml brute greedy -g 20                           
python main.py pre -d d1 -f generate_csv_from_pkl -bl 1 2 3 4 -o rev -ml brute greedy -g 20                           
```


### <span id="head6">fixied epsilon, vary pricing scheme</span>

```angular2html
python main.py pre -d d1 -f plot_from_pkl_3d -bl 1 2 3 4  -g 20 -o rev -m greedy     --gamma 2
python main.py pre -d d1 -f plot_from_pkl_3d -bl 1 2 3 4  -g 20 -o rev -m brute      --gamma 2
python main.py pre -d d1 -f plot_from_pkl_3d -bl 1 2 3 4  -g 20 -o sw  -m greedy     --gamma 2
python main.py pre -d d1 -f plot_from_pkl_3d -bl 1 2 3 4  -g 20 -o sw  -m brute      --gamma 2
                                                                                     
python main.py pre -d d2 -f plot_from_pkl_3d -bl 1 2 3  -g 20 -o rev -m greedy       --gamma 3
python main.py pre -d d2 -f plot_from_pkl_3d -bl 1 2 3  -g 20 -o rev -m brute        --gamma 3
python main.py pre -d d2 -f plot_from_pkl_3d -bl 1 2 3  -g 20 -o sw  -m greedy       --gamma 3
python main.py pre -d d2 -f plot_from_pkl_3d -bl 1 2 3  -g 20 -o sw  -m brute        --gamma 3
                                                                                     
python main.py pre -d d4 -f plot_from_pkl_3d -bl 1 2   -g 20 -o rev -m greedy        --gamma 3
python main.py pre -d d4 -f plot_from_pkl_3d -bl 1 2   -g 20 -o rev -m brute         --gamma 3
python main.py pre -d d4 -f plot_from_pkl_3d -bl 1 2   -g 20 -o sw  -m greedy        --gamma 3
python main.py pre -d d4 -f plot_from_pkl_3d -bl 1 2   -g 20 -o sw  -m brute         --gamma 3



```



## <span id="head7">Plot net</span>

### <span id="head8">curve p(v) and q(v) under different gamma for each dataset</span>
```angular2html
# 1 figure each dataset
python main.py pre -d d1 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
python main.py pre -d d2 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
python main.py pre -d d4 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
```

### <span id="head9">distributions of vis deg for each dataset,</span>
```angular2html
# 2 figures each dataset
python main.py pre -d d1 --bin 10  -f plot_dist -cl vis deg                 
python main.py pre -d d2 --bin 10  -f plot_dist -cl vis deg
python main.py pre -d d4 --bin 10  -f plot_dist -cl vis deg

```

### <span id="head10">distributions of p and q under different gamma for each dataset</span>
```angular2html                                                                    
# each dataset generate |gml| figures for p and |gml| figures for q                                                           
python main.py pre -d d1 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3                   
python main.py pre -d d2 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3     
python main.py pre -d d4 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3  
   
```




## <span id="head11">Auto documentation</span>

### <span id="head12">usages table</span>

| args           | desc    | 
| :------------- | :---------- |
| -h, --help          | show this help message and exit                               |
| --did , -d          | The data to experiment on.                                    |
| --seed , -s         | The seed for all randomness.                                  |
| --percent_R , -pr   | The percentage of requesters R/N.                             |
| --percent_S , -ps   | The percentage of suppliers S/N.                              |
| --gamma , -gm       | [study] The parameter of function p(v) and q(v).              |
| --budget_list , -bl | [vary] The budget of suppliers to select.                     |
| --grain_p , -gp     | [study]N umber of samples of p, i.e., 1/epsilon_p.            |
| --grain_alpha , -ga | [study] Number of samples of alpha, i.e.,1/epsilon_alpha.     |
| --method , -m       | [study] The method to use to compute optimum.                 |


### <span id="head13">generate doc via sphinx:</span>
```
cd doc
make clean
sphinx-apidoc -o ./source ../exp2 -f
make html
file:///Users/zsy/Desktop/work2exp/doc/build/html/main.html
```





## <span id="head14"> Utils</span>

### <span id="head15">clean history pkl</span>
```
cd exp2
python
>>> import zutil
>>> zutil.clean_old_files()
```

### <span id="head16">extrat content tree</span>
```angular2html
cd exp2
python
>>> import zutil
>>> zutil.detectHeadLines('README.md')
# will override the original README.md
# better use typora to edit, 
```




## <span id="head17"> Statements</span>

### <span id="head18"> datasets</span>
3 datasets

### <span id="head19">naming issues with paper</span>
joint paper
Interchangable concept
```
curve_p <--> value function p_u()
curve_q <--> cost function q_u()
```

each line `u v` the meaning is confusing:
- in code: means there is an edge from u to v, present u can influence v
- in paper: means there is an link from v to u, present v follows u
