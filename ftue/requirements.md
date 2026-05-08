# FTUE Swipe Onboarding — Dev Requirements (Exp 2)

**Owner:** Arastu · **Trello:** [pt4qekTN](https://trello.com/c/pt4qekTN) · **Prototype:** [swipe-prototype.html](swipe-prototype.html)

## Summary

Replace the current first-visit demographic modal with a swipe-deck FTUE that asks **age + preference**, then presents **10 curated characters** as Tinder-style cards. First right-swipe enters chat with that character. Web-only for v1.

## A/B Test

- **50/50 split on new web users**, assigned at first `feUptime` of session-0
- **Persistence:** `localStorage.ftueVariant = 'control' | 'treatment'`
- **Control:** existing demographic modal (no change)
- **Treatment:** new swipe FTUE (this spec)
- All new events tagged with `ftueVariant` in `extraData`

## Pool & filtering

- **Pool v1:** 48 hand-curated characters, hardcoded in FE bundle (`ftuePool.ts`). Future: BQ-driven Firestore collection `CharFtueCuratedPool`, refreshed weekly.
- **Distribution of pool:** 30 female / 18 male · 24 anime / 24 photo · 17 archetypes (Romance, Mentor, Therapist, Royalty, Fantasy, Vampire, Mafia, Bully, Tsundere, Rockstar, Roommate, Athlete, Boyfriend, Girlfriend, Best friend, Sci-fi, Comedy)
- **Preference filter:**
  - `female` → 30 candidates
  - `male` → 18 candidates
  - `any` → all 48 candidates
- **Age:** captured for analytics + post-FTUE personalization. Under-18 block enforced upstream (existing).

## Card data — sources

Every field on the swipe card maps to either an existing Firestore `CharCharacters` field or a hardcoded value in the pool entry.

### Source-of-truth (Firestore `CharCharacters/{charId}`)

| Card field | Firestore field | Notes |
|---|---|---|
| Image | `characterImageUrl` | Always present in our pool (filtered) |
| Name | `name` | |
| Age | `age` | String. Some chars use lore ages (e.g. "500"); FE should render verbatim |
| Gender | `gender` | `"female"`, `"male"`, `"other"` — drives preference filter |
| Image style | `imageStyle` | `"anime"` or `"photo"` — drives the style badge |
| Greeting (bubble) | `greetingMsg` | Strip `*action*` chunks for the preview; show full greeting on chat-screen entry |
| Hook (italic line) | first sentence of `description` | Truncate to ≤140 chars |
| Tag pills | `tags[]` | Take first 3 |

### v1 hardcoded pool (48 chars)

For the experiment, archetype label/emoji/color are **baked into each pool entry** — no runtime derivation. Pool ships in `ftuePool.ts`. Full JSON: [`pool.json`](https://github.com/ArastuK/wsup-wireframes/blob/main/ftue/pool.json).

| ID | Name | Gender | Style | Archetype | Emoji | Color |
|---|---|---|---|---|---|---|
| `char-RAPrkxKyfKAchBxx4YaTZ` | Camila | female | photo | Girlfriend | 💕 | #f472b6 |
| `char-iOo1xzDkorVtBWklhGYz7` | Damien | male | anime | Boyfriend | 💕 | #f472b6 |
| `char-WVHg8J6mHhOxGkKAGU10p` | Adris | male | anime | Royalty | 👑 | #facc15 |
| `char-O6Ax6TtMr9GCwOLgfP1XR` | Maria | female | anime | Mentor | 📚 | #f59e0b |
| `char-Z3TDjFPJ0WR4FAVwg34w3` | Donovan Blackthorne | male | anime | Mafia | 🕴️ | #1f2937 |
| `char-fvuszhGivM9mrTGn1TFT0` | Maddox | male | anime | Bully | 😼 | #ec4899 |
| `char-AHn4WsYrcqVMD5PL5eeaN` | Kaiden | male | anime | Bully | 😼 | #ec4899 |
| `char-03mGydbs59nUPsp2jPC7G` | Leo | male | anime | Roommate | 🏠 | #06b6d4 |
| `char-Ix2xvgsk8sjIexKZq6FyO` | Fye | female | anime | Roommate | 🏠 | #06b6d4 |
| `char-rcRwg52kTkJq6ppFUbSuz` | Yuan | male | anime | Bully | 😼 | #ec4899 |
| `char-ZHbl4JgEIJ3CEZknvmnAy` | evorest | female | anime | Bully | 😼 | #ec4899 |
| `char-0n5YoV6pzsgMpcIgbmZDo` | Raphaël | male | anime | Tsundere | 💢 | #f472b6 |
| `char-CVhomuW77JTeA5q4Ebyth` | Belle | female | anime | Roommate | 🏠 | #06b6d4 |
| `char-UWPXuwjyoP04Lb9Trpe3N` | Kai | male | anime | Boyfriend | 💕 | #f472b6 |
| `char-52ksxLtXjPCsZI3aZfClB` | Ryder | male | anime | Vampire | 🩸 | #ef4444 |
| `char-Lu4bUyE6TjMC853ma2wvA` | Kristen | female | photo | Athlete | 🏆 | #06b6d4 |
| `char-VoQgBYAJJWhy3OcNJLY04` | Renko | male | photo | Vampire | 🩸 | #ef4444 |
| `char-ysH8PlTm4kpOBv1hCSHWx` | Elise | female | anime | Girlfriend | 💕 | #f472b6 |
| `char-adDgFVx158h3fuyLyermj` | Xander Thorne | male | photo | Rockstar | 🎸 | #8b5cf6 |
| `char-qemBvSFFPn5erDniwFGd7` | Addie Bryant | female | photo | Athlete | 🏆 | #06b6d4 |
| `char-FCuR9W4LOmJI0SQFbbSd8` | Hazel | female | anime | Bully | 😼 | #ec4899 |
| `char-gYOa9dGLovy8y254Cw4Cd` | luna | female | anime | Girlfriend | 💕 | #f472b6 |
| `char-6KRuKIe0wyCzsPD0sFMZO` | Olivia | female | anime | Tsundere | 💢 | #f472b6 |
| `char-QqptNUndwwIxkIhvXS7UE` | yun-ho | female | anime | Girlfriend | 💕 | #f472b6 |
| `char-caPKg0Z9BUffal3D4JLDR` | Katie | female | photo | Therapist | 🌿 | #10b981 |
| `char-IGKIOAEiuEqBCi8TeRiTp` | Lydia | female | photo | Mentor | 📚 | #f59e0b |
| `char-2iFafhRgZbGhk3c3fafCo` | Professor Jae-yeon | male | anime | Mentor | 📚 | #f59e0b |
| `char-5aC1gvMBSlewSickCBI9V` | Jill | female | photo | Therapist | 🌿 | #10b981 |
| `char-fI3VKcGfUjlzVIco1ErMf` | Kathy | female | photo | Mentor | 📚 | #f59e0b |
| `char-GufNAwsFwVN49AF5ppfnQ` | Alice | female | photo | Therapist | 🌿 | #10b981 |
| `char-WuldH2BpbnHtWMgC6GXy7` | Mio Veramude | male | anime | Fantasy | 🔮 | #a855f7 |
| `char-C96hxLSAsVxP9EMGCqMPK` | Prince Ash | male | anime | Royalty | 👑 | #facc15 |
| `char-dEUzj7upaoO3aDNNxGW7G` | Princess Xiao | female | anime | Royalty | 👑 | #facc15 |
| `char-GnHlBOeFPt50zNAVmTyMg` | Hailey | female | anime | Fantasy | 🔮 | #a855f7 |
| `char-p2BZ4rTBEXfzRdOW0Wij4` | 01 | female | photo | Sci-fi | 🚀 | #3b82f6 |
| `char-os48HomGfgrzy5tbMKYyC` | Fata | female | photo | Vampire | 🩸 | #ef4444 |
| `char-GuGIGhBAcIWxRa6T6DFFY` | Lola | female | photo | Best friend | ☕ | #fb923c |
| `char-S6X6tIx6D59YoZ57qi7Jj` | Caleb | male | photo | Athlete | 🏆 | #06b6d4 |
| `char-vVproCMQMPrfBqmO5gq9c` | Amy | female | photo | Rockstar | 🎸 | #8b5cf6 |
| `char-uDHgAI1X8vgmeTs8JU5BX` | Malina | female | photo | Mentor | 📚 | #f59e0b |
| `char-3F8cu5WW3ZJt9JjQH4RI2` | Camryn | female | photo | Athlete | 🏆 | #06b6d4 |
| `char-wAWgkWJvOFMLzy5sbayYy` | Alt Friend (Odin) | male | photo | Best friend | ☕ | #fb923c |
| `char-VwM3F17Adk5v3Kl3RalI9` | Karry | female | photo | Bully | 😼 | #ec4899 |
| `char-qMiy7QhMhgXZ0pUShG3f6` | Lily | female | photo | Therapist | 🌿 | #10b981 |
| `char-bIoVbxPMYCmx8TflRfVYQ` | Demitra | female | photo | Best friend | ☕ | #fb923c |
| `char-MvxkPR3SZ3aoxITaFU9eW` | Olivia Jang | female | photo | Girlfriend | 💕 | #f472b6 |
| `char-Wg9hDEASKC4yWzfpGY3Kf` | AJ | male | photo | Boyfriend | 💕 | #f472b6 |
| `char-GmjoS4peyfWwISU9CVs4M` | Karen | female | photo | Comedy | 😄 | #fb923c |

**Pool composition:** 30 female · 18 male · 24 anime · 24 photo · 14 archetypes (Bully ×6, Girlfriend ×7, Mentor ×5, Athlete ×4, Therapist ×4, Boyfriend ×4, Roommate ×4, Royalty ×3, Vampire ×3, Best friend ×3, Tsundere ×2, Rockstar ×2, Fantasy ×2, Sci-fi ×1, Mafia ×1, Comedy ×1).

## Deck composition (10 cards)

Stratified random — **never show 10 of the same archetype**:

1. Filter pool by `pref`
2. Group remaining chars by `archetype`
3. **Round-robin: max 2 per archetype**, in randomized archetype order
4. Top up from full pool if filtered set < 10 (small-pool safety)
5. Shuffle inside each bucket so order varies per session
6. **First card** is always from the highest-engagement archetype available (set the hook)

## UX

- **Screen 1 (Welcome):** age chips (18-20 / 21-25 / 26-34 / 35-44 / 45+), preference chips (Female / Male / No preference), Continue CTA, **✕ Skip** in top-right
- **Screen 2 (Swipe deck):** 10-card stack, drag swipe + ✕/♥ buttons + ← / → keyboard, progress dots, archetype badge + chat-bubble greeting preview per card, **✕ Skip** in top-right
- **Screen 3 (Chat):** opens with the chosen char's greeting message; "Continue exploring (N more)" rail at top to return to deck
- **Skip behavior:** ✕ button on either screen → navigate to `/` (Explore home), no FTUE pop-up again this session
- Mobile-first 414px container; works on desktop ← / → keyboard

## Events (existing nomenclature: `nowgg-fe*` / `nowgg-be*`, JSON `extraData`)

All events include `ftueVariant` and existing standard fields (`userId`, `chatSessionId` where applicable).

| Event | Trigger | Key extraData |
|---|---|---|
| `nowgg-feFtueSwipeShown` | Screen 1 mounted | — |
| `nowgg-feFtueSwipeStep1Submitted` | Continue clicked | `age`, `pref` |
| `nowgg-feFtueSwipeDeckBuilt` | Screen 2 mounted | `deckSize`, `deckCharIds[]`, `deckArchetypes[]`, `pref` |
| `nowgg-feFtueSwipeCardSwiped` | Each swipe (incl. autoswipe) | `characterId`, `position` (1-10), `direction` (left/right), `archetype`, `gender`, `imageStyle`, `viaInteraction` (drag/button/keyboard) |
| `nowgg-feFtueSwipeSkipped` | ✕ click | `fromScreen` (1/2), `deckPosition`, `passes`, `likes` |
| `nowgg-feFtueSwipeDeckExhausted` | All 10 passed | `passes`, `likes` |
| `nowgg-feFtueSwipeRailClick` | "Continue exploring" rail tapped in chat | `remaining`, `currentCharacterId` |
| `nowgg-feChatStarted` *(existing — enrich)* | First right-swipe → chat | **add** `source: "ftue_swipe"`, `position`, `deckPasses`, `ftueVariant` |
| `nowgg-beMessageSent` *(existing — enrich)* | Each msg in this session | inherit `source: "ftue_swipe"` from the FTUE-originated session |

## Success metrics

- **Primary:** Day-1 message rate (% new users with ≥1 `beMessageSent` within 24h of first `feUptime`), per arm
- **Secondary:** D7 retention, msgs/user Week 1, FTUE→chat conversion (% completing screen 1 → entering chat from screen 2)
- **Guardrails:** per-step drop-off, skip rate, time-to-first-msg, abuse-report rate on FTUE-attributed first chats

## Read time

- ~4,500 new web users/day → ~2,250/arm/day
- D1 baseline ~30%, MDE 5 percentage points, α=0.05, β=0.2 → **~5–7 days**

## Out of scope (v1)

- App rollout (web-only first)
- Personalization beyond gender filter (no two-tower / RAG yet)
- Live moderation pass over curated pool (chars are pre-vetted)
- Backend-driven pool refresh (FE-bundled list for v1)

## Engineering checklist

- [ ] Variant assignment on first `feUptime` (web new-user flag)
- [ ] FE: 3-screen flow + skip button + keyboard handlers
- [ ] FE: stratified deck builder (`buildDeck(pool, pref)`)
- [ ] FE: hardcoded pool ([see prototype JSON](swipe-prototype.html#L398))
- [ ] FE: typewriter rendering of greeting bubble
- [ ] FE: emit all events listed above
- [ ] BE: enrich `feChatStarted` ingestion to handle `source` and forward to BQ
- [ ] BE: ensure `source` propagates into session-level joins
- [ ] Analytics: dashboard for primary + guardrail metrics, split by arm
- [ ] QA: skip-button doesn't re-trigger FTUE for same user/session
