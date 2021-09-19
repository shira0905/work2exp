# work2exp

To run main algorithms to generate the result pkl:
```
# if use brute_force method
python main.py -d d1 -a 2 -gp 20 -ga 20 -bl 1,2,3 -m brute
# if use greedy method
python plot.py -d d1 -a 2 -gp 20 -ga 20 -bl 1,2,3 -m greedy
```


To generate the content for excel record:

```
# if show social welfare
python plot.py -d d1 -a 2 -gp 20 -ga 20 -bl 1,2,3,4  --sw
# if show revenue
python plot.py -d d1 -a 2 -gp 20 -ga 20 -bl 1,2,3,4  --rev
```


