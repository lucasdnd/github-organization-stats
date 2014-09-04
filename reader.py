from github import Github
import pymysql

#-------------------------------------------------------------------

def userExists(gh_user_id, cur):
  try:
    cur.execute("""SELECT gh_user_id FROM users WHERE gh_user_id = %s""", (gh_user_id))
    if len(cur.fetchall()) >= 1:
      return True
    return False
  except Exception as e:
    print "Error running userExists query for user " + str(gh_user_id)
    print e

#-------------------------------------------------------------------

def addUser(gh_user_id, name, conn, cur):
  try:
    cur.execute("""INSERT INTO users (gh_user_id, name) values (%s, %s)""", (gh_user_id, name))
    conn.commit()
    print "User " + name + " included"
  except Exception as e:
    print "Error running addUser query for user " + name
    print e

#-------------------------------------------------------------------

def repoExists(gh_repo_id, cur):
  try:
    cur.execute("""SELECT gh_repo_id FROM repos WHERE gh_repo_id = %s""", (gh_repo_id))
    if len(cur.fetchall()) >= 1:
      return True
    return False
  except Exception as e:
    print "Error running repoExists query for repo " + str(gh_repo_id)
    print e

#-------------------------------------------------------------------

def addRepo(gh_repo_id, gh_repo_name, gh_repo_description, conn, cur):
  try:
    cur.execute("""INSERT INTO repos (gh_repo_id, gh_repo_name, gh_repo_description) values (%s, %s, %s)""", (gh_repo_id, gh_repo_name, gh_repo_description))
    conn.commit()
    print "Repo " + gh_repo_name + " included"
  except Exception as e:
    print "Error running addRepo query for repo " + gh_repo_name
    print e

#-------------------------------------------------------------------

def addContribution(gh_user_id, gh_repo_id, w, a, d, c, conn, cur):

  # Get the local user and repo id
  userId = getLocalUserId(gh_user_id, cur)
  repoId = getLocalRepoId(gh_repo_id, cur)
  if userId == 0 or repoId == 0:
    print "Cannot add contrib. userId = " + str(userId) + ", repoId = " + str(repoId)
    return

  # Check if this contribution has already been made
  if contribExists(userId, repoId, w, cur):
    print "Contribution already exists"
    return

  # D-D-D-DROP THE BASS
  try:
    cur.execute("""INSERT INTO contribs (user_id, repo_id, w, a, d, c) values (%s, %s, %s, %s, %s, %s)""", (userId, repoId, w, a, d, c))
    conn.commit()
  except Exception as e:
    print "Error adding contribs for user " + str(userId) + " in repo " + str(repoId)
    print e

#-------------------------------------------------------------------

def contribExists(userId, repoId, w, cur):
  try:
    cur.execute("""SELECT user_id, repo_id, w FROM contribs WHERE user_id = %s AND repo_id = %s AND w = %s""", (userId, repoId, w))
    if len(cur.fetchall()) >= 1:
      return True
    return False
  except Exception as e:
    print "Error checking if contribution already exists for user " + str(userId) + ", repo " + str(repoId) + " and w " + str(w)
    print e

#-------------------------------------------------------------------

def addPunchCard(gh_repo_id, day, hour, commits, conn, cur):

  # Get the local repo id
  repoId = getLocalRepoId(gh_repo_id, cur)
  if repoId == 0:
    print "Could not get local repo id for " + str(gh_repo_id)
    return

  try:
    cur.execute("""INSERT INTO punchcard (repo_id, day, hour, commits) values (%s, %s, %s, %s)""", (repoId, day, hour, commits))
    conn.commit()
  except Exception as e:
    print "Error running addPunchCard query for repo " + str(gh_repo_id)
    print e

#-------------------------------------------------------------------

def getLocalUserId(gh_user_id, cur):
  try:
    cur.execute("""SELECT id FROM users WHERE gh_user_id = %s""", (gh_user_id))
    for row in cur.fetchall():
      return row[0]
      break
  except Exception as e:
    print "Error getting local user id for user " + str(gh_user_id)
    print e

#-------------------------------------------------------------------

def getLocalRepoId(gh_repo_id, cur):
  try:
    cur.execute("""SELECT id FROM repos WHERE gh_repo_id = %s""", (gh_repo_id))
    for row in cur.fetchall():
      return row[0]
      break
  except Exception as e:
    print "Error getting local repo id for repo " + str(gh_repo_id)
    print e

#-------------------------------------------------------------------

def addCommit(gh_user_id, gh_repo_id, sha, message, a, d, t, created_at, conn, cur):

  # Check if this commit already exits
  if commitExists(sha, cur):
    print "Commit " + sha + " already exists"
    return

  # Get the local user and repo id
  userId = getLocalUserId(gh_user_id, cur)
  repoId = getLocalRepoId(gh_repo_id, cur)
  if userId == 0 or repoId == 0:
    print "Cannot add commit. userId = " + str(userId) + ", repoId = " + str(repoId)
    return

  try:
    cur.execute("""INSERT INTO commits (user_id, repo_id, sha, message, a, d, t, created_at) values (%s, %s, %s, %s, %s, %s, %s, %s)""", (userId, repoId, sha, message, a, d, t, created_at))
    conn.commit()
    print "commit included"
  except Exception as e:
    print "Error adding commit for user " + str(userId) + " and repo " + str(repoId)
    print e

#-------------------------------------------------------------------

def commitExists(sha, cur):
  try:
    cur.execute("""SELECT sha FROM commits WHERE sha = %s""", (sha))
    if len(cur.fetchall()) >= 1:
      return True
    return False
  except Exception as e:
    print "Error checking if commit with sha " + str(gh_repo_id) + " exists"
    print e

