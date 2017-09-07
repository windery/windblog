# windblog

A blog app written with flask.

### **feature**
* Posts
  * Markdown
  * Code Highlighting
  * Dispus Comment
  * Tags

* Download Proxy
* File Upload/Download

### usage
1. add "WINDBLOG_DB_URI=sqlite:////path/to/dbfile" "WINDBLOG_ADMIN_PASSWORD=your_password" environment variable
2. ./manage.py db init && ./manage.py db migrate && ./manage.py db upgrade
3. access http://127.0.0.1/init
4. access http://127.0.0.1/admin to login


