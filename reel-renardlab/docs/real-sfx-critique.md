# Critique, round 1

| axis | score | basis |
|---|---|---|
| hook | 10.0 | first sound at 0.15s |
| sync | 9.7 | 27/28 sounds on their frame (peaks, arrivals, or first onsets for clicks) |
| coverage | n/a | 31 cues for 31 declared events (the list is the reference; runs and clusters are thinned on purpose) |
| pacing | 10.0 | 6.0 weighted events per 10 s, longest silence 4.7 s |
| variety | 9.6 | 29 source recordings, 22 families in 29 sounds (runs and interface sounds not counted) |
| hierarchy | 10.0 | 11.9 dB between the loud and the quiet sounds |
| headroom | 10.0 | true peak -1.6 dBTP |
| loudness | 10.0 | final -14.7 LUFS (the author's own balance is kept) |
| balance | 10.0 | median event peak -3 dB vs the original around it, big sounds -2 dB (whole-track gap +13 LU) (8 event(s) on speech left to the speech axis) |
| audibility | 10.0 | 0 of 31 sounds sit more than 30 dB under the film's own sound in the mix (median -9 dB, after the ducking) |
| speech | 8.5 | 1 sound(s) in 1 moment(s) are within 3 dB of the voice or above it (0 above) even after ducking |
| low_end | 10.0 | 0 heavy sound(s) on top of existing bass |
| mono | 10.0 | the SFX track loses 0.2 dB when folded to mono (0 = the channels agree, 3 = unrelated, 6+ = parts cancel); 0 of 31 sounds lose more than 6 dB; the film loses 0.0 LU in mono against 0.0 LU for the original (+0.0 added) |

**PASS**: lowest axis 8.5 (every axis must reach 8; a new film needs at least 3 rounds)

Nothing blocks showing it. If there is time, the cheapest polish:
1. hierarchy: 'magic' at 47.48s is 10 dB quieter (perceived level) than the other chime sounds: a thin recording, pick a fuller one (search.py --role chime --sheet) or raise it
2. hierarchy: 'pop x0.90' at 11.97s is 9 dB quieter (perceived level) than the other pop sounds: a thin recording, pick a fuller one (search.py --role pop --sheet) or raise it

Listen to these 5 moments, on headphones and then once on a phone speaker. This script cannot hear: they are the places where the numbers above are least certain, and none of them says that it sounds good:
  1.    0.15s  'pop x0.70': the first sound of the film: the hook; its attack was moved 112 ms so that it lands on the moment. Listen for: does it land with the picture at once, and is it clearly there under the music or the voice? / does the lead-in still read as part of the sound?
  2.    4.69s  'whoosh x0.70': brought 6 dB up to the perceived level of its role. Listen for: a thin recording lifted that far can turn harsh: is it clean?
  3.   31.21s  'pop x0.80': its peak sits -12 ms from the moment. Listen for: does it feel early or late against the picture?
  4.   37.34s  'thump x0.60': the highest peak of the film (-2 dBFS before the master). Listen for: is it big without hurting on headphones, and does the music under it pump?
  5.   47.48s  'magic': 1 sound(s) on top of the voice, -2.0 dB against it; the quietest by perceived loudness among the sounds that are not ticks. Listen for: is every word still understood? / can it be heard at all?
  (--listen-out FILE.wav cuts them into one file of the film's own sound)

Still to judge by eye on review.png: character fit (each sound suits its picture), cleanliness (no mud in the low end under music/voice, nothing masks speech), taste (designed, not sprayed on).
