\# Security Code Review Report



\## CODSOFT Internship - Task 3



\### Project: Secure Code Review of a Python Flask Application



\---



\## 1. Objective



The objective of this security review was to examine a Python Flask web application for common security weaknesses and coding flaws.



The application was reviewed using:



\- Manual source-code analysis

\- Bandit static security analysis

\- Secure coding practices

\- Comparison between vulnerable and secure implementations



The vulnerable application was created as a controlled local demonstration and was not deployed to a public server.



\---



\## 2. Technologies Used



\- Python 3

\- Flask

\- SQLite

\- Bandit

\- Werkzeug Security

\- Regular expressions

\- Python Socket library



\---



\## 3. Security Review Methodology



The following process was used:



1\. Review the application source code manually.

2\. Identify potentially unsafe coding practices.

3\. Run Bandit static code analysis.

4\. Document identified vulnerabilities.

5\. Implement secure coding improvements.

6\. Run Bandit against the secure implementation.

7\. Compare the security results.



\---



\## 4. Vulnerabilities Identified



\### Finding 1 - SQL Injection



\*\*Severity:\*\* High



\*\*Location:\*\* `vulnerable\_app.py`



The vulnerable application constructed an SQL query by directly concatenating user-controlled input.



Example:



```python

query = (

&#x20;   "SELECT \* FROM users "

&#x20;   "WHERE username = '" + username +

&#x20;   "' AND password = '" + password + "'"

)

