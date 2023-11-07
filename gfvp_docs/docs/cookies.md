---
title: Technical Guide GF Cookies app of GFVP
summary: Here given overview of the accounts app of Green fuel validation platform.
copyright: (c) gf-vp.com
repo_url: https://github.com/haradhansharma/biofuel
edit_uri: blob/v24123/gfvp_docs/docs
authors:
    - Haradhan Sharma
date: 2023-10-16

---

# GF Cookies App

The GF Cookies app is a Django application designed to handle user consent for cookies. It allows users to either accept or decline the use of cookies and stores consent records in the database.

## Features

- Users can provide their consent for cookie usage.
- Consent records are stored in the database, including user information, session details, and the type of consent (accept or decline).
- A cookie is set for users who accept cookies with a one-year expiration.

## Installation

1. Clone the repository to your local machine:
2. Install the required dependencies:
3. Apply database migrations:
4. Start the Django development server:
5. Access the app in your web browser at [http://localhost:8000/cookie_consent](http://localhost:8000/cookie_consent).

## Usage

- Visit the `/cookie_consent` URL to manage cookie consent.
- Users can click the "Accept" or "Decline" button to provide their consent or decline cookies.
- Consent records are stored in the database for future reference.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Create a new branch for your changes.
4. Make your changes and commit them.
5. Push your changes to your fork on GitHub.
6. Create a pull request to submit your changes for review.

## Contributions

Contributions to enhance or expand this custom Django admin configuration are welcome. Feel free to submit pull requests with improvements, bug fixes, or additional features.



## Credits

This app is developed by [Haradhan Sharma](https://github.com/haradhansharma).

For more information, visit the [GF-VP website](https://www.gf-vp.com).
