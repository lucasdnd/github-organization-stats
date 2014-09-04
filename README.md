github-organization-stats
=========================

Python+MySQL scripts to collect and analyze information about your Github organizations

#### Setup

1. Create a Github access token in the [Github settings](https://github.com/settings/applications). Make sure you grant it the `repo` and `user` scopes.

1. Install [PyGithub](http://jacquev6.github.io/PyGithub/v1/introduction.html) using `sudo easy_install PyGithub`

2. Install PyMySQL using `sudo pip install PyMySQL`

3. Run the `db.sql` script on your MySQL instance

4. Open `reader.py` and add your access token where it says "ENTER YOUR ACCESS TOKEN HERE"

5. Run `reader.py` to drop the bass. It may take many hours to finish, depending on how many repos/users your orgs have

6. Run the queries in `fun.sql` to have fun
