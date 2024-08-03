# Ninbot

Ninbot is a collection of Discord-Bots I have written for a small server with my friends.

## log_bot

This Bot simply saves every message that is sent to text files.

## poll_bot

This Bot adds reactions to messages in certain channels, where voting is encouraged.

## shitcoin_bot

This Bot enables server members to earn "Shitcoin" (SC). They can then gamble with them to reach the top of the leaderboard.

### Commands (user)

|command|function|
|-------|--------|
|bal|shows the users current balance|
|cf \[amount\]|coin flip: user receives/loses their wager|
|cf_history|DEBUG: shows number of logged coin flips, succesfull coinflips and average pivot value|
|daily|grants the user a random amount of SC; once per day|
|gift \[target\] \[amount\]|gifts the target the specified amount of SC|
|top|shows the current leaderboard|

### Commands (developer)

|command|function|
|-------|--------|
|data_reset|resets all user data|
|set \[user\] \[amount\]|sets the balance of the user to the specified amount|
|show_data|shows all stored user data|

## Documentation

[discord.py](https://discordpy.readthedocs.io/en/stable/)