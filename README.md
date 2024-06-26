# SimpleSpellChecker
Thai customizable spell-checking library in Python. 

# How to use

```python

from lstchecker import LSTSpellChecker

checker = LSTSpellChecker(correct_list="<file of correct spelling list>",
                          incorrect_list="<file of incorrect spelling list>")

output = checker.process("<your input here (in Thai)>")
```

# File Format 

## Correct List

```
กก
กกช้าง
กกธูป
กกุธภัณฑ์
กง
กงกอน
กงการ
กงฉาก
...
```

## Incorrect List

```
(incorrect word) ||| (correct word)
```

For example, 

```
ดิจิตอล ||| ดิจิทัล
```



# Limitation

Current version supports only Thai text.