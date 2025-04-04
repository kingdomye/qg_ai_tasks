Each topology is saved with an **NPY** file created by **NumPy** library, researchers can read it with any NPY software interface. The file contains the state information of all agents, and this dataset only involves two-dimensional state, where edge weighs are provided in the description of Fig. 2. For example: 

```python
[
    [x1, y1],   # the state of 1st agent
    [x2, y2],   # the state of 2nd agent
    ...
    [xn, yn],   # the state of n-th agent    
]
```

