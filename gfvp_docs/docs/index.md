---
title: Techniucale Documentation Homepage
summary: Here given overview of the Green fuel validation platform.
authors:
    - Haradhan Sharma
    - 
date: 2023-01-24

---


# GFVP - Green Fuel Validation Platform
    ## Solo Developer:
        Haradhan Sharma
        Email: haradhan.sharma@gmail.com
        Website: [hrdnsh.com](http://hrdnsh.com)

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Technology Stack](#technology-stack)
4. [Contributors](#contributors)
5. [Installation](#installation)
6. [Usage](#usage)
7. [Documentation](#documentation)
8. [License](#license)

---
## Project Overview

GFVP (Green Fuel Validation Platform) is a web application built using Django 4.0.1 and various frontend technologies. It serves as a platform for validating and managing green fuel-related data. The application allows different types of users to interact with the system, and it's designed to support various features for managing data related to green fuels.
***
## Project Structure

**The project follows a well-organized directory structure:**

    root/
        accounts -> app
        blog -> app
        crm -> app
        doc -> app
        evaluation -> app
        feedback -> app
        gfvp -> project
        gfvp_docs -> mkdocs directory
        glossary -> app
        guide -> app
        home -> app
        navigation -> app
        logs
        static -> static folder
        upload -> media folder
        templates -> templates for apps and project
        .env
        .gitignore
        gfvp.dot
        gfvp.png ->database schema
        manage.py ->project manager
        mkdocs.yml ->mkdocs configuration
        requirements.txt
        robots.txt


Ensure that the necessary Python packages specified in `requirements.txt` are installed for the project to run successfully.
___
## Technology Stack

- Python 3.10
- Django 4.0.1
- ReportLab
- Panda
- Numpy
- xhtml2pdf
- Material Admin
- Bootstrap 5 with Volt theme
- Chartist.js
- AOS.js
- HTMX
- jQuery
- Font Awesome
- Youtube API
- IPinfo API

## Contributors

    
    1. Business logic and instructions provided by:
        1. Krishna Hara Chakrabarti
        2. Jessica Hofman
    2. Contributed to user guide
        1. Pragya Chudal
   

## Installation

- Clone the repository to your local machine.   
    `git clone <repository_url>`

- Create a virtual environment (optional but recommended).    
    `python -m venv venv`

- Activate the virtual environment.  

    `// On Windows
    venv\Scripts\activate`

    `// On macOS and Linux
    source venv/bin/activate`

- Install the required dependencies. 
    `pip install -r requirements.txt`

- Create a `.env` file in the project root and configure any environment-specific settings.
- Apply database migrations.  
    `python manage.py migrate`

- Start the development server.  
    `python manage.py runserver`

The application should now be accessible at http://localhost:8000/.

## Usage

__Genarate .dot file and database schema__

* First, make sure you have django-extensions installed. If it's not already in your `requirements.txt`, you can add it:

    ``django-extensions==3.2.1``

* Then, run the following command to generate a graph_models.dot file:

    ``python manage.py graph_models -a -o gfvp.dot``

* To generate a PNG image from the `.dot` file, you can use Graphviz. If you don't have Graphviz installed, you can add it to your `requirements.txt`:

    ``graphviz==0.17``

* After installing Graphviz, you can use the dot command to convert the .dot file to a PNG image:

    ``dot -Tpng gfvp.dot -o gfvp.png``

## Mkdocs Commands 
* Configure `mkdocs.yml`.
* Add `xxxx.md` in `gfvp_docs/docs`
* run `mkdocs build` command to build the documentation site.
* `mkdocs -h` - Print help message and exit.


## Documentation

Documentation for each app can be found in their respective `readme.md` files:

- [Accounts App](/docs/accounts.html)
- [Blog App](/docs/blog.html)
- [CRM App](/docs/crm.html)
- [Doc App](/docs/doc.html)
- [Evaluation App](/docs/evaluation.html)
- [Feedback App](/docs/feedback.html)
- [GFVP Project](/docs/gfvp.html)
- [Glossary App](/docs/glossary.html)
- [Guide App](/docs/guide.html)
- [Home App](/docs/home.html)
- [Navigation App](/docs/navigation.html)

Additional documentation for the project can be found in the code comments.

## License

> Copyright © 2023 Haradhan Sharma

> This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


