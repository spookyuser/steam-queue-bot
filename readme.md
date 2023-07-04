# Steam Queue Bot

A work in progress python script that can be used with github actions to automatically clear your steam queue, so that you can get your free trading cards during a sale event.

## Status

I'm still in the process of testing this script and I'm not even sure if its working at all yet because I keep accidentally clearing my queue :(

On top of that I don't know how robust the method of using steam cookies for authentication is. According to https://dev.doctormckay.com/topic/365-cookies/ cookies can expire for many reasons. But my hope is that they will be able to last for the short time steam sales last. So a possibility is the script might end up working - but only for a day.

Right now i'm just parsing the entire cookie string stored on the steam page so that the script doesn't need to be updated when cookie names change. So the `STEAM_COOKIE` secret needs to be a plain cookie string like "cookie1=value1; cookie2=value2; cookie3=value3;". I'm not sure if this is the best way to do it, but it works for now.

## Dependencies

Python 3.11

## Instructions

1. Go to https://store.steampowered.com/ in your browser and log in to steam
2. Press F-12 to open up the developer tools of your browser
3. Either copy the entire cookie string from a request header to `store.steampowered.com/explore` (like from the network tab) or use this [chrome extension to do it](https://chrome.google.com/webstore/detail/storageace/cpbgcbmddckpmhfbdckeolkkhkjjmplo) (set the export type to key=value)

You can now either run the script _locally_ or as a _github action_.

**Github Actions:**

The script comes with a github action that is scheduled to run once a day automatically, or manually via workflow runs. To set this up you need to:

- Fork this repo
- Create a secret called `STEAM_COOKIE` and paste the value of the cookie you copied earlier into it
- The script should now automatically run once a day, be sure to disable the action when the sale is over
- ??? Profit

**Locally:**

- export an env variable called `STEAM_COOKIE` with the value of the cookie you copied earlier
- run `python queue-bot.py`

**GH cli:**
Oh and you could also use the GH cli to set the secret instead.
And run it manually if you want

- Set cookie
  - `gh secret set STEAM_COOKIE -b "<paste your cookie here>"`
  - `gh secret set STEAM_COOKIE -b "$(pbpaste)"` (mac)(paste this command first lol)
- Run workflow manually
  - `gh workflow run queue-bot.yml`

## TODO

- Is there a way i could get this to disable automatically when the sale is over?
