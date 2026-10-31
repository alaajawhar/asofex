# Alarmifex positioning  (updated 2026-10-30)

## Statement
For young iPhone users who tune out the same default tones and can't put the songs, reels or clips they love into Apple's Clock app, Alarmifex is the custom alarm app that turns any sound into a real system alarm, trimmed to the exact part they want and ringing even on silent, unlike Alarmy and Loud Alarm (which sell punishment and noise) or music-service alarms (which need Spotify or Apple Music and a silent song playing all night).

## The one promise (screenshot 1)
"Any sound. Your alarm."
Why it stops the scroll: it names the thing Apple's Clock won't do in four words, and every neighbor in search sells loudness, missions or a music service. The subline makes it concrete with the audience's own objects: "Songs, reels, memes, speeches." Alternates kept: "Wake up to your sound" and "Make any sound your alarm". Avoid Mornova's "Wake up to any song."

## Supporting benefits (each maps to a real screen)
1. A reel becomes an alarm: share the link, the sound comes out. Screen: ReelImportView (trim and name after pulling the sound from a shared link) or SoundUploadView with a video picked.
2. Wake up to the best part: trim to the exact second, up to 1:00, with your own title and cover. Screen: AudioTrimmerView mid-edit (must-show).
3. It actually rings: on silent, through Focus, offline, app closed (AlarmKit). Screen: the system alarm alert on the Lock Screen showing a custom sound's alarm.
4. Every alarm, its own sound. Screen: Alarm list with several alarms, each with a different custom sound.
5. Your sounds in one place. Screen: Sounds tab with My Sounds (custom covers: a song clip, reel audio, a meme, a speech).
6. Not sure what to pick? 34 sounds by mood. Screen: Browse Categories (Calm, Energetic, Motivational...).
7. Wake up gradually with a Wake-up Series of alarms with different sounds. Screen: Wake-up Series editor/timeline.

## Tone
Is: playful, confident, plain. Never: preachy, scary, corporate. Banned words: seamless, powerful, ultimate, revolutionary, effortless, AI-powered, unleash, game-changer, "#1", "best", "loudest". No exclamation marks, no emoji. Sentence case.

## Objections and where the gallery answers them
| Objection | Screenshot |
|---|---|
| "Can't I just do this in Apple's Clock?" | 1 and 2: any sound, from a reel or file, not just iTunes tones |
| "Will it actually go off?" | 4: rings on silent, Focus, offline, app closed |
| "Is it fiddly to set up?" | 2 and 3: share a link, trim, done |
| "I don't have a sound in mind" | 7: 34 built-in sounds by mood |
| "I'll get used to it and sleep through it" | 5 or 8: a different sound per alarm, Wake-up Series |
| Price / paywall | not shown in screenshots (user decision); no "free" claims |

## Decisions log
- 2026-10-30: lead promise is "any sound becomes your alarm"; loud / rings on silent is the supporting proof (user choice).
- 2026-10-30: price and free tier are not mentioned in screenshots (user choice).
- 2026-10-30: deliverables iPhone 6.9" and iPad 13", 8 each, en-US. iPhone first; pause for user confirmation before iPad.
- 2026-10-30: export iPhone at 1320x2868 (accepted by Apple; 1260x2736 was rejected on a previous upload). iPad 2064x2752.
- 2026-10-30: render with Codex CLI built-in image_gen, upscale locally with finalize.py (no Higgsfield).
- 2026-10-30: no in-app voice recording exists; never claim or show recording. Voice only as an imported voice memo.
- 2026-10-30: character-led direction uses a "clock buddy" made from the app icon.
- 2026-10-30: storyboard of 8 approved as written.
- 2026-10-30: screenshot 3 subline changed to "Trim it to the exact second." (uploads have no 1:00 cap in code; the earlier line was untrue).
- 2026-10-30: screen 6 keeps the catalog (Calm) pending user review of IP; subline drops the unverified "34". Screen 2 uses the Add-a-sound capture, subline "Pull the sound from any video you saved.", pending user review.
- 2026-10-30: direction B (Night Signal) chosen for the set.
- 2026-10-30: user switched the set to direction C (Clock Buddy, mascot). C's existing screenshot 1 kept as 01 and style ref. B set archived in alternates/iphone-6.9-night-signal/.
- 2026-10-30: iPad 13 set rendered in direction C with Codex; sheet screens (add-sound, trimmer, editor) have the catalog background blurred and dimmed in the capture to hide third-party IP.
- 2026-10-30: iPhone set re-rendered fully with Codex (02,04-08 replaced WaveSpeed renders); WaveSpeed mix kept in alternates/iphone-6.9-wavespeed-mix.
