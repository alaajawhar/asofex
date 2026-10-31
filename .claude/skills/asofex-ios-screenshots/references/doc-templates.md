# Document templates (output/<app>/docs/)

Write these before any rendering, right after the intake is confirmed and research is done. Keep them current: whenever the user adds information, a capture reveals something, or a decision changes, update the relevant file the same turn. They are the source of truth a later run reads first.

## research.md
```
# <App> research  (updated YYYY-MM-DD)
## Inputs received
- <what the user gave, with paths and URLs>
## Audience
- Who: ...
- Search intent and phrases: ...
- Pains (their words): 1. "..." 2. "..." 3. "..."
- Desired outcomes: ...
## App as it is today
- Store page: subtitle, first 3 lines of description, rating, review count, what's new
- Current screenshots: what they say, what is weak
- Review themes: praise / complaints (quotes)
## Competitors
| App | Screenshot 1 headline | Proof used | Visual style | Weakness we exploit |
## Category conventions
- Respect: ...
- Break: ...
## Proof inventory (only verified)
- ...
## Open questions
- ...
```

## positioning.md
```
# <App> positioning  (updated YYYY-MM-DD)
## Statement
For <audience> who <pain>, <App> is the <category> that <outcome>, unlike <alt> which <weakness>.
## The one promise (screenshot 1)
"..."  Why it stops the scroll: ...
## Supporting benefits (each maps to a real screen)
1. ... -> screen: ...
2. ...
3. ...
## Tone
Is: <3 adjectives>. Never: <3 words>. Banned words: ...
## Objections and where the gallery answers them
| Objection | Screenshot |
## Decisions log
- YYYY-MM-DD: ...
```

## copy.md
```
# <App> screenshot copy and storyboard  (updated YYYY-MM-DD)
Devices: iPhone 6.9" 1320x2868, iPad 13" 2064x2752. Locales: en-US. Engine: <codex|openai|gemini|higgsfield>.
Direction: mascot, <character name> (see Direction below)

| # | Role | Headline | Subheadline | Proof | Capture | Layout |
|---|------|----------|-------------|-------|---------|--------|
| 1 | Hook | ... | ... | ... | none / home.png | no-UI hero |
...
## Rationale per screenshot
1. ...
## Alternates (for A/B tests)
1. a) ... b) ...
## Direction (mascot)
- Vibe: ...
- Background and ground shapes (hex): ...
- Typography: ... Accent color: ...
- Device treatment: tilted ~10 degrees, alternating
- Mascot: source (existing / icon turned character / invented), look, size, palette
## Pose arc
| # | Pose (acts out the headline) | Prop |
## Localization
| # | en-US headline | <locale> headline | <locale> sub |
```
