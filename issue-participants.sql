SELECT
  actor.login,
  COUNT( actor.login ) c
FROM
  [githubarchive:year.2017]
  [githubarchive:year.2018]
  [githubarchive:month.201901] 
  [githubarchive:month.201902] 
  [githubarchive:month.201903] 
  [githubarchive:month.201904] 
WHERE
  repo.name = 'ethereum/go-ethereum'
  AND type = 'IssueCommentEvent'
GROUP BY
  actor.login
ORDER BY
  c DESC
LIMIT
  10