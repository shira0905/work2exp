- [ work2exp](#head1)
	- [ 环境搭建](#head2)
	- [Run algorithms **](#head3)
		- [ 运行记录](#head4)
		- [ 结果可视化](#head5)
		- [CSV debug](#head6)
			- [pkl2csv: 将**单个**pkl转化成以以下head格式的csv](#head7)
			- [将多个pkl转化成以以下head格式的csv  (参数: 选中的文件列表)](#head8)
			- [将多个pkl转化成以以下head格式的csv  (参数: 给定的四个参数 进行笛卡尔乘积)](#head9)
			- [视图陈列 TODO](#head10)
	- [Plot exp **](#head11)
		- [evaluating $\texttt{OptSupplierSet}$](#head12)
		- [evaluating the $\texttt{OptPrice(OptSupplierSet)}$](#head13)
		- [ the impact of valuation functions](#head14)
		- [one figure each budget ](#head15)
		- [one figure each epsilon](#head16)
		- [fixied epsilon, vary pricing scheme](#head17)
	- [Plot net](#head18)
		- [curve p(v) and q(v) under different gamma for each dataset](#head19)
		- [distributions of vis deg for each dataset,](#head20)
		- [distributions of p and q under different gamma for each dataset](#head21)
	- [Auto documentation](#head22)
		- [get help](#head23)
		- [usages table](#head24)
		- [generate doc via sphinx:](#head25)
	- [ Utils](#head26)
		- [clean history pkl](#head27)
		- [extrat content tree](#head28)
	- [ Statements](#head29)
		- [ datasets](#head30)
		- [naming issues with paper](#head31)
# <span id="head1"> work2exp</span>





## <span id="head2"> 环境搭建</span>

```
# 根据yml文件创建虚拟环境（文件中已经包括环境名字）
conda env create -f environmenttest.yml

# 导出虚拟环境到yml文件
conda env export > environment.yml
```





## <span id="head3">Run algorithms **</span>


### <span id="head4"> 运行记录</span>

```
python main.py algo -dl d1 d4 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48
python main.py algo -dl d2 d5 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48
python main.py algo -dl d3 d6 -ll 2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4 # 2x2x4x3=48

# test
python main.py algo        -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 2 -bl 1 2
python zutil.py -f csvbr1  -dl d1 -ll 2  -ol I W RI RW -ml brute  -bl 1 2
python main.py algo -dl d1 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3 # 1x2x5x1=10
python main.py algo -dl d4 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2 3 # 1x2x5x1=10
python main.py algo -dl d2 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d5 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d3 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
python main.py algo -dl d6 -ll 2 3  -ol I W RI RW -ml brute  -gl 20 -bl 1 2   # 1x2x5x1=10
```



### <span id="head5"> 结果可视化</span>

缺少的会did 

```
# 1104 aggregate
python zutil.py -f csvopt -dl d1 -ll 1 2 3  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvfull -dl d1 -ll 1 2 3  -ol I W RI RW -ml brute greedy h1 h2 -gl 20 -bl 1 2 3 4

# 1104-1930 test aggregate
python zutil.py -f csvopt  -dl d1 d4 -ll  2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvfull -dl d1 d4 -ll  2 3  -ol I W RI RW -ml greedy h1 h2 -gl 20 -bl 1 2 3 4
python zutil.py -f csvbr1  -dl d1 -ll 2  -ol I W RI RW -ml brute  -gl 20 -bl 1 

python main.py algo -dl d1 -ll 2  -ol I W RI RW -ml brute -gl 2 -bl 1 2

python zutil.py -f csvbr1  -dl d1 -ll 2  -ol I W RI RW -ml brute  -bl 1 2
python zutil.py -f  csvopt -dl d1   -ll 2    -ol I W RI RW -ml greedy h1 h2 brute -gl 20 -bl 1 2
```





#### <span id="head8">将多个pkl转化成以以下head格式的csv  (参数: 选中的文件列表)</span>

命令参数: 选中pkl files, 右键复制路径, 参数记得加引号在黏贴, 因为是\n分隔的

```
python zutil.py -f merge_pkl_2csv_select -files "
_d1_1_I_brute_1101232129.pkl
_d1_1_I_h1_1101232129.pkl"
# 格式列名 ['did', 'lamb', 'obj', 'method', 'budget', 'opt_scheme', 'opt_setM_star', 'opt_obj_star']
# 输出文件 ../eplots/exp/merge_{nowTime}.csv
```





## <span id="head11">Plot exp **</span>







### <span id="head12">evaluating $\texttt{OptSupplierSet}$</span>

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



### <span id="head13">evaluating the $\texttt{OptPrice(OptSupplierSet)}$</span>

比较不同的 epsilon 对结果的影响

### <span id="head14"> the impact of valuation functions</span>







### <span id="head15">one figure each budget </span>

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


### <span id="head16">one figure each epsilon</span>

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


### <span id="head17">fixied epsilon, vary pricing scheme</span>

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



## <span id="head18">Plot net</span>

### <span id="head19">curve p(v) and q(v) under different gamma for each dataset</span>
```angular2html
# 1 figure each dataset
python main.py pre -d d1 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
python main.py pre -d d2 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
python main.py pre -d d4 -f plot_curve_single -cl p q  -gml 0 0.5 1 2 3   
```

### <span id="head20">distributions of vis deg for each dataset,</span>
```angular2html
# 2 figures each dataset
python main.py pre -d d1 --bin 10  -f plot_dist -cl vis deg                 
python main.py pre -d d2 --bin 10  -f plot_dist -cl vis deg
python main.py pre -d d4 --bin 10  -f plot_dist -cl vis deg

```

### <span id="head21">distributions of p and q under different gamma for each dataset</span>
```angular2html                                                                    
# each dataset generate |gml| figures for p and |gml| figures for q                                                           
python main.py pre -d d1 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3                   
python main.py pre -d d2 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3     
python main.py pre -d d4 --bin 10  -f plot_dist -cl p q -gml 0.5 1 2 3  
   
```



## <span id="head22">Auto documentation</span>

### <span id="head23">get help</span>

honestly I refer to README.md for command instruction rather than use 'help'

```
python main.py -h # get sub command
python main.py algo # get the details of sub command
python main.py plot # get the details of sub command
```



### <span id="head24">usages table</span>

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


### <span id="head25">generate doc via sphinx:</span>
```
cd doc
make clean
sphinx-apidoc -o ./source ../exp2 -f
make html
file:///Users/zsy/Desktop/work2exp/doc/build/html/main.html
```





## <span id="head26"> Utils</span>

### <span id="head27">clean history pkl</span>
```
python zutil.py -f clean_old_pkl -dl d1  -ll 1 2 3  -ol I W RI RW A -ml h1 h2 brute # 这个是全部情况的参数
A 也需要删除, 有update
```

### <span id="head28">extrat content tree</span>
```angular2html
python zutil.py -f detectHeadLines -file ../README.md 
```




## <span id="head29"> Statements</span>

### <span id="head30"> datasets</span>
3 datasets

### <span id="head31">naming issues with paper</span>
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
