import sys
import numpy
import pandas
import tensorflow as tf
import sklearn
import joblib
import matplotlib

print(f"Python version: {sys.version.split()[0]}")
print(f"numpy version: {numpy.__version__}")
print(f"pandas version: {pandas.__version__}")
print(f"tensorflow version: {tf.__version__}")
print(f"scikit-learn version: {sklearn.__version__}")
print(f"joblib version: {joblib.__version__}")
print(f"pickle version: (standard library, no version)")
print(f"matplotlib version: {matplotlib.__version__}")