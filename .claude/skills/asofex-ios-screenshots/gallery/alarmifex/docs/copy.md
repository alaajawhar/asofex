# Alarmifex screenshot copy and storyboard  (updated 2026-10-30)
Devices: iPhone 6.9" 1320x2868 (done), iPad 13" 2064x2752 (done, direction C, Codex). Locales: en-US.
Direction chosen: C. Clock Buddy (user switched from B on 2026-10-30; B set kept in alternates/iphone-6.9-night-signal). Storyboard approved by the user 2026-10-30.

| # | Role | Headline | Subheadline | Proof | Capture | Layout |
|---|------|----------|-------------|-------|---------|--------|
| 1 | Hook | Any sound. *Your* alarm. | Songs, reels, memes, speeches. | none | my-sounds.png (My Sounds list, 6 custom sounds with covers) | text top, phone tilted, cropped bottom |
| 2 | Core job (reel) | Saved a reel? Make it *ring*. | Pull the sound from any video you saved. | none | add-sound.png ("Bring in a sound." Audio file / Video; user to review) | text top, phone mirrored tilt |
| 3 | Trimmer (must-show) | Wake up to the *best part* | Trim it to the exact second. | 0:40 to 1:20 selection visible in UI | trimmer.png (AudioTrimmerView mid-edit with title and cover) | device top, text bottom |
| 4 | Reliability proof | It rings. Even on *silent*. | Through Focus, offline, app closed. | product proof (AlarmKit) | lock-alarm.png (AlarmKit full-screen alert "Nap's over" 5:13) | text top, phone straight |
| 5 | Personal | Every alarm, its *own* sound | Hype on weekdays. Calm on Sundays. | none | alarms.png (6 alarms incl. "Easy mornings" series; labels Leg day, Sunrise run, Class at 8, Sunday slow, Game day) | text top, phone tilted |
| 6 | Breadth | No sound in mind? Pick a *mood*. | Ready-made sounds for every mood. | none | moods.png (Calm category; user to review catalog IP) | device top, text bottom |
| 7 | Differentiator | Wake up in *waves* | A series of sounds, 15 minutes apart. | none | series.png (Timeline: 6:00 Sunday Vinyl, 6:15 Rooftop Sunrise, 6:30 Crowd Goes Wild) | text top, phone mirrored tilt |
| 8 | Close | Make tomorrow sound like *you* | Set your first sound tonight. | none | editor.png (Edit Alarm 6:30 AM "Sunrise run", weekdays, Rooftop Sunrise, volume high) | text top, phone straight |

## Rationale per screenshot
1. The search-results hook. Names the one thing Apple's Clock won't do, in four words, with the audience's own objects in the subline. Neighbors sell loudness, missions or a music service.
2. The share-a-reel flow is the most "new" thing in the category (Mornova and Video Alarm don't show it). Concrete action, not a feature name.
3. Must-show. "Best part" is the emotional payoff of trimming (the drop, the chorus, the punchline); the subline carries the spec.
4. Answers the #1 category fear in competitor reviews ("DO NOT RELY ON THIS TO WAKE YOU UP", "silent song all night"). Proof by product mechanism, since we have no ratings to show.
5. Habituation pain from the site ("you stopped hearing your alarm") turned positive; specific days make it real.
6. Covers the "I don't have a sound" objection; a number gives specificity.
7. Wake-up Series is unique; "waves" frames it as gentle without being preachy.
8. Close: borrows the site's line, CTA verb in the subline. No price, no "free".

## Alternates (for A/B tests)
1. a) Any sound. *Your* alarm. b) Wake up to *your* sound c) Make any sound your *alarm*
2. a) Saved a reel? Make it *ring*. b) From reel to *alarm* c) That reel? Your *alarm* now.
3. a) Wake up to the *best part* b) Keep just the *drop* c) Cut it to the *second*
4. a) It rings. Even on *silent*. b) Silent switch? Still *rings*. c) No Wi-Fi? Still *rings*.
5. a) Every alarm, its *own* sound b) Never tune it *out* c) New sound, every *morning*
6. a) No sound in mind? Pick a *mood*. b) 34 sounds by *mood* c) Calm, hype or *motivated*
7. a) Wake up in *waves* b) One alarm *isn't enough* c) Ease in, sound by *sound*
8. a) Make tomorrow sound like *you* b) Your morning, your *sound* c) Set it *tonight*

## Captures (Phase 4)
Device: iPhone 17 Pro Max simulator "Alarmifex Shots 17PM" (6DBB1667-BEDD-419B-BA00-C61E75CFFEC4), iOS 27.0, light theme, status bar 9:41. Launched with `-skipOnboarding -screenshotPremium` (TEMP DEBUG flags: premium state + production catalog; remove from the iOS repo after capture).
Demo content: custom sounds made from royalty-free audio, cover art generated for this purpose (no real people, no brands). Titles: "Rooftop Sunrise", "Neon Anime Opening", "Stair Sprint Speech", "Yawning Cat Meme", "Sunday Vinyl", "Crowd Goes Wild".

Spares: choose-sounds.png (series pick step, sounds numbered 1-3), sounds-feed.png.
Notes found during capture: the catalog contains third-party IP (celebrities, Squid Game, Minions, Windows 10, anime art); custom sounds show the subtitle "classic" in the series timeline (likely an app label bug); "34 sounds" was not verifiable from code, so screen 6 uses no number; uploads have no 1:00 trim cap.

## Directions
### A. Sunrise Gradient: bright, confident, brand-led
Background: diagonal gradient violet #6C38FC to blue #0A7AFD to cyan #02CEF0, large low-contrast waveform bars behind the phone. Type: heavy geometric sans (Manrope ExtraBold style), white, accent word pale cyan #BFF6FF. Device: silver iPhone 17 Pro Max, tilted ~10 degrees, edge-cropped. Decoration: waveform bars from the icon. Proof style: product specifics in sublines. Spec: renders/iphone-6.9/dirA/spec.json
### B. Night Signal: premium, dark, calm before the alarm
Background: navy #0B1020 to #141B3A, concentric rings and thin waveform strokes in violet-to-cyan behind the phone. Type: heavy geometric sans, white, accent word filled violet-to-cyan gradient; sub #A9B3D1. Device: black titanium, tilted, edge-cropped. Spec: renders/iphone-6.9/dirB/spec.json
### C. Clock Buddy (character-led): playful, warm
Background: off-white #FEFDFD with two flat ground hills (lavender #E6DEFF, sky #D6E8FF). Character "Buddy": round alarm clock from the app icon, violet/cyan bells, violet-blue-cyan gradient body, white face, navy dot eyes, mouth made of five tiny waveform bars, stubby arms, flat, ~22% of canvas height, overlapping a bottom corner of the phone. Type: heavy rounded geometric sans, navy #0B1020, accent violet #6C38FC. Device: silver, tilted ~10 degrees, alternating direction across the set.
Pose arc (one per screen): 1 dancing with headphones and music notes; 2 holding a tiny film-clip/clapper slate, pulling a sound wave out of it; 3 holding giant scissors snipping a waveform ribbon; 4 bells ringing hard, eyes wide, standing over a "mute" switch it ignores; 5 holding a stack of small cards with different note symbols; 6 thinking, chin on hand, three colored mood bubbles (no text); 7 surfing a gentle sound wave; 8 waving goodnight with a crescent moon behind.
Spec: renders/iphone-6.9/dirC/spec.json

## Localization
(en-US only for now)
