---
title: Techniucale Documentation Homepage
summary: Here given overview of the Green fuel validation platform.
authors:
    - Haradhan Sharma
    - 
date: 2023-01-24

---
# Welcome to GFVP Technical Docs


## About Project Technologies
* It is a `Python39-Django's` project.
* Using `Bootstrap5` based `Volt` template partially.
* `HTMX` JS library implemented for interactivity.
* `MySql` as database.
* Project running on the VPS.
* `requirements.txt` explaining the package requirements to run the project.

## Business Logic and Developper

* Business logic and design idea provided by Krishna Hara Chakrabarti
* Sole developer [Haradhan Sharma](https://hrdnsh.com)

## Requirements

* All python and Django library listed in the `requirements.txt`
* `Bootstrap 5` has been used as CSS librry
* `HTMX` Implemented
* `chartist.js` used to genarate Graphicale chart i the website.
* `aos.js` for animation. using form CDN.
* `mkdocs` for technicale documentation.


## Project layout
    accounts            # Django app to control user accounts. Described at (/docs/accounts.html)
    blog                # Django app to control Blog functionality. Described at (/docs/blog.html)
    crm                 # Django app to control minimalist CRM side width. Described at (/docs/crm.html)
    doc                 # Django app to manage common data site width. Described at (/docs/doc.html)
    evaluation          # Django app to control evaluation procedure and reports. Described at (/docs/evaluation.html)
    gfvp                # Main Django Project
    gfvp_docs           # mkdocs framework to wrie technicale documentation. Described at (https://www.mkdocs.org)
    glossary            # Django app to control glossary feature. Described at (/docs/glossary.html)
    guide               # Django app to manage genarel documetation about site feature and usecase. Described at (/docs/guide.html)
    home                # Django app to manage some general sction. Describe at (/docs/index.html)
    static              # Django's static root directory
    templates           # Main Template directory of the project
    manage.py           # Django Project file
    mkdocs.yml          # The configuration file of mkdocs
    my_project.dot      # About project layout
    my_project.png      # Grahical databse schema of the project.
    requirements        # Dependencies are listed here.


## Necessary Information
* The project can be deploy at linux and windows both
* To know about features and user guide visit [Guide](https://gf-vp.com/guide).
* If `git pull` command instruct to stash due to migration file ended with `alter_lead_confirm.py` and `alter_accordion_apps.py` just delete those file from target and recall `git pull`
* `.so` is essential for linux environment and `.pyd` is essential for windows of the evaluation app
* `.so` is essential for linux environment and `.pyd` is essential for windows of the **gfvp** project folder.




## Mkdocs Commands 
* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.






# Heading level 1 
## Heading level 1
### Heading level 1
#### Heading level 1
##### Heading level 1
###### Heading level 1

I just love **bold text**.
I just love __bold text__.
Love**is**bold

> Dorothy followed her through many of the beautiful rooms in her castle.


> Dorothy followed her through many of the beautiful rooms in her castle.
>
> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.


> Dorothy followed her through many of the beautiful rooms in her castle.
>
>> The Witch bade her clean the pots and kettles and sweep the floor and keep the fire fed with wood.



> #### The quarterly results look great!
>
> - Revenue was off the chart.
> - Profits were higher than ever.
>
>  *Everything* is going according to **plan**.


1. First item
2. Second item
3. Third item
    1. Indented item
    2. Indented item
4. Fourth item


- First item
- Second item
- Third item
    - Indented item
    - Indented item
- Fourth item

* This is the first list item.
* Here's the second list item.

    I need to add another paragraph below the second list item.

* And here's the third list item.


* This is the first list item.
* Here's the second list item.

    > A blockquote would look great below the second list item.

* And here's the third list item.


At the command prompt, type `nano`.


``Use `code` in your Markdown file.``


***

---

_________________


My favorite search engine is [Duck Duck Go](https://duckduckgo.com).

My favorite search engine is [Duck Duck Go](https://duckduckgo.com "The best search engine for privacy").


I love supporting the **[EFF](https://eff.org)**.
This is the *[Markdown Guide](https://www.markdownguide.org)*.
See the section on [`code`](#code).

![The San Juan Mountains are beautiful!](/assets/images/san-juan-mountains.jpg "San Juan Mountains")


[![An old rock in the desert](/assets/images/shiprock.jpg "Shiprock, New Mexico by Beau Rogers")](https://www.flickr.com/photos/beaurogers/31833779864/in/photolist-Qv3rFw-34mt9F-a9Cmfy-5Ha3Zi-9msKdv-o3hgjr-hWpUte-4WMsJ1-KUQ8N-deshUb-vssBD-6CQci6-8AFCiD-zsJWT-nNfsgB-dPDwZJ-bn9JGn-5HtSXY-6CUhAL-a4UTXB-ugPum-KUPSo-fBLNm-6CUmpy-4WMsc9-8a7D3T-83KJev-6CQ2bK-nNusHJ-a78rQH-nw3NvT-7aq2qf-8wwBso-3nNceh-ugSKP-4mh4kh-bbeeqH-a7biME-q3PtTf-brFpgb-cg38zw-bXMZc-nJPELD-f58Lmo-bXMYG-bz8AAi-bxNtNT-bXMYi-bXMY6-bXMYv)


| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |


```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```


```json
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```

http://www.example.com

`http://www.example.com`

This **word** is bold. This <em>word</em> is italic.