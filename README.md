# Flexible Job-shop Scheduling Problem With Genetic Algorithm

This project involves using Genetic Algorithm to solve the Flexible Job-shop Scheduling Problem.

## 1. Create Instance.py based on actual problems

For example, the following is the processing schedule for each certain workpiece.


|            | Machine1 | Machine2 | Machine3 | Machine4 | Machine5 | Machine6 | Machine7 | Machine8 | Machine9 | Machine10 | Machine11 |
| :--------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :------: | :-------: | :-------: |
| Operation1 |    10    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation2 |    0    |    9    |    0    |    0    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation3 |    0    |    0    |    14    |    16    |    0    |    0    |    0    |    0    |    0    |     0     |     0     |
| Operation4 |    0    |    0    |    0    |    0    |    15    |    25    |    21    |    0    |    0    |     0     |     0     |
| Operation5 |    0    |    0    |    0    |    0    |    0    |    0    |    0    |    9    |    13    |    25    |    14    |

If the number of workpieces is **5**, the **Instance.py** will be written in the following format.

```python
Processing_time = [[10, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9999, 14, 16, 9999, 9999, 9999, 9999, 9999, 9999, 9999],
                   [9999, 9999, 9999, 9999, 15, 25, 21, 9999, 9999, 9999, 9999],
                   [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9, 13, 25, 24]]
J = {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}
J_num = 5
M_num = 11
O_num = 25
```

The following is an introduction to variable names.

* **Processing_time** : `the processing schedule of every workpiece written in the list format`
  * _In the table, the row index represents the sequence number of the operation, the column index represents the sequence number of the machine, and the numerical value represents the corresponding processing time._
  * _If a machine is not selected in the operation, the corresponding value is represented by **9999**._
* **J** : `the index of each workpiece and the total number of corresponding operations written in the dictionary format`
* **J_num** : `the number of workpieces`
* **M_num** : `the number of machines`
* **O_num** : `the number of operations for all workpieces`

## 2. Set the parameters of Genetic Algorithm

Set the parameters of the genetic algorithm in **GA.py**.

```python
class GA():
    def __init__(self):
        self.Pop_size = 400
        self.Pc = 0.8
        self.Pm = 0.3
        self.Pv = 0.5
        self.Pw = 0.95
        self.Max_Itertions = 100
```

The following is an introduction to variable names.

* **Pop_size** : `the size of population`
* **Pc** : `the probability of performing the crossover operation`
* **Pm** : `the probability of performing the variational operation`
* **Pv** : `the probability of choosing which way to perform the crossover operation`
* **Pw** : `the probability of choosing which way to perform the variational operation`
* **Max_Itertions** : `the maximum number of evolutionary generations`

## 3. Run main.py

After the code runs, the following two results will appear.

* **Result1** : processing schedule of all the workpieces showed in gantt chart

  ![](assets/img1.png)

* **Result2** : the maximum completion time of each iteration

  ![](assets/img2.png)
