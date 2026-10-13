# LE Consent cookie library

The shared list of known cookies used by the [LE Consent](https://github.com/TevStack/le-consent) WordPress plugin on Local Eyes client sites.

Every site downloads `cookie-library.json` from this repo, via jsDelivr's free CDN, before each scheduled scan:

```
https://cdn.jsdelivr.net/gh/TevStack/le-consent-library@main/cookie-library.json
```

If the download fails or is invalid, sites keep using the copy bundled in the plugin. A newer library is only used if its `version` is higher than the bundled one.

## Adding a cookie

When a site finds a cookie it doesn't recognise, the alert email has a **Suggest for library** link. It opens an issue here, pre-filled with where the cookie was found and which script set it.

1. Work out what the cookie is. Search the name, and check the script that set it.
2. Add an entry to `cookies` in `cookie-library.json`:
   ```json
   { "name": "_lfa", "category": "marketing", "provider": "Lead Forensics", "processor": "leadforensics", "duration": "2 years", "description": "Identifies businesses visiting the site." }
   ```
   - **category** is one of `necessary`, `functional`, `analytics` or `marketing`.
   - **name** accepts `*` as a wildcard, e.g. `_hjSession_*`.
   - **processor** is optional. It links to a company in `processors`, which feeds the client's privacy policy. If the company is new, add it there with `name`, `purpose` and `privacy_url`.
3. If you know the script that sets it, add or extend an entry in `sources`. That's what lets the plugin **block** the script before consent.
   - **patterns** are matched against script and iframe URLs.
   - **inline** is matched against inline script code.
4. Bump `version` to today's date, e.g. `2026.10.14`. For a second change on the same day, use `2026.10.14.1`.
5. Commit to `main`. The **Validate library** check must pass. Then close the issue.

## When sites pick it up

- Sites check for a new library before each scheduled scan, and at most once a day otherwise. *Consent → Settings → Cookie library → Check now* forces a check.
- jsDelivr caches `@main` for up to 12 hours. To push a change out sooner, open https://purge.jsdelivr.net/gh/TevStack/le-consent-library@main/cookie-library.json
- Scans only use the library to categorise **new** cookies, or cookies still in *Uncategorised*. A cookie that already has a category on a site is never changed. This is by design.

## Checking locally

```
python scripts/validate.py
```
