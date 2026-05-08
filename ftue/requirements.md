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
