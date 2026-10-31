export const meta = {
  name: 'asofex-research',
  description: 'Compact research sweep for App Store screenshot strategy: a dozen or so Sonnet agents, each reading a bundle of 3 to 8 related sources, structured JSON back',
  whenToUse: 'Called by the asofex-ios-screenshots skill in Phase 2. args: {app, storeUrl, landingUrl, category, competitors:[names or URLs], audienceHints, knownProof, extraSources:[urls], alreadyCovered, maxRounds, maxAgents}. Do not call with no args.',
  phases: [
    { title: 'Sweep', detail: 'one agent per bundle of related sources, returns structured findings', model: 'sonnet' },
    { title: 'Gaps', detail: 'one agent per round asks what is still missing and proposes a few new bundles', model: 'sonnet' },
  ],
}

let a = args
if (typeof a === 'string') { try { a = JSON.parse(a) } catch { a = null } }
if (!a || typeof a !== 'object' || !a.app) {
  return { started: false, reason: 'no-args', next: 'asofex-research needs args {app, storeUrl, ...}. The asofex-ios-screenshots skill supplies them in Phase 2.' }
}
const app = a.app
const category = a.category || 'its category'
const competitors = Array.isArray(a.competitors) ? a.competitors : []
const maxRounds = a.maxRounds || 3
const maxAgents = a.maxAgents || 16
let agentsUsed = 0
const MODEL = 'sonnet'

const FINDINGS = {
  type: 'object',
  properties: {
    reached: { type: 'boolean' },
    sources_read: { type: 'array', items: { type: 'string' } },
    source_type: { type: 'string' },
    summary: { type: 'string' },
    audience_quotes: { type: 'array', items: { type: 'object', properties: { quote: { type: 'string' }, context: { type: 'string' }, url: { type: 'string' } }, required: ['quote', 'url'] } },
    pains: { type: 'array', items: { type: 'string' } },
    desired_outcomes: { type: 'array', items: { type: 'string' } },
    search_phrases: { type: 'array', items: { type: 'string' } },
    proof: { type: 'array', items: { type: 'object', properties: { claim: { type: 'string' }, url: { type: 'string' } }, required: ['claim', 'url'] } },
    competitor: { type: 'object', properties: { name: { type: 'string' }, screenshot1_headline: { type: 'string' }, all_headlines: { type: 'array', items: { type: 'string' } }, proof_used: { type: 'string' }, visual_style: { type: 'string' }, weakness: { type: 'string' }, rating: { type: 'string' }, price: { type: 'string' } } },
    conventions: { type: 'array', items: { type: 'string' } },
    new_leads: { type: 'array', items: { type: 'object', properties: { type: { type: 'string' }, target: { type: 'string' }, why: { type: 'string' } }, required: ['type', 'target'] } },
  },
  required: ['reached', 'sources_read', 'source_type', 'summary'],
}

const GAPS = {
  type: 'object',
  properties: {
    missing: { type: 'array', items: { type: 'string' } },
    tasks: { type: 'array', items: { type: 'object', properties: { type: { type: 'string' }, targets: { type: 'array', items: { type: 'string' } }, why: { type: 'string' } }, required: ['type', 'targets'] } },
  },
  required: ['missing', 'tasks'],
}

const TOOLING = `Tools: use WebFetch and WebSearch first. If a page blocks fetching or needs scrolling (App Store review pages, Reddit, sites with consent walls), load the Chrome tools with ToolSearch ("select:mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__tabs_close_mcp"), create your OWN new tab, do your work there, and close that tab before finishing. Never touch tabs you did not create. Read every target in your bundle, and up to 3 closely related pages you find along the way (a linked thread, a review page), but do not wander beyond that. List every URL you actually read in sources_read. If none of the targets are reachable, return reached=false with a one-line summary; if some are, return reached=true and note the failures in summary. Quote people verbatim with the URL. Never invent numbers, ratings, awards, or press. Return only the structured object.`

