# Alarmifex research  (updated 2026-10-30)

## Inputs received
- iOS source: `~/Documents/projects/alarmifex/alarmifex-ios` (SwiftUI, AlarmKit, iOS 26.2+, iPhone + iPad, scheme `alarmifex`, bundle `com.amdose.alarmifex`).
- Brand: `~/Documents/projects/alarmifex/alarmifex-claude/alarmifex-branding/` (icon masters, `brand/palette.json`, Manrope).
- ASO audit 2026-10-30: `output/alarmifex/audit/2026-10-30-aso-audit.md` (keywords, competitors, ratings, reviews).
- Research workflow run `wf_d59bc0df-ff2` (14 Sonnet agents, 10 bundles): `research/findings.json`.
- Store: https://apps.apple.com/us/app/id6760241021 · Site: https://alarmifex.com

## Audience
- Who: young iPhone users (teens to 30s) who are bored of, or tune out, the default iPhone tones and want to wake to something they chose: a song, the audio of a reel/TikTok/video they saved, an anime opening, a meme, a motivational speech, a voice memo. Secondary: heavy sleepers and people whose alarm "didn't go off" (silent switch, Focus, no Wi-Fi).
- Search intent and phrases: custom alarm sounds, alarm sound maker, wake up to any song, video alarm, loud alarm clock, alarm that makes you get up, wake up call (audit: `custom alarm sounds`, `alarm sound maker` #7, `loud alarm clock` p51).
- Pains (their words):
  1. "the default irritating ringtones to wake me up" (MacRumors forum)
  2. "I used to hit snooze five times and start every day stressed and rushing." (Product Hunt review)
  3. "DO NOT RELY ON THIS TO WAKE YOU UP." / "Doesn't work half the time" (Video Alarm and Alarmy reviews: alarms that silently fail)
  4. "why must I have a silent song 'playing' the entire night??" / "I don't want to waist my battery just to have an alarm." (Music Alarm Clock for Spotify reviews)
  5. "the songs i need cant add in my clock app" (Alarmifex 1★ review, ZAF): Apple Clock cannot use arbitrary audio.
- Desired outcomes: "I can pick a music video the night before and wake up to it." · "The ability to choose whatever song I want to wake up to is amazing." (Video Alarm reviews) · "a much more personalized wake-up experience" (Product Hunt).

## App as it is today
- Store page: name "Alarmifex: Custom Alarm Sounds", subtitle "Loud Music & Song Wake Up Call". Description line 1: "Alarmifex turns any sound into your alarm. A song, a viral reel or video clip, an anime opening, your own voice, or a motivational speech". Free with IAP, 3-day trial, $0.99 weekly to $39.99 yearly. 4.3★ from 3 US ratings, 8 worldwide.
- Current screenshots (7 iPhone, 4 iPad): lead with a sleep-music / Hz frame and small serif headlines; the core job (any sound becomes the alarm) is not on screenshot 1 (audit fix #4).
- Review themes: the only written reviews are 1★ about the paywall (JP, ZAF). Product Hunt (5.0, 6 reviews): praise for personalization and motivational speeches; asks for a gradual volume ramp.
- What the code actually supports (claims must stay inside this):
  - Import any audio file (MP3/M4A) or the audio track of a video, trimmed up to 1:00, with title and cover (AudioTrimmerView).
  - Share a reel/video link to Alarmifex (share extension) and it pulls the sound (ReelImportView).
  - Built-in library: 34 sounds in mood categories (Calm, Energetic, Motivational...).
  - AlarmKit system alarms: ring on silent, through Focus, offline, without the app open; Lock Screen and Dynamic Island controls.
  - Wake-up Series: several alarms with different sounds in a row.
  - Light and dark themes; per-alarm volume.
  - NOT supported: recording your voice in-app (no microphone code). "Your own voice" is only true as an imported voice memo file. Do not show or claim in-app recording.
  - Custom (uploaded) sounds and premium sounds need a subscription. Price is not shown in screenshots (user decision).

## Competitors
| App | Screenshot 1 headline | Proof used | Visual style | Weakness we exploit |
|---|---|---|---|---|
| Alarmy (4.8, 250K) | "You'll wake up. Always." / Built for Heavy Sleepers | 100M+ Downloads laurel | Bright blue/yellow gradient, huge white sans, tilted multi-phones, cartoon mascot | Sells punishment (missions); "doesn't work half the time" reviews; no custom-song story |
| myAlarm Clock (4.6, 14.9K) | "Wake up listening to the latest headline news" | none | Dated orange-crimson gradient, small type | Confusing copy (lyrics, news); dated |
| Alarmify / Music Alarm for Spotify (4.2, 5.7K) | "World's best music alarm" | #1 Music Alarm laurel, Spotify/Apple Music logos | Music-service led | Needs Spotify/Apple Music, plays a silent song all night, battery drain |
| Loud Alarm Clock – the LOUDEST (4.8, 39K) | "MADE FOR HEAVY SLEEPERS" | none in screenshots | All-caps feature lists | Loudness only, no personalization |
| Video Alarm (4.3, 3.8K) | "Wake up Using any online video" | none | Dated, plain | Ads on every alarm, $8/week, crashes, "DO NOT RELY ON THIS" |
| Mornova (new, 3 ratings) | "Wake up to any song." (Pick it on Apple Music. Keep your favorite 28 seconds.) | none | Warm peach / dark purple gradients, bold sans with orange highlight word, floating glass UI cards | Same promise but Apple Music-centric; no reel/share-sheet hook; leans on anti-snooze tasks |

## Category conventions
- Respect: headline in the top third, 2 to 6 words, bold sans on a saturated brand gradient; device tilted or cropped; one idea per screen; "Wake up ..." imperative phrasing on screenshot 1.
- Break: everyone sells loudness, missions or music services. We sell the sound itself: show the user's own sounds (song clip, reel audio, meme, speech) as the product, and show reliability (rings on silent, offline, no app open) as proof instead of download badges we do not have.
- Watch: Mornova says "Wake up to any song." almost word for word. Our headline must not echo it; lean on "any sound / your sound / reel" instead.

## Proof inventory (only verified)
- No ratings, counts, awards or press usable (8 ratings worldwide, both written reviews 1★).
- Product Hunt 5.0 from 6 reviews (https://www.producthunt.com/products/alarmifex/reviews): too thin to badge; do not use.
- Product proof we can state truthfully: rings on silent and Focus, works offline, no need to keep the app open (AlarmKit); trim to the exact second, up to 1:00; 34 built-in sounds; share a reel link straight to the app.

## Open questions
- Reddit unreachable (WebFetch, WebSearch and Chrome all blocked); no Reddit quotes. TikTok/YouTube comments unread.
- Competitor galleries past screenshot 3 unread.
- Screenshot captures: custom sounds show subscription locks and a "Subscribe to keep your premium sounds ringing" banner when not subscribed; need a subscribed state on the simulator (see positioning decisions log).
