
<div align="center">
    <img src="https://i.imgur.com/2rvvPvi.png" alt="Discord Relay Bot" width="100" />
    <h1>Discord Relay Bot</h1>
</div>
<div align="center">

[![Follow @saple1337](https://img.shields.io/badge/Follow-@saple1337-181717?style=for-the-badge&logo=github)](https://github.com/saple1337)
[![Star](https://img.shields.io/badge/Star-Repo-181717?style=for-the-badge&logo=github)](https://github.com/saple1337/RelayDiscord)
[![Fork](https://img.shields.io/badge/Fork-Repo-181717?style=for-the-badge&logo=github)](https://github.com/saple1337/RelayDiscord/fork)
[![Watch](https://img.shields.io/badge/Watch-Repo-181717?style=for-the-badge&logo=github)](https://github.com/saple1337/RelayDiscord/subscription)
[![Buy Me a Coffee](https://i.imgur.com/mYcE2J8.png)](https://www.buymeacoffee.com/saple1337)

</div>


Welcome to the **Discord Relay Bot**! This bot helps you relay important game information to authorized Discord servers with ease. Follow the steps below to get started with setting up and using the bot.


## 🚀 Installation

### Prerequisites
Make sure you have the following installed:
- [Python 3.8+](https://www.python.org/downloads/)
- [discord.py](https://pypi.org/project/discord.py/)
- [aiohttp](https://pypi.org/project/aiohttp/)


### Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

## 🛠 Configuration

### `relay_config.json`
This file stores the bot configuration. Update it with your bot's token, activity status, and DM response.

```json
{
    "token": "",
    "prefix": "!",
    "activity": "",
    "dm_response": "Message relayed to all webhooks except your own.",
    "image_directory": "./images/"
}
```

### `relay_whitelist.json`
This file manages the whitelist of authorized users and servers.

```json
{
    "servers": [
        {
            "server_name": "Placeholder",
            "authorized_users": [
                "Placeholder",
                "Placeholder"
            ],
            "server_link": "",
            "webhook_link": "",
            "server_image": "https://i.imgur.com/"
        },
        {
            "server_name": "Placeholder",
            "authorized_users": [
                "Placeholder"
            ],
            "server_link": "",
            "webhook_link": "",
            "server_image": "https://i.imgur.com/"
        }
    ]
}

```

## ▶️ Running the Bot

Run the bot using the following command:

```bash
python relay.py
```

The bot will start and log into your Discord server, displaying the activity specified in `relay_config.json`.

## 💻 Usage

1. **DM the Bot:** Start a conversation by sending a DM to the bot with the game information.
2. **Respond to Prompts:** The bot will prompt you for the game name, hosting time, and any additional information.
3. **Automatic Relay:** If you’re authorized, the bot will automatically relay the message to other servers in the whitelist.

### Cooldown
Each user is subject to a 3-hour cooldown between message relays to prevent spam.

## 🤝 Contributing

Feel free to contribute to the project by submitting a pull request. All contributions are welcome!

For any questions or issues, reach out via my [profile](https://github.com/saple1337).
