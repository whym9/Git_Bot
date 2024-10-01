# GitHub Management Telegram Bot

## Overview
This bot provides GitHub integration, allowing users to authenticate with GitHub and manage their repositories from Telegram. The bot supports viewing repository details, pull requests, issues, and more.

## Features
- GitHub OAuth2 Authentication
- Rate-limiting using Redis
- GitHub repository management (view pull requests, issues, etc.)
- Daily and monthly request reset using scheduled jobs
- Scalable using Docker and Redis

## Setup

### Prerequisites
1. Python 3.8+
2. Redis for rate-limiting
3. Docker (optional)

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/your-repo/telegram-github-bot.git

2. Install dependancies:
    ```bash
   pip install -r requirements.txt
    ```

3. Set environment variables for GitHub OAuth2:
    ```bash
    export GITHUB_CLIENT_ID=<your_client_id>
    export GITHUB_CLIENT_SECRET=<your_client_secret>
    export BOT_TOKEN=<your_bot_token>
    ```

4. Run the bot:
    ```bash
    python main.py
    ```

# Usage
Once the bot is running, use commands like /start, /login, and /repos to interact with your GitHub account.

# Rate-limiting
The bot uses Redis for rate-limiting. You can adjust rate limits by modifying the config.json.

# Docker Setup
To run the bot in Docker:
    
    docker-compose up

This will set up a Redis instance and 6 replicas of your bot.

#### b. **Adding Unit Tests**
Testing is essential for reliability and maintainability. You can use **pytest** for your bot. Below is a basic example to test GitHub API interactions:

```python
import pytest
from bot import get_github_repos

def test_get_github_repos(mocker):
    # Mock GitHub API response
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=lambda: {"data": "mocked"}))

    response = get_github_repos("mocked_token")
    assert response == {"data": "mocked"}
```
# GitHub Actions for CI/CD
Add a simple GitHub Actions workflow to run your tests on each push:
```yaml
name: Python CI

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.x
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest
```
