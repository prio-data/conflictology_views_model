# VIEWS Conflictology Model 🛠️
## A general purpose Python function for generating VIEWS conflictology forecasts

[![Official Website](https://img.shields.io/badge/PRIO_website-www.prio.org-darkgreen
)](https://www.prio.org)
[![VIEWS Forecasting Website](https://img.shields.io/badge/VIEWS_Forecasting-www.viewsforecasting.org-purple
)](https://www.prio.org)
[![Twitter Follow](https://img.shields.io/twitter/follow/PRIOresearch
)](https://twitter.com/PRIOresearch)
[![LinkedIn](https://img.shields.io/badge/PRIO_on_linkedin-LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/company/prio/?originalSubdomain=no)


VIEWS conflictology model is a Python function designed to facilitate generating conflictology uncertainty forecasts. It is developed and maintained by the [Peace Research Institute Oslo (PRIO)](https://www.prio.org) as part of the [VIEWS project](https://www.prio.org/Projects/Project/?x=1749).


## 📚 Table of Contents 

1. [🛠 Installation](#🛠-installation)
2. [📝 Usage](#📝-usage)
3. [🤝 Contributing](#🤝-contributing)
4. [🐞 Common bugs](#🐞-common-bugs)
5. [🔖 License](#🔖-license)

## 🛠 Installation

To use conflictology model, the required libraries are:

```python
from viewser import Queryset, Column
import numpy as np
import pandas as pd
```


## 📝 Usage

The conflictology_benchmark function is the main function  


```python
# variables
test_partitioner_dict = {"train": (491, 492), "predict": (493, 504)}
steps = [1, 2, 3, 9, 36]
outcome = 'sb'
loa = 'cm'
x_conflictology = 3

# function call
conflictology_benchmark(test_partitioner_dict, steps, loa,x_conflictology, outcome)



```

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Make an issue describing the feature you want to add or the bug you want to fix.
2. Create your Feature Branch (`git checkout -b <issuenumber>-<your-feature-name>`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin <issuenumber>-<your-feature-name>`)
5. Open a Pull Request

## 🐞 Common bugs

A common bug is not importing the function from the script, so please import it as given below:

```python
# the function is in the views_conflictology file
import views_conflictology as fm
```


## 🔖 License

Distributed under the MIT License.



