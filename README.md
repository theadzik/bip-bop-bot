# MeaningOfWordsBot

[u/MeaningOfWordsBot](https://www.reddit.com/user/MeaningOfWordsBot/)
uses OpenAI to correct some of the most common mistakes
in Polish language posted on [r/Polska](https://www.reddit.com/r/Polska/).

---

## Deployment

This bot runs on my [homelab](https://github.com/theadzik/homelab)
kubernetes cluster.

Before the bot can be deployed, the database must exist.
The script is available here: [./scripts/created-db.py](./scripts/create-db.py).

## Config

Config files in this repo were at some point used in
production, but should be treated as examples. The actual,
live configuration is available in
[theadzik/homelab](https://github.com/theadzik/homelab/tree/main/manifests/base/reddit-meaningofwords/configs)
repository.
