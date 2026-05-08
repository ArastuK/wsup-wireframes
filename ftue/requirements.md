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

## Card data — what's source-of-truth vs derived

Every field on the swipe card maps to either an existing Firestore `CharCharacters` field or a derived display field computed at deck-build time.

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

### Derived (computed by `deriveArchetype(char)` at deck-build time)

The **archetype label** ("Mentor", "Royalty", "Tsundere"…) and its **emoji + color** are NOT in Firestore. They're computed from `tags[]` + `categories[]` + `name` + `description` using a priority-ordered rule list. First rule that matches wins.

```ts
type Archetype = { label: string; emoji: string; color: string };

const ARCHETYPE_RULES: Array<{ test: (c: Character) => boolean; archetype: Archetype }> = [
  { test: c => has(c.tags, ['royalty','royalverse']) || /prince|princess/i.test(c.name),    archetype: { label: 'Royalty',     emoji: '👑',  color: '#facc15' }},
  { test: c => has(c.tags, ['vampire']) || c.categories.includes('vampire'),                archetype: { label: 'Vampire',     emoji: '🩸',  color: '#ef4444' }},
  { test: c => c.categories.includes('fantasy') || has(c.tags, ['fantasy','magic','elf','demon','fairy','supernatural','wizard','dragon','mage']), archetype: { label: 'Fantasy', emoji: '🔮', color: '#a855f7' }},
  { test: c => has(c.tags, ['android','robot','sci-fi','scifi','space']),                   archetype: { label: 'Sci-fi',      emoji: '🚀',  color: '#3b82f6' }},
  { test: c => /therap|psycholog|dietitian|counsel/i.test(c.description + c.background),    archetype: { label: 'Therapist',   emoji: '🌿',  color: '#10b981' }},
  { test: c => c.categories.includes('teacher') || has(c.tags, ['mentor','professor','teacher']), archetype: { label: 'Mentor', emoji: '📚', color: '#f59e0b' }},
  { test: c => c.categories.includes('mafia') || has(c.tags, ['boss']),                     archetype: { label: 'Mafia',       emoji: '🕴️', color: '#1f2937' }},
  { test: c => c.categories.includes('bully') || has(c.tags, ['bully']),                    archetype: { label: 'Bully',       emoji: '😼',  color: '#ec4899' }},
  { test: c => has(c.tags, ['tsundere','enemies to lovers']),                                archetype: { label: 'Tsundere',    emoji: '💢',  color: '#f472b6' }},
  { test: c => c.categories.includes('celebrities') || has(c.tags, ['musician']) || /rockband/i.test(c.description), archetype: { label: 'Rockstar', emoji: '🎸', color: '#8b5cf6' }},
  { test: c => has(c.tags, ['roommate']),                                                    archetype: { label: 'Roommate',    emoji: '🏠',  color: '#06b6d4' }},
  { test: c => has(c.tags, ['athlete','sports']),                                            archetype: { label: 'Athlete',     emoji: '🏆',  color: '#06b6d4' }},
  { test: c => has(c.tags, ['supernatural']),                                                archetype: { label: 'Supernatural',emoji: '✨',  color: '#a855f7' }},
  { test: c => c.categories.includes('boyfriend')  || has(c.tags, ['boyfriend']),            archetype: { label: 'Boyfriend',   emoji: '💕',  color: '#f472b6' }},
  { test: c => c.categories.includes('girlfriend') || has(c.tags, ['girlfriend']),           archetype: { label: 'Girlfriend',  emoji: '💕',  color: '#f472b6' }},
  { test: c => has(c.tags, ['best friend']) || c.categories.includes('friend'),              archetype: { label: 'Best friend', emoji: '☕',  color: '#fb923c' }},
  { test: c => c.categories.includes('romantic'),                                            archetype: { label: 'Romance',     emoji: '💕',  color: '#f472b6' }},
];
// Fallback
const FALLBACK: Archetype = { label: 'Character', emoji: '💬', color: '#6b7280' };
```

**Why derived not stored:** keeps creators free to tag however they want and lets us tune the FTUE label set without a Firestore migration. Run derivation at deck-build time on FE; archetype is included in `feFtueSwipeCardSwiped.extraData` so analytics can split metrics by archetype without re-deriving.

**Working reference:** the Python derivation that built the prototype is at [`build_final_pool.py`](https://github.com/ArastuK/wsup-wireframes/blob/main/ftue/build_final_pool.py) — port these rules to TS verbatim.

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