function finderPrompt(t) {
  const base = `You are researching the mobile app "${app}" (${category}) to inform App Store screenshot strategy. Task type: ${t.type}. Your bundle of targets (read all of them):\n${t.targets.map((x, i) => `${i + 1}. ${x}`).join('\n')}\n${t.why ? 'Why: ' + t.why : ''}\n`
  const byType = {
    'store-page': 'Read the App Store listing. Return: subtitle, first lines of the description, rating and count, price/IAP, what the current screenshots say (headline per screenshot if visible), what is weak. Put ratings and counts into proof with the URL.',
    'store-reviews': 'Read as many user reviews as you can reach for this app (App Store page, apps.apple.com reviews, or a review aggregator). Extract 8 to 15 verbatim quotes: praise, complaints, and the moment they decided to install. Fill pains and desired_outcomes in the users own words.',
    'competitor-listing': 'Read this competitor App Store listing. Fill the competitor object: screenshot 1 headline, every headline you can read, proof used, visual style, rating, price, and the weakness we can exploit. Also list category conventions you notice.',
    'competitor-reviews': 'Read reviews of this competitor. Extract verbatim quotes about what users love and hate, especially reasons they switched away or would switch. Fill pains and desired_outcomes.',
    'reddit': 'Search Reddit for this query (use WebSearch with site:reddit.com, then open threads). Extract 8 to 15 verbatim quotes about the problem, what people tried, and what they want. Fill pains, desired_outcomes, search_phrases.',
    'forum': 'Search forums, Q&A sites, and communities (Quora, Hacker News, Product Hunt, niche forums) for this query. Extract verbatim quotes and the words people use to describe the problem.',
    'blog-press': 'Find and read articles, reviews, roundups, or press for this target. Extract quotable proof (with URL), comparisons, and the language reviewers use. Note any awards or press mentions as proof with URL.',
    'landing-page': 'Read the app landing page or website. Extract the positioning, headline, claimed benefits, proof (testimonials, logos, numbers with URL), pricing, and tone.',
    'keywords': 'Research search phrases people type when looking for apps like this. Use WebSearch autocomplete-style queries ("best app for", "app to", "how to") and store listings. Return 15 to 30 search_phrases and the top 5 competitors that rank for them as new_leads.',
    'top-charts': 'Look at the App Store category top charts and "you might also like" for this category. Return the top 10 apps as new_leads of type competitor-listing with URLs, and the headline conventions you see.',
    'source-code': 'Read this local source path with Read/Grep. Extract the real feature list, screen names, onboarding steps, paywall copy, and any strings that reveal positioning. No fabrication: only what the code shows.',
    'generic': 'Read this source and extract anything relevant: quotes, pains, outcomes, proof with URL, competitor facts, conventions.',
  }
  return base + (byType[t.type] || byType.generic) + '\n' + TOOLING + `\nFill new_leads with at most 3 further sources you noticed that are clearly worth a separate read (type one of: store-page, store-reviews, competitor-listing, competitor-reviews, reddit, forum, blog-press, landing-page, keywords, top-charts, generic). Leave it empty if nothing stands out.`
}

const norm = x => (x || '').toLowerCase().replace(/[?#].*$/, '').replace(/\/+$/, '')
const seen = new Set()
const queue = []
function enqueue(type, targets, why) {
  const fresh = (targets || []).filter(x => x && !seen.has(type + '|' + norm(x)))
  if (!fresh.length) return false
  fresh.forEach(x => seen.add(type + '|' + norm(x)))
  queue.push({ type, targets: fresh, why })
  return true
}
const chunk = (arr, n) => { const out = []; for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n)); return out }

const appTargets = [a.storeUrl, a.landingUrl, ...(a.extraSources || [])].filter(Boolean)
if (a.storeUrl) enqueue('store-reviews', [a.storeUrl], 'the app itself: listing plus as many reviews as reachable')
if (appTargets.length) enqueue('landing-page', appTargets, 'everything the app says about itself')
if (a.sourcePath) enqueue('source-code', [a.sourcePath])
for (const group of chunk(competitors, 3)) enqueue('competitor-listing', group, 'listing plus reviews for each competitor in the bundle')
enqueue('keywords', [`${app} ${category}`, `App Store ${category} category top charts and similar apps`], 'search phrases and the apps that rank for them')
const hints = a.audienceHints ? ` ${a.audienceHints}` : ''
enqueue('reddit', [`${category} app frustrated`, `${category} app worth it`, `best ${category} app`, `switched from ${category} app`, `${category} app recommendation${hints}`], 'audience language on Reddit')
enqueue('forum', [`${category} app problems${hints}`, `looking for ${category} app${hints}`, `${app} Hacker News OR Product Hunt`], 'audience language on forums and Q&A sites')
enqueue('blog-press', [`${app} review`, `best ${category} apps 2026`, `${app} vs`], 'articles, roundups, press')

const fkey = s => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim().slice(0, 80)
const seenFacts = new Set()
const results = []
const unreachable = []
const leads = []
let dry = 0, round = 0

