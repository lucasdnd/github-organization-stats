-- Fun queries you can run:

-- All meaningful contributions (a, d, c > 0) by all users in all repos
select users.name, repos.gh_repo_name, w, a, d, c from contribs inner join users on contribs.user_id = users.id inner join repos on contribs.repo_id = repos.id where a > 0 or d > 0 or c > 0;

-- Users with most commits
select users.name, sum(c) commits from contribs inner join users on contribs.user_id = users.id where a > 0 or d > 0 or c > 0 group by users.name order by sum(c) desc;

-- Repositories most worked on
select repos.gh_repo_name, sum(c) commits, sum(a) additions, sum(d) deletions from contribs inner join repos on contribs.repo_id = repos.id where a > 0 or d > 0 or c > 0 group by repos.gh_repo_name order by sum(c) desc, sum(a) desc, sum(d) desc;

-- Most common words in commit messages
select lower(word), count(lower(word)) from words
where word not in('merge', 'of', 'branch', 'to', 'on', '\'master\'', 'and', 'in', 'for', '-', 'de')
group by lower(word) order by count(lower(word));

-- Commits on weekends
select sum(commits) commits_on_weekends from punchcard where day = 0 or day = 6;

-- Commits throughout the day
select concat(hour, "-", hour+1) hour_of_day, sum(commits) commits from punchcard group by hour;

-- Who made most commits on weekends
select users.name, count(commits.created_at) commits_on_weekends from commits inner join users on commits.user_id = users.id where dayofweek(commits.created_at) = 1 or dayofweek(commits.created_at) = 7 group by users.name order by count(commits.created_at) desc;

-- Top 10 repos with most open issues
select r.gh_repo_name, count(i.id) from issues i inner join repos r on i.repo_id = r.id where i.state = 'open' group by r.id order by count(i.id) desc limit 10;

-- Issues closed by time of day
select concat(hour(time(created_at)), '-', hour(time(created_at))+1) time, count(*) issues_closed from issues where state = "closed" group by hour(time(created_at));

-- Average days to close recent issues (<= 7 days)
select

  gh_repo_name repo,

  avg(datediff(closed_at, created_at)) avg_days_to_close_issue

  from issues i
  inner join repos r on i.repo_id = r.id
  where created_at >= adddate(now(), INTERVAL -7 DAY)
  and closed_at >= adddate(now(), INTERVAL -7 DAY)
  group by gh_repo_name
  order by avg(datediff(closed_at, created_at))
  limit 100;
