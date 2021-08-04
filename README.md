# Generators and Iteration Tools

[toc]

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DU_EaMOtUsb5F64b9jtI5y51hu_-o-NY?usp=sharing)

## Generators

- Generators are created by adding a `yield` to the function

- Yield returns the data from the function and remembers the state of the function

- When the function is called next time, it starts the execution from the point where it left

- In the below function, the function call `my_func()` won't return anything since it has become a generator object

- When the `__next__` is implemented on the generator then we will get the output

  ```python
  def my_func():
      i = 0
      print(i)
      i += 1
      yield "Flying"
      print(i)
      yield 'Jeans'
  ```

  ```python
  my_func()
  ```

  ```python
  generator = my_func()
  next(generator)
  ```

- **All Generators are Iterators but all iterators are not generators**





## Making Iterable from Generator

- As we know all the generators are Iterators so they get exhausted
- Sometimes there might be a need of having an inexhaustible generator. Thus, we have to create Iterables from Generators
-  In order to create such Iterables, we use `yield` in the Iterator function to make the class Iterable

```python
class Sqaures:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return Sqaures.squares_gen(self.n)

    @staticmethod
    def squares_gen(n):
        for i in range(n):
            yield i ** 2
```

```python
sq = Sqaures(5)

[num for num in sq]
```

```python
[num for num in sq]
```

- The above example shows that Iterables are created and they are inexhaustible



## Generator Expressions and Performance

- Generators can also be created by using the comprehensions

```python
g = (i**2 for i in range(10))
```

```python
type(g)
```

```python
for item in g:
    print(item)
```

- This is called generator expression
- To fetch the values out of the generator expression, we have to use it with the `for-loop`
- Generators are popular because they are **lazy**
- Generator expressions execute only when they are asked to do so. On the other hand list comprehensions gets executed as soon as they are defined
- This lazy property help to optimize the memory usage
- Below is the memory and speed performance comparison of `list` and `generator` 

```python
from timeit import timeit
from math import factorial

def combo(n, k):
    return factorial(n) // (factorial(k) * factorial(n-k))
```

```python
size = 600
timeit('[[combo(n, k) for k in range(n+1)] for n in range(size+1)]', globals=globals(), number=1)
```

```python
size = 600
timeit('((combo(n, k) for k in range(n+1)) for n in range(size+1))', globals=globals(), number=1)
```

- Above code shows the defining time for both of them is very different. Generators are very fast this is due to the fact that they are just initialized and not executed while the list is executed as soon as it is initialized

```python
from timeit import timeit
```

```python
def pascal_list(size):
    l = [[combo(n, k) for k in range(n+1)] for n in range(size+1)]
    for row in l:
        for item in row:
            pass
```

```python
def pascal_gen(size):
    g = ((combo(n, k) for k in range(n+1)) for n in range(size+1))
    for row in g:
        for item in row:
            pass
```

```python
size = 600
timeit('pascal_list(size)', globals=globals(), number=1)
```

```python
size = 600
timeit('pascal_gen(size)', globals=globals(), number=1)
```

- Executing above code shows execution time is not that different for both the generators and the lists
- Below codes blocks shows that memory usage the very less for the generators since they are not executed but only get created

```python
import tracemalloc
```

```python
def pascal_list(size):
    l = [[combo(n, k) for k in range(n+1)] for n in range(size+1)]
    for row in l:
        for item in row:
            pass
    stats = tracemalloc.take_snapshot().statistics('lineno')
    print(stats[0].size, 'bytes')
```

```python
def pascal_gen(size):
    g = ((combo(n, k) for k in range(n+1)) for n in range(size+1))
    for row in g:
        for item in row:
            pass
    stats = tracemalloc.take_snapshot().statistics('lineno')
    print(stats[0].size, 'bytes')
```

```python
tracemalloc.stop()
tracemalloc.clear_traces()
tracemalloc.start()
pascal_list(300)
```