#-------------------------------------------------------------------

def addWord(sha, message, conn, cur):
  for word in message.split(" "):
    try:
      cur.execute("""INSERT INTO words (sha, word) values (%s, %s)""", (sha, word))
      conn.commit()
    except Exception as e:
      print "Error adding word " + word + " in sha " + sha
      print e

#-------------------------------------------------------------------

def issueExists(repo_id, number, cur):
  try:
    cur.execute("""SELECT repo_id, num FROM issues WHERE repo_id = %s and num = %s""", (repo_id, number))
    if len(cur.fetchall()) >= 1:
      return True
    return False
  except Exception as e:
    print "Error checking if issue with number " + str(number) + " in repo " + str(repo_id) + " exists"
    print e

#-------------------------------------------------------------------

def addIssue(gh_repo_id, num, title, body, state, created_at, closed_at, conn, cur):

  # Get the local repo id
  repoId = getLocalRepoId(gh_repo_id, cur)
  if repoId == 0:
    print "Cannot add issue. repoId " + str(repoId) + " not in local db"
    return

  # Check if this issue already exists
  if issueExists(repoId, num, cur):
    print "Issue " + str(num) + " in repo " + str(repoId) + " already exists"
    return

  try:
    cur.execute("""INSERT INTO issues (repo_id, num, title, body, state, created_at, closed_at) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (repoId, num, title, body, state, created_at, closed_at))
    conn.commit()
  except Exception as e:
    print "Error adding issue " + str(num) + " in repo " + str(repoId)
    print e

#-------------------------------------------------------------------

def truncateDatabase(conn, cur):
  try:
    cur.execute("TRUNCATE TABLE users")
    cur.execute("TRUNCATE TABLE repos")
    cur.execute("TRUNCATE TABLE contribs")
    cur.execute("TRUNCATE TABLE punchcard")
    cur.execute("TRUNCATE TABLE commits")
    cur.execute("TRUNCATE TABLE words")
    cur.execute("TRUNCATE TABLE issues")
    conn.commit()
    print "Database clean"
  except Exception as e:
    print "Error running truncates"
    print e

# Script -----------------------------------------------------------

# Database connection
conn = pymysql.connect(host='127.0.0.1', port=3306, user='gh', passwd='gh', db='github', charset='utf8')
cur = conn.cursor()

# truncateDatabase(conn, cur)

# Connect to Github
g = Github("ENTER YOUR ACCESS TOKEN HERE")

# Access your Organization here (or include it in the loop below if you have more than one)
orgs = g.get_user().get_orgs()
repos = orgs[0].get_repos()

# Loop through!
for repo in repos:

  # Access the repo and add it to the database, if needed
  print
  print "Checking if " + repo.name + " exists in the database..."
  if not repoExists(repo.id, cur):
    print "Repository does not exist. Including it..."
    addRepo(repo.id, repo.name, repo.description, conn, cur)

  # Access the repo issues
  try:
    issues = repo.get_issues(state="all")
  except:
    print "Something wrong getting issues for " + repo.name
    continue;

  # Add the issues
  if not issues is None:
    for issue in issues:
      try:
        print "Adding issue " + str(issue.number)
        addIssue(repo.id, issue.number, issue.title, issue.body, issue.state, issue.created_at, issue.closed_at, conn, cur)
      except Exception as e:
        print "Something wrong reading issue!"
        print e

  # Access the repo stats
  try:
    stats = repo.get_stats_contributors()
  except Exception as e:
    print "Something wrong getting contributions for " + repo.name
    continue
  if stats is None:
    print "Stats for " + repo.name + " is None"
    continue

  # Contributions in 'master'
  for contrib in stats:

    authorName = ""
    try:
      authorName = contrib.author.name
    except Exception as e:
      print "Something wrong getting author name here"
      continue
    if authorName is None:
      print "Author name is None"
      continue

    # Access the user contributions, and add it if it doesn't exist yet
    print "Checking if " + authorName + " exists in the database..."
    if not userExists(contrib.author.id, cur):
      print "User does not exist. Including it..."
      addUser(contrib.author.id, authorName, conn, cur)

    # Add the user contributions
    for week in contrib.weeks:
      addContribution(contrib.author.id, repo.id, week.w, week.a, week.d, week.c, conn, cur)
    print "All contributions added"

  # Get the Punch Card data
  print "Reading punch card data for " + repo.name
  try:
    punchCard = repo.get_stats_punch_card()
  except Exception as e:
    print "Something wrong getting punch card data for " + repo.name
    print e
  if not punchCard is None:
    for day in range(0, 7): # Day of week
      for hour in range(0, 24): # Hour of day
        commits = punchCard.get(day, hour)
        addPunchCard(repo.id, day, hour, commits, conn, cur)
    print "Punch card done for " + repo.name

  # Get all the commits
  print "Reading commits data for " + repo.name
  try:
    commits = repo.get_commits()
  except Exception as e:
    print "Something wrong getting commits for " + repo.name
    print e
  if not commits is None:
    for commit in commits:
      try:
        addCommit(commit.author.id, repo.id, commit.sha, commit.commit.message, commit.stats.additions, commit.stats.deletions, commit.stats.total, commit.commit.author.date, conn, cur)
        addWord(commit.sha, commit.commit.message, conn, cur)
      except Exception as e:
        print "Something wrong reading commit stuff"
        print e

print "Done"

# Close the database connection
cur.close()
conn.close()
