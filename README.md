# Google Apps Script Sync

<p align="center">
    <img src="https://travis-ci.com/atom-tr/apps-script-sync.svg?branch=master"/>
    <img src="https://codecov.io/gh/atom-tr/apps-script-sync/branch/master/graph/badge.svg"/>
</p>

----

<p align="center">
   <img src="https://img.shields.io/badge/language-python-blue?style"/>
   <img src="https://img.shields.io/github/license/atom-tr/apps-script-sync"/>
   <img src="https://img.shields.io/github/stars/atom-tr/apps-script-sync"/>
   <img src="https://img.shields.io/github/forks/atom-tr/apps-script-sync"/>
   <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
</p>
<p align="center">
   Are you tired of copy-pasting your code to script.google.com? <br>
   This tool will help you to sync your files to script.google.com project.
</p>

<p align="center">
    <a href="https://github.com/atom-tr/apps-script-sync/issues">Report Bug</a>
    ·
    <a href="https://github.com/atom-tr/apps-script-sync/issues">Request Feature</a>
  </p>

## Prerequisites

1. Create a new Google Apps Script project at <https://script.google.com/home>.
    - Get the project ID from the URL. It is the string between `/d/` and `/edit`.
2. Follow the instructions at <https://developers.google.com/apps-script/api/quickstart/python> to:
    - Enable the Google Apps Script API for your project
    - Download the `credentials.json` file to your computer
    - Get the `token.json` file.
3. You will need a GitHub token with `repo` scope. You can create one at <https://github.com/settings/tokens>
    > enabling the repo scope seems **DANGEROUS**
	but this is the only way to access the repository files and sync them to Google Script.
4. Save secrets in your repository settings.
	- `GH_TOKEN`: GitHub token
	- `PROJECT_ID`: Google Script project ID
	- `CLIENT_ID`: Google app client ID
	- `CLIENT_SECRET`: Google app client secret
	- `REFRESH_TOKEN`: Google app refresh token

## Workflow

First, you need to create a new repository for your project. Then, you need to create a new workflow file in `.github/workflows` folder. You can use the following template:

```yaml
name: Sync to script.google

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.11"]

    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: atom-tr/apps-script-sync@main
        with:
          # Github
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
          # Google Script
          PROJECT_ID: ${{ secrets.PROJECT_ID }} # Project ID, you can get it from the URL of your project
          PROJECT_PATH: # Project path, where the folder in repo will be synced to in Google Script, default is src
          # Google app
          # CLIENT_TYPE: installed
          CLIENT_ID: ${{ secrets.CLIENT_ID }}
          CLIENT_SECRET: ${{ secrets.CLIENT_SECRET }}
          REFRESH_TOKEN: ${{ secrets.REFRESH_TOKEN }}
```

When you push your code to the repository, the workflow will be triggered and it will sync your code to Google Script.