```python
tracemalloc.stop()
tracemalloc.clear_traces()
tracemalloc.start()
pascal_gen(300)
```



## Yield From

- There might be a case where generators of generators are created
- In such case if we have to access the elements, then we have to write nested `for-loops` 
- This is so common in Python that Python creators have created `yield from` for this purpose
- `yield from <iterator>` is equivalent to `for i in iteraors: yield  i`

```python
def matrix(n):
    gen = ( (i * j for j in range(1, n+1))
            for i in range(1, n+1)
          )
    return gen

def matrix_iterator(n):
    for row in matrix(n):
        for item in row:
            yield item
```

```python
for i in matrix_iterator(3):
    print(i)
```

- If we execute the above and below code blocks, we get same result

```python
def matrix_iterator(n):
    for row in matrix(n):
        yield from row
```

```python
for i in matrix_iterator(3):
    print(i)
```





## Aggregators

We can use the below aggregators on the generators

```python
def squares(n):
    for i in range(n):
        yield i**2
```

```python
min(squares(5))
```

```python
max(squares(5))
```

```python
sum(squares(5))
```





## Slicing

- In generators, slicing is not possible in the conventional way
- Below code blocks throws an error when we try to slice the generators

```python
import math

def factorials(n):
    for i in range(n):
        yield math.factorial(i)

facts = factorials(100)        
```

```python
facts[0:2]
```

- In order to slice, we can use the following function 

```python
def slice_(iterable, start, stop):
    # Exhaust all the values before the starting point
    for _ in range(0, start):
        next(iterable)
        
    # Yield the values in the range of interest
    for _ in range(start, stop):
        yield(next(iterable))
```

```python
list(slice_(factorials(100), 1, 5))
```

- Itertools also provide `islice` to perform the similar job

```python
from itertools import islice

list(islice(factorials(10), 0, 3))
```

- **Negative Slicing is not possible using `islice`**





## Selecting and Filtering

- Element selecting and filtering can be done using the below functions from itertools

```python
def gen_cubes(n):
    for i in range(n):
        print(f'yielding {i}')
        yield i**3

def is_odd(x):
    return x % 2 == 1

def is_even(x):
    return x % 2 == 0
```

### filter() and filterfalse()

```python
filtered = filter(is_odd, gen_cubes(10))
```

```python
from itertools import filterfalse

evens = filterfalse(is_odd, gen_cubes(10))
```

### takewhile() and dropwhile()

```python
from itertools import takewhile

list(takewhile(lambda x: 0 <= x <= 0.9, gen_cubes(15)))
```

```python
from itertools import dropwhile

l = [1, 3, 5, 2, 1]
list(dropwhile(lambda x: x < 5, l))
```

### zip()

```python
data = ['a', 'b', 'c', 'd', 'e']
selectors = [True, False, 1, 0]

[item for item, truth_value in zip(data, selectors) if truth_value]
```

### compress()

```python
from itertools import compress
list(compress(data, selectors))
```





## Infinite Iterators

- These can be created using the following functions from itertools

```python
from itertools import (
    count,
    cycle,
    repeat, 
    islice)
```

### count()

```python
from decimal import Decimal

g = count(10)
g = count(10, step=2)
g = count(1+1j, 1+2j)
g = count(Decimal('0.0'), Decimal('0.1'))
```

### cycle()

```python
g = cycle(('red', 'green', 'blue'))
list(islice(g, 8))

def colors():
    yield 'red'
    yield 'green'
    yield 'blue'
cols = colors()
g = cycle(cols)
```

### repeat()

```python
g = repeat('Python')
for _ in range(5):
    print(next(g)
```



---



## Code Details

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1d6wl2sAtUPlK0Qf_bqBYeQfC82v2fOLu?usp=sharing)

### Problem Statement

#### Goal 1

Create a lazy iterator that will return a named tuple of the data in each row. The data types should be appropriate - i.e. if the column is a date, you should be storing dates in the named tuple, if the field is an integer, then it should be stored as an integer, etc.