while (queue.length && dry < 2 && round < maxRounds && agentsUsed < maxAgents) {
  round++
  const batch = queue.splice(0, Math.max(0, Math.min(queue.length, maxAgents - agentsUsed - 1)))
  agentsUsed += batch.length + 1
  log(`Round ${round}: ${batch.length} bundles (${batch.reduce((n, t) => n + t.targets.length, 0)} sources), ${results.length} findings so far`)
  const out = await pipeline(batch, t =>
    agent(finderPrompt(t), { label: `${t.type} x${t.targets.length}: ${t.targets[0].slice(0, 40)}`, phase: 'Sweep', schema: FINDINGS, model: MODEL, effort: 'medium' })
      .then(r => r ? { ...r, task: t } : null))
  let fresh = 0
  for (const r of out.filter(Boolean)) {
    if (!r.reached) { unreachable.push({ task: r.task, note: r.summary }); continue }
    let novel = false
    for (const q of (r.audience_quotes || [])) { const k = 'q:' + fkey(q.quote); if (!seenFacts.has(k)) { seenFacts.add(k); novel = true } }
    for (const p of (r.proof || [])) { const k = 'p:' + fkey(p.claim); if (!seenFacts.has(k)) { seenFacts.add(k); novel = true } }
    for (const p of [...(r.pains || []), ...(r.desired_outcomes || []), ...(r.search_phrases || [])]) { const k = 'x:' + fkey(p); if (!seenFacts.has(k)) { seenFacts.add(k); novel = true } }
    if (r.competitor && r.competitor.name) { const k = 'c:' + fkey(r.competitor.name); if (!seenFacts.has(k)) { seenFacts.add(k); novel = true } }
    if (novel) fresh++
    results.push(r)
    leads.push(...(r.new_leads || []))
  }
  const byType = {}
  for (const l of leads.splice(0)) { if (l && l.type && l.target) (byType[l.type] = byType[l.type] || []).push(l.target) }
  for (const [type, targets] of Object.entries(byType)) enqueue(type, targets.slice(0, 6), 'leads surfaced by finders')
  const covered = [...seen].join('\n')
  const digest = results.slice(-40).map(r => `- [${r.source_type}] ${(r.sources_read || []).join(', ')}: ${r.summary}`).join('\n')
  const prior = a.alreadyCovered ? `\nCoverage from a previous run (do not repeat): ${a.alreadyCovered}\n` : ''
  const gaps = await agent(`You audit research coverage for App Store screenshot strategy for "${app}" (${category}).\nSources already covered (type|target):\n${covered}${prior}\nRecent findings digest:\n${digest}\n\nWhat is still missing to write a strong research brief: audience segments not heard from, competitor angles unread, proof unverified at its source, search language unknown, objections unexplored, platforms (Reddit, forums, YouTube comments, Product Hunt, app review blogs, Twitter/X, TikTok captions) not yet searched. Propose at most 4 NEW bundles that are not in the covered list; each bundle is one type with 3 to 6 related targets (URLs or queries) that one agent can read in a single pass. Fewer is better; return empty tasks unless something important is missing. Types: store-page, store-reviews, competitor-listing, competitor-reviews, reddit, forum, blog-press, landing-page, keywords, top-charts, generic. Return missing and tasks. If coverage is genuinely complete, return empty tasks.`, { label: `gaps round ${round}`, phase: 'Gaps', schema: GAPS, model: MODEL, effort: 'high' })
  let added = 0
  for (const t of ((gaps && gaps.tasks) || [])) if (enqueue(t.type, t.targets, t.why)) added++
  log(`Round ${round}: ${fresh} sources with new facts, ${added} new tasks from gaps${gaps && gaps.missing && gaps.missing.length ? ' (' + gaps.missing.slice(0, 3).join('; ') + ')' : ''}`)
  if (fresh === 0 && added === 0) dry++; else dry = 0
}
if (queue.length) log(`Stopped (rounds ${round}/${maxRounds}, agents ${agentsUsed}/${maxAgents}) with ${queue.length} bundles unread: ${queue.map(t => t.type + ' x' + t.targets.length).join(', ')}`)
if (unreachable.length) log(`${unreachable.length} sources unreachable`)

return {
  app, rounds: round, agents: agentsUsed, bundles_read: results.length, unreachable, unread: queue,
  findings: results.map(r => ({ source_type: r.source_type, sources_read: r.sources_read || [], summary: r.summary, audience_quotes: r.audience_quotes || [], pains: r.pains || [], desired_outcomes: r.desired_outcomes || [], search_phrases: r.search_phrases || [], proof: r.proof || [], competitor: r.competitor || null, conventions: r.conventions || [] })),
}
