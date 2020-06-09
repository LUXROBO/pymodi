Contributing
============
Contributions are welcomed, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Types of Contributions
----------------------

### Report Bugs
Report bugs at <https://github.com/LUXROBO/pymodi/issues>. Fill in all the information required at issue template.

### Fix Bugs
Look through the GitHub issues for bugs. You are welcome to implement anything tagged with \"bug\"
and \"help wanted\".

### Implement Features
Look through the GitHub issues for features. You are welcome to implement anything tagged with \"bug\"
and \"help wanted\".

### Write Documentation
PyMODI could always use more documentation, whether it be part of the
official PyMODI docs, docstrings, or even blog posts,
articles, and such.

### Submit Feedback
The best way to send feedback is to file an issue at

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible to make it easier to
    implement.
-   Remember that this is a volunteer-driven project and that
    contributions are welcome :)

Pre-requisites
-------------
You should be familiar with the following items.

1. git-flow
2. python unit-test
3. git commit message naming convention
4. docstring
5. python type annotations

Getting Ready for PyMODI Contribution
--------------------------------
Please read the following to get ready for the contribution!!

1. Fork the pymodi repo on GitHub

    [![Fork PyMODI](https://github.com/k2sebeom/pymodi/blob/feature/refactor-contribution-guideline/docs/_static/img/Fork_btn.JPG)](https://github.com/LUXROBO/pymodi/fork)

     ^ Click this to fork the repo!!

2. In your device, clone your fork locally:

        $ git clone git@github.com:your_name_here/LUXROBO/pymodi.git

3. Install the version of PyMODI in your branch:

        $ python setup.py develop

4. Setup the git hooks to facilitate contribution:

        $ git config core.hooksPath .githooks

5. Do NOT manipulate master branch or develop branch directly. Create a new branch for local development.

    PyMODI's branch naming convention follows a git-flow convention,

    If you fixed a bug:

        $ git checkout -b hotfix/name-of-your-bug-fix

    If you implemented a new feature:

        $ git checkout -b feature/name-of-your-feature

6. Whenever you make major changes, make a commit to the repository:

        $ git add file-you-have-changed
        $ git commit -m your-commit-message

    PyMODI contribution follows a git naming convention for the commit messages.
    https://chris.beams.io/posts/git-commit/

    TL;DR: When writing a commit message, imagine your message is preceded by

    "This commit will... your-commit-mesage"

    e.g.

        $ git commit -m "Fix error in motor module communication"
        $ git commit -m "Refactor contribution document"
        $ git commit -m "Remove redundant import in modi.py"

7. After you push your changes to local branch, make sure your code passes
all unittests and flake8 convention tests. If you have set your githooks path at step 4,
git will automatically run the tests when you push your changes.

8. Make a pull request to LUXROBO/pymodi/develop branch.

    ![PR guide](https://github.com/k2sebeom/pymodi/blob/feature/refactor-contribution-guideline/docs/_static/img/PR_guide.png)

   Name the pull request based on the default PR templates. Choose either of the templates based on the type of your contribution.

9. Congratulations! You made a meaningful contribution to PyMODI.

<p align="center">
    <img src="https://github.com/k2sebeom/pymodi/blob/feature/refactor-contribution-guideline/docs/_static/img/modi_thank.JPG" alt="thanks" width=300, height=180>
</p>

Tips
----
To run a subset of tests:

    $ python -m unittest tests.test_modi
    
To automatically intialize the MODI object in an interactive shell:

    $ python -im modi -n <nb_modules>

Contact Us
---
If you have any questions regarding PyMODI, contact us at <mailto> tech@luxrobo.com </mailto>
