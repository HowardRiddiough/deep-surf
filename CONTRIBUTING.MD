# Contributing code
I follow a strict pull request process. Work in short-lived branches and submit a pull request when ready. 

# Code style
PEP 8 with the following modifications:

line length = 110 rather than 79 (also configured in file .flake8)
Google DocStrings
PEP 8 doesn't have a strong opinion on whether " or ' I have opted to use " to align with code formatter 
black. 

# Pre-commit checks
Before each commit, ensure all tests pass and there are no flake8 warnings.

# Running tests
In root of repo, simply run pytest.