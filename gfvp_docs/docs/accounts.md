---
title: Documention of account app of the green fuel validation platform
summary: Technicale documention of the Account app of the green fuel validatuin platform has been mentioned here.
authors:
    - Waylan Haradhan Sharma
    - 
date: 2023-01-24
---

# Welcome to Accounts app's Technical Docs

Here I will mention the important points of Account App. These points will help a Django developer get an idea of the project.
***
### About `models.py`
***

#### `class UserType(models.Model)` have 4 BooleanField:
* `is_marine`
* `is_producer`
* `is_expert`
* `is_consumer` and
* `active` BooleanField to control use type in frontend.

indicates the types of user of the site.




---
This is the first paragraph of the document.

| First Header | Second Header | Third Header |
| ------------ | ------------- | ------------ |
| Content Cell | Content Cell  | Content Cell |
| Content Cell | Content Cell  | Content Cell |

```
Fenced code blocks are like Standard
Markdown’s regular code blocks, except that
they’re not indented and instead rely on
start and end fence lines to delimit the
code block.
```

```python
def fn():
    pass
```


| Fruit(left)      | Emoji(center) | Taste(right)     |
| :---        |    :----:   |          ---: |
| Mango is the king of Fruits      | :mango:       | Sweet, and I love it  |
| Lemon is good for health   | :lemon:        | Sour, mix it in the water     |