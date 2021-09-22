# work2exp

#### Run main algorithms to generate the result pkl:


```
# if use brute_force method  
python main.py -d d1 -gamma 2 -gp 20 -ga 20 -bl 1,2,3,4 -m brute --rev
python main.py -d d1 -gamma 2 -gp 20 -ga 20 -bl 1,2,3,4 -m brute --sw
# if use greedy method  
python main.py -d d1 -gamma 2 -gp 20 -ga 20 -bl 1,2,3,4 -m greedy --rev
python main.py -d d1 -gamma 2 -gp 20 -ga 20 -bl 1,2,3,4 -m greedy --sw
```

Old version
```
python emain0815.py -d d2 --do_greedy -bl 2 -gl 10 -pr 0.5 -ps 0.5 -alpha 0.5 --beta_paras 3,6,6,3
```


#### Generate content for excel record:

```
# if show social welfare
python plot.py -d d1 -gamma 2 -gp 20 -ga 20 -bl 1,2,3,4  --sw
# if show revenue
python plot.py -d d1 -gamma 2 -gp 5 -ga 5 -bl 1,2,3,4  --rev
```

#### Plot
```
python plot.py -d d1 -gamma 2 --stat

```



#### Generate doc via sphinx:
```
cd doc
make clean
sphinx-apidoc -o ./source ../exp2 -f
make html
file:///Users/zsy/Desktop/work2exp/doc/build/html/main.html
```


