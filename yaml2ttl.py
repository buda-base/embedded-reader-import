
import yaml
import dpath.util

with open('test.yaml') as f:
    # use safe_load instead load
    dataMap = yaml.safe_load(f)
    print(dataMap[0])



