# Ninbot

Ninbot is a collection of Discord-Bots I have written for a small server with my friends.

## log_bot

This Bot simply saves every message, that is sent, edited or deleted.

## poll_bot

This Bot adds reactions to messages in certain channels, where voting is encouraged and enables custom polls in the poll channel.

## shitcoin_bot

This Bot enables server members to earn "Shitcoin" (SC). They can then gamble with them to reach the top of the leaderboard.

### Commands (user)

|command|function|
|-------|--------|
|bal|shows the users current balance|
|bet \[value\]|user buys a 'lottery ticket' for given value|
|daily|grants the user a random amount of SC; once per day|
|gift \[target\] \[amount\]|gifts the target the specified amount of SC|
|steal \[target\]|user spends some SC in order to have a chance to steal from the target.|
|top|shows the current and all-time leaderboards|

### Commands (developer)

|command|function|
|-------|--------|
|add_user \[target\]|adds target to the system|
|data_reset|resets all user data|
|set \[user\] \[amount\]|sets the balance of the user to the specified amount|
|show_data|shows all stored user data|

## Documentation

[discord.py](https://discordpy.readthedocs.io/en/stable/)
