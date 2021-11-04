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

### 运行记录

```
python main.py algo -dl d1 d4 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48
python main.py algo -dl d2 d5 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48
python main.py algo -dl d3 d6 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48

python main.py algo -dl d1 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3 # 1x2x5x1=10
python main.py algo -dl d4 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3 # 1x2x5x1=10
python main.py algo -dl d2 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d5 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d3 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d6 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
```











### recording

```
# 1102-1540 running
python main.py algo -dl d1 -ll 2 3  -ol I W RI RW -ml brute -gl 20 -bl 1 2 3

# 1103-1230 看昨天跑出来的 在各个情setting下的 optimal scheme
python zutil.py -f merge2csv_var -dl d1 -ll 2 3  -ol I W RI RW -ml brute 
# sample 某一个setting的各个scheme 下的 M_star
python zutil.py -f show2csvs_select -files "
d1_2_I_brute_1102161557.pkl
d1_2_RI_brute_1102172523.pkl"

# 1103-1330 running
python main.py algo -dl d1 -ll 1  -ol I W RI RW -ml brute -gl 20 -bl 1 2 3

# 1900 running using 4times faster new implementation
python main.py algo -dl d1 -ll 2 3  -ol I W RI RW -ml brute h1 -gl 5 -bl 1 2
# 2030 testing new implementation for greedy
python main.py algo -dl d1 -ll 2 3  -ol I W RI RW -ml brute h1 -gl 5 -bl 1

# 1103-2200 running
python main.py algo -dl d1 -ll 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   

python main.py algo -dl d2 -ll 1 2 3  -ol I W RI RW -ml greedy h1 h2  -gl 20 -bl 1 2 3 4

# 1104 aggregate
python zutil.py -f csvopt -dl d1 -ll 1 2 3  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvfull -dl d1 -ll 1 2 3  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1 2 3 4
 
# 1104 brute
python main.py algo -dl d1 -ll 1 2 3  -ol I W RI RW -ml brute h1 -gl 5 -bl 1 2

# 1104-1830 run easys
python main.py algo -dl d1 -ll 1 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
python main.py algo -dl d4 -ll 1 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
# 1104-1900 test brute
python main.py algo -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 20 -bl 1 2

# 1104-1930 test aggregate
python zutil.py -f csvopt -dl d1 d4 -ll 1 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvfull -dl d1 d4 -ll 1 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvbr1 -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 20 -bl 1
python zutil.py -f csvbr4 -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 20 -bl 1
python zutil.py -f csvopt -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 20 -bl 1
python zutil.py -f csvfull -dl d1 -ll 2  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1

# 1105
python main.py algo -dl d1 -ll  2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3
python main.py algo -dl d4 -ll  2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3
python main.py algo -dl d2 -ll  2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2
python main.py algo -dl d5 -ll  2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2


```









### CSV debug

#### pkl2csv: 将**单个**pkl转化成以以下head格式的csv

```
python zutil.py -f pkl2csv -file d1_2_I_brute_1102151009.pkl  
# 格式列名 ['did', 'lamb', 'obj', 'method', 'budget', 'scheme', 'setM_star', 'I', 'W', 'RI', 'RW']
# 输出文件 ../eplots/exp/show_{file}.csv
```

#### 将多个pkl转化成以以下head格式的csv  (参数: 选中的文件列表)

命令参数: 选中pkl files, 右键复制路径, 参数记得加引号在黏贴, 因为是\n分隔的

```
python zutil.py -f merge_pkl_2csv_select -files "
_d1_1_I_brute_1101232129.pkl
_d1_1_I_h1_1101232129.pkl"
# 格式列名 ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']
# 输出文件 ../eplots/exp/merge_{nowTime}.csv
```

#### 将多个pkl转化成以以下head格式的csv  (参数: 给定的四个参数 进行笛卡尔乘积)

命令参数: 适用于想看一下上一个run出来的一些pkls, 直接复制algo里面的 dl ll ol ml 四个参数.

```
python zutil.py -f merge_pkl_2csv -dl d1  -ll 1 2 3  -ol I W RI RW  -ml h1 brute
# 格式列名 ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']
# 输出文件 ../eplots/exp/merge_{info}.csv
```

#### 视图陈列 TODO

用 VSCODE 打开, 比pycharm的 edit as table 强

```
python zutil.py -f aggregate -dl d1 -ll 2 3  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1 2 3 4
```

- [ ] 如果没有那个pkl文件就不行, 改成占位吧



## <span id="head3">Plot exp **</span>







### evaluating $\texttt{OptSupplierSet}$

```
python main.py algo -dl d1 -ll 1 2 3 -gl 20 10 5 -ol I W RI RW -ml h1 greedy -bl 1 2 3 4

python main.py algo -d d2 -bl 1 2 3   -g 20 -o rev  -m brute  --gamma 3    
python main.py algo -d d4 -bl 1 2     -g 20 -o rev  -m brute  --gamma 3
```



- [ ] 理清楚需要画哪一些图
  - data = {d1, d2, d3}
    - gamma = {1, 2, 3}
      - obj = {I, V, R}
        - Plot 
          x-axis: budget list of data
          y-axis: value obj
          columns: 3 algorithms

  那么就是 3x3x2= 18 pdf, 注意这里的revenue不画

- [ ] 怎么分组好呢
  - [ ] Fig1: gamma=1 
    - [ ] I of d1, V of d1
    - [ ] I of d2, V of d2
    - [ ] I of d3, V of d3
  - [ ] Fig2: gamma=2 的时候: 有6张子图同上
  - [ ] Fig3: gamma=3 的时候: 有6张子图同上

- [ ] 3d 放在这里比较合适吧, 



### evaluating the $\texttt{OptPrice(OptSupplierSet)}$

比较不同的 epsilon 对结果的影响

###  the impact of valuation functions







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

### get help

honestly I refer to README.md for command instruction rather than use 'help'

```
python main.py -h # get sub command
python main.py algo # get the details of sub command
python main.py plot # get the details of sub command
```



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
python zutil.py -f clean_old_pkl -dl d1  -ll 1 2 3  -ol I W RI RW A -ml h1 h2 brute # 这个是全部情况的参数
A 也需要删除, 有update
```

### <span id="head16">extrat content tree</span>
```angular2html
python zutil.py -f detectHeadLines --filename README.md  # 1102 还未测试服哦
```




## <span id="head17"> Statements</span>

### <span id="head18"> datasets</span>
3 datasets

### <span id="head19">naming issues with paper</span>
- valuation function and curve

  Interchangable concept

  - curve_p <--> value function p_u()
  - curve_q <--> cost function q_u()

- each line `u v` the meaning is confusing:
  - in code: means there is an edge from u to v, present u can influence v
  - in paper: means there is an link from v to u, present v follows u
- name of objective / measurements 
  - objI   / the first type objective / the first type network welfare
  - objV  / sw / the second type objective / the second type network welfare
  - objR / rev

- replave all alpha by p

- grain and epsilon

  - grain is integer used in code 
  - epsilon is 1/grain used in paper

- gamma lambda (之前gamma重复了所以改成

  - gamma is the propotional of requesters and supliers in the 

  - [ ] lambda is the parameter of valuaiton function 还没有改过来, 改成lamb 不然冲突

- solution 5元 result 4元 少了一个setM