#### Goal 2

Calculate the number of violations by car make.



### Solution

#### Goal 1

- The goal is to get a row from a file
- When we open the file, the iterator for the file is a lazy iterator and that's what make the class `LazyIterator`  lazy
- If the goal was to access the elements of each row then we could have created another lazy iterator to provide the data
- Creating another generator inside the class will be redundant hence we are only accessing the data from pre-existing lazy iterator
- Adding additional laziness creates unnecessary complexities to access the data

```python
from collections import namedtuple, Counter

class LazyIterator:
    """
    LazyIterator class to read from *.csv file and return namedtuple of data in each row
    """
    def __init__(self, filename):
        """
        Constructor
        """
        # To check if all the rows are read from the file
        self.exhausted = False

        # Namedtuple to store the date information
        self.Date = namedtuple('Date', "month day year")
        self.Date.__doc__ = 'Date on which the traffic violation was issued'
        self.Date.month.__doc__ = 'Month of the year'
        self.Date.day.__doc__ = 'Day of the month'
        self.Date.year.__doc__ = 'Year'

        # Data type of each field in the namedtuple
        self.data_types = ['INT', 'STRING', 'STRING', 'STRING', 'DATE', 'INT', 'STRING', 'STRING', 'STRING']

        self.file = open(filename, 'r')

        # Create an iterator for iterating over rows of a file
        self.file_iter = iter(self.file)

        # Format the 1st line to extract the headers from the file
        headers = next(self.file_iter).replace(' ', '').strip('\n').split(',')

        # Create a namedtuple for the violation data
        self.Data = namedtuple('Data', headers, defaults=[None] * len(headers))
        self.Data.__doc__ = "Traffic violation data"
        self.Data.SummonsNumber.__doc__ = "Record number associated with the violations"
        self.Data.PlateID.__doc__ = "Plate Number of the vehicle"
        self.Data.RegistrationState.__doc__ = "State in which the vehicle is registered"
        self.Data.PlateType.__doc__ = "Type of number plate on the vehicle"
        self.Data.IssueDate.__doc__ = "Date on which the violation was issued"
        self.Data.ViolationCode.__doc__ = "Traffic violation code"
        self.Data.VehicleBodyType.__doc__ = "Type of the vehicle body"
        self.Data.VehicleMake.__doc__ = "Manufacturing Company of the vehicle"
        self.Data.ViolationDescription.__doc__ = "Description of Violation"

    def __iter__(self):
        """
        Method to create an iterator
        """
        return self

    def __next__(self):
        """
        Method to access next row from the file
        """
        if not self.exhausted:
            row_data = self.cast_row(self.data_types, next(self.file_iter).replace(' ', '').strip('\n').split(','))
            if row_data is not None:
                return row_data
            raise StopIteration
        raise StopIteration

    def cast_row(self, data_type, data_row):
        """
        Function to return the casted value of the data row
        :param data_type: Expected data type
        :param data_row: Input data row
        :return: Data row in the converted format
        """
        casted_data = (self.cast(data_type, value) for data_type, value in zip(data_type, data_row))

        _data = self.Data(*casted_data)
        return _data

    def cast(self, data_type, value):
        """
        Function to cast appropriate data type for the input value
        :param data_type: Expected data type
        :param value: Input value
        :return: Converted value in the data_type
        """
        if data_type == 'STRING':
            return str(value)
        elif data_type == 'INT':
            return int(value)
        elif data_type == 'DATE':
            value = value.split('/')
            return self.Date(*value)
```

```python
# Create an object of class
_object = LazyIterator('nyc_parking_tickets_extract-1.csv')
```

```python
# Create an Iterator Object
iterator_object = iter(_object)
parking_data = []

# Access row data from the iterator
for row in iterator_object:
    parking_data.append(row)
    print(row)
```



#### Goal 2

```python
violation_data = Counter(data.VehicleMake for data in parking_data if data is not None)
print(violation_data)
```

