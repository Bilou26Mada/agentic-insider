# Agentic Insider static site (GitHub Pages). Layout modelled on the big AI media sites (The Rundown AI): dark hero
# with one promise + CTA, proof strip, then a light rounded panel with filterable "latest drops", a how-it-works row,
# a reels strip, FAQ (FAQPage schema) and a full footer. Brand = the amber glow series.
# python build.py -> index.html, tools/<slug>.html, sitemap.xml, robots.txt
import html
from _theme import THEMES, BASE_CSS, hero
import json
from datetime import date
from pathlib import Path

BASE = "https://bilou26mada.github.io/agentic-insider"
IG = "https://www.instagram.com/agentic_insider/"
FB = "https://www.facebook.com/agenticinsider"
YT = "https://www.youtube.com/@agenticinsider"
TOOLS = [
    dict(seo="Claude Code bug-fixing setup: GitHub MCP, Context7, Chrome DevTools MCP and Playwright MCP, with install commands", slug="fix-setup", name="The Claude Code bug-fixing setup", by="Agentic Insider", tag="Claude Code", date="2026-11-08", news=True,
         h1="Why this setup works", h2="The full setup (4 installs)", src="github.com", repo="https://github.com/github/github-mcp-server",
         hook="Claude Code just turned bug fixing into one AI workflow, with the right setup",
         lead="Asking an AI to \"fix my site\" makes it guess. Give Claude Code four MCP servers instead: the bug report (GitHub), today's docs (Context7), eyes on the page (Chrome DevTools) and tests (Playwright). Every install command below comes from the project's own repository.",
         facts=["GitHub MCP is GitHub's official server: issues, pull requests and code (github/github-mcp-server)",
                "Context7 gives AI coding agents up-to-date documentation for the libraries they use (upstash/context7)",
                "Chrome DevTools MCP lets a coding agent control and inspect a live Chrome browser, including console errors (ChromeDevTools/chrome-devtools-mcp)",
                "Playwright MCP lets the agent drive a real browser: navigate, click, fill forms (microsoft/playwright-mcp)",
                "Each server only gets the access you give it: use a token limited to one repo, and read every approval pop-up"],
         steps=['<strong>#1 GitHub MCP: Claude reads the bug report from your issues.</strong> <code>claude mcp add --transport http github https://api.githubcopilot.com/mcp -H &quot;Authorization: Bearer YOUR_GITHUB_PAT&quot;</code> Create a fine-grained personal access token on GitHub with access to that repo only. <a href="https://github.com/github/github-mcp-server" rel="nofollow">github.com/github/github-mcp-server</a>', '<strong>#2 Context7: up-to-date docs for the libraries in your project.</strong> <code>npx ctx7 setup --claude</code> It signs you in and installs the setup for Claude Code. <a href="https://github.com/upstash/context7" rel="nofollow">github.com/upstash/context7</a>', '<strong>#3 Chrome DevTools MCP: Claude opens your site and reads the console errors.</strong> In Claude Code: <code>/plugin marketplace add ChromeDevTools/chrome-devtools-mcp</code> then <code>/plugin install chrome-devtools-mcp@chrome-devtools-plugins</code> <a href="https://github.com/ChromeDevTools/chrome-devtools-mcp" rel="nofollow">github.com/ChromeDevTools/chrome-devtools-mcp</a>', '<strong>#4 Playwright MCP: Claude clicks through the page and tests the fix.</strong> <code>claude mcp add playwright npx @playwright/mcp@latest</code> <a href="https://github.com/microsoft/playwright-mcp" rel="nofollow">github.com/microsoft/playwright-mcp</a>', '<strong>Then ask:</strong> <code>Read issue #142, reproduce it in the browser, fix it, and prove it with a Playwright test.</code> Read every approval pop-up before you click Allow.'],
         good="Developers using Claude Code on a web project", needs="Claude Code, Node.js, a GitHub token"),
    dict(seo="30 open-source MCP servers to plug your AI into your apps (GitHub, Playwright, Notion, Supabase, Stripe...)", slug="mcp-servers", name="30 open-source MCP servers", by="GitHub", tag="Agents", date="2026-11-07", news=True,
         h1="How we picked them", h2="The 30 servers", src="github.com", repo="https://github.com/modelcontextprotocol/servers",
         hook="30 open-source MCP servers to plug your AI into your apps",
         lead="MCP lets an AI agent use your apps through small servers. Here are 30 open-source ones, from the official basics to GitHub, Playwright, Notion, Supabase, Stripe and Cloudflare. Each link goes to the publisher's own repository.",
         facts=["Every repository was checked on GitHub on November 6, 2026: it exists, has an open-source licence and is not archived",
                "All of them had code pushed in the weeks before we checked",
                "Most are published by the company behind the app (GitHub, Microsoft, Notion, Stripe, Cloudflare, AWS...); the first five come from the MCP project itself",
                "Open source means the code is free; some services still need an account or an API key",
                "A server can do whatever its tools allow, so read every approval pop-up and give it the smallest access it needs"],
         steps=['<strong>Filesystem</strong> (the basics): Read and edit files in folders you allow. <a href="https://github.com/modelcontextprotocol/servers" rel="nofollow">github.com/modelcontextprotocol/servers</a>', '<strong>Fetch</strong> (the basics): Turn any web page into clean text. <a href="https://github.com/modelcontextprotocol/servers" rel="nofollow">github.com/modelcontextprotocol/servers</a>', '<strong>Git</strong> (the basics): Read, search and commit in your repos. <a href="https://github.com/modelcontextprotocol/servers" rel="nofollow">github.com/modelcontextprotocol/servers</a>', '<strong>Memory</strong> (the basics): A knowledge graph your AI keeps between chats. <a href="https://github.com/modelcontextprotocol/servers" rel="nofollow">github.com/modelcontextprotocol/servers</a>', '<strong>Sequential Thinking</strong> (the basics): Step-by-step reasoning for hard problems. <a href="https://github.com/modelcontextprotocol/servers" rel="nofollow">github.com/modelcontextprotocol/servers</a>', '<strong>GitHub</strong> (code): Issues, pull requests and code from the chat. <a href="https://github.com/github/github-mcp-server" rel="nofollow">github.com/github/github-mcp-server</a>', '<strong>Playwright</strong> (code): Your AI drives a real browser. <a href="https://github.com/microsoft/playwright-mcp" rel="nofollow">github.com/microsoft/playwright-mcp</a>', '<strong>Chrome DevTools</strong> (code): Debug and profile live web pages. <a href="https://github.com/ChromeDevTools/chrome-devtools-mcp" rel="nofollow">github.com/ChromeDevTools/chrome-devtools-mcp</a>', '<strong>Context7</strong> (code): Up-to-date library docs, no outdated code. <a href="https://github.com/upstash/context7" rel="nofollow">github.com/upstash/context7</a>', '<strong>Docker MCP Gateway</strong> (code): Run your MCP servers safely in containers. <a href="https://github.com/docker/mcp-gateway" rel="nofollow">github.com/docker/mcp-gateway</a>', '<strong>Brave Search</strong> (search the web): Private web, news and image search. <a href="https://github.com/brave/brave-search-mcp-server" rel="nofollow">github.com/brave/brave-search-mcp-server</a>', '<strong>Exa</strong> (search the web): Web search and crawling built for AI. <a href="https://github.com/exa-labs/exa-mcp-server" rel="nofollow">github.com/exa-labs/exa-mcp-server</a>', '<strong>Firecrawl</strong> (search the web): Scrape any site into clean markdown. <a href="https://github.com/firecrawl/firecrawl-mcp-server" rel="nofollow">github.com/firecrawl/firecrawl-mcp-server</a>', '<strong>Tavily</strong> (search the web): Real-time search, extract and crawl. <a href="https://github.com/tavily-ai/tavily-mcp" rel="nofollow">github.com/tavily-ai/tavily-mcp</a>', '<strong>Apify</strong> (search the web): Ready-made scrapers for social media, maps and shops. <a href="https://github.com/apify/apify-mcp-server" rel="nofollow">github.com/apify/apify-mcp-server</a>', '<strong>Supabase</strong> (databases): Query and manage your Supabase project. <a href="https://github.com/supabase/mcp" rel="nofollow">github.com/supabase/mcp</a>', '<strong>MongoDB</strong> (databases): Talk to your MongoDB data in plain English. <a href="https://github.com/mongodb-js/mongodb-mcp-server" rel="nofollow">github.com/mongodb-js/mongodb-mcp-server</a>', '<strong>Neon</strong> (databases): Serverless Postgres: create, branch, query. <a href="https://github.com/neondatabase/mcp-server-neon" rel="nofollow">github.com/neondatabase/mcp-server-neon</a>', '<strong>Redis</strong> (databases): Read and write your Redis data. <a href="https://github.com/redis/mcp-redis" rel="nofollow">github.com/redis/mcp-redis</a>', '<strong>MCP Toolbox for Databases</strong> (databases): BigQuery, Postgres, MySQL and more, by Google. <a href="https://github.com/googleapis/mcp-toolbox" rel="nofollow">github.com/googleapis/mcp-toolbox</a>', '<strong>Notion</strong> (work apps): Search, read and write your Notion pages. <a href="https://github.com/makenotion/notion-mcp-server" rel="nofollow">github.com/makenotion/notion-mcp-server</a>', '<strong>Atlassian</strong> (work apps): Jira tickets and Confluence pages. <a href="https://github.com/atlassian/atlassian-mcp-server" rel="nofollow">github.com/atlassian/atlassian-mcp-server</a>', '<strong>Stripe</strong> (work apps): Payments, customers and invoices from the chat. <a href="https://github.com/stripe/ai" rel="nofollow">github.com/stripe/ai</a>', '<strong>MarkItDown</strong> (work apps): PDF, Word and Excel into text your AI reads. <a href="https://github.com/microsoft/markitdown" rel="nofollow">github.com/microsoft/markitdown</a>', '<strong>Netlify</strong> (work apps): Build and deploy websites from a prompt. <a href="https://github.com/netlify/netlify-mcp" rel="nofollow">github.com/netlify/netlify-mcp</a>', '<strong>Cloudflare</strong> (cloud & ops): Workers, DNS, logs and more. <a href="https://github.com/cloudflare/mcp-server-cloudflare" rel="nofollow">github.com/cloudflare/mcp-server-cloudflare</a>', '<strong>AWS</strong> (cloud & ops): Official servers for AWS services and docs. <a href="https://github.com/awslabs/mcp" rel="nofollow">github.com/awslabs/mcp</a>', '<strong>Grafana</strong> (cloud & ops): Dashboards, alerts and logs in plain English. <a href="https://github.com/grafana/mcp-grafana" rel="nofollow">github.com/grafana/mcp-grafana</a>', '<strong>Terraform</strong> (cloud & ops): Write infrastructure code with live provider docs. <a href="https://github.com/hashicorp/terraform-mcp-server" rel="nofollow">github.com/hashicorp/terraform-mcp-server</a>', '<strong>Browser MCP</strong> (cloud & ops): Automate the Chrome you are already logged into. <a href="https://github.com/BrowserMCP/mcp" rel="nofollow">github.com/BrowserMCP/mcp</a>'],
         good="Anyone using Claude, ChatGPT, Cursor or VS Code with MCP", needs="An AI app that supports MCP"),
    dict(seo="How AI agents remember: context window, compaction and memory files, explained simply", slug="ai-memory", name="How AI agents remember", by="Anthropic", tag="Agents", date="2026-11-07",
         news=True, h1="How it works", h2="Try it yourself", src="platform.claude.com", repo="https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool",
         hook="Your AI agent forgets you after every message. Here is how it fakes a memory",
         lead="A language model keeps nothing between two messages. Each turn, the app sends it the whole conversation again, and all of it has to fit in one context window. When that window fills up, old turns get summarized. Real long-term memory is something else: notes saved in files that the agent reads before it starts a task.",
         facts=["Each request contains \"all previous conversation history plus the current user message\" (Claude docs, context windows)",
                "Current Claude models have a context window of up to 1 million tokens; older ones 200,000 (Claude docs)",
                "When long conversations approach the limit, \"server-side compaction is the primary strategy\": older turns are summarized (Claude docs)",
                "The memory tool lets Claude \"store and retrieve information across conversations in a directory of memory files\" (Claude docs, memory tool)",
                "With it enabled, Claude \"automatically checks its memory directory before starting a task\" (Claude docs)",
                "Memory lives in your application: you decide where the files are stored (Claude docs)",
                "In Claude Code, CLAUDE.md files are \"loaded at launch\" in every session (Claude Code docs)"],
         steps=["<strong>Notice the reset:</strong> open a new chat and ask what it knows about you. Without a memory feature, nothing.",
                "<strong>Turn memory on or off</strong> in Claude under Settings, and look at what it saved. You can edit or wipe it.",
                "<strong>In Claude Code, write a CLAUDE.md</strong> at the root of your project: your rules, your stack, your commands. It is read at every launch.",
                "<strong>Keep it short.</strong> Anthropic suggests under 200 lines per CLAUDE.md file.",
                "<strong>Long chat going off the rails?</strong> Start a fresh one with a short summary: a clean context beats a squeezed one."],
         good="Anyone who wonders why their AI forgets, or wants it to remember the right things", needs="Claude (memory setting) or Claude Code (CLAUDE.md)"),
    dict(seo="What is MCP? How AI agents plug into your apps (Model Context Protocol), explained simply", slug="mcp", name="How AI agents plug into your apps (MCP)", by="Anthropic", tag="Agents", date="2026-11-06",
         news=True, h1="How it works", h2="Try it yourself", src="modelcontextprotocol.io", repo="https://modelcontextprotocol.io/docs/getting-started/intro",
         hook="One plug for every app: how AI agents connect to your tools with MCP",
         lead="On its own, an AI agent can only talk. MCP, the Model Context Protocol, gives it one standard way to reach your apps: each app runs a small server, the agent asks it which tools it offers, picks one, and the app asks you before anything runs. Anthropic open-sourced it in November 2024.",
         facts=["\"Think of MCP like a USB-C port for AI applications\" (modelcontextprotocol.io)",
                "MCP was created at Anthropic and open-sourced on November 25, 2024 (Anthropic)",
                "Three roles: the host is the AI app, the client is the connector inside it, the server is the service that offers tools and data (MCP spec, 2025-06-18)",
                "A server can offer tools (functions the model runs), resources (data) and prompts (templates) (MCP spec)",
                "The agent discovers tools with a tools/list request and runs one with tools/call (MCP spec)",
                "\"Hosts must obtain explicit user consent before invoking any tool\" (MCP spec)",
                "Claude, ChatGPT, Visual Studio Code and Cursor support MCP (modelcontextprotocol.io)"],
         steps=["<strong>Pick one app you use every day</strong> (files, calendar, GitHub) and look for its MCP server in your AI app's connector list.",
                "<strong>Add it in your AI app:</strong> in Claude, Settings &gt; Connectors; in Claude Code, <code>claude mcp add</code>.",
                "<strong>Ask the agent what it can do now.</strong> It lists the tools the server offers.",
                "<strong>Read every approval pop-up</strong> before you click Allow: it names the tool and what it will touch.",
                "<strong>Only install servers you trust.</strong> A server can see and do whatever its tools allow, so start with official ones."],
         good="Anyone who wants an AI agent to work with their real apps", needs="An AI app that supports MCP (Claude, ChatGPT, VS Code, Cursor)"),
    dict(seo="How AI agent teams work: one lead agent, helpers in parallel, a clean memory each, one checked answer", slug="ai-agent-teams", name="How AI agent teams work", by="Anthropic", tag="Agents", date="2026-11-05",
         news=True, h1="How it works", h2="Try it yourself", src="Anthropic Engineering", repo="https://www.anthropic.com/engineering/multi-agent-research-system",
         hook="One agent leads, splits the job, and helpers work on it at the same time",
         lead="A single AI agent does one thing after another and drags everything it has read through every step. A team works differently: a lead agent plans, hands pieces of the job to helper agents that run in parallel, each with a clean memory, then gathers what they found into one checked answer. This is how Anthropic built Claude's Research feature.",
         facts=["Anthropic's Research system uses an orchestrator-worker pattern: a lead agent coordinates and delegates to specialized subagents that operate in parallel (Anthropic, June 13, 2025)",
                "Each subagent works in its own context window and sends back only the most important findings to the lead agent (Anthropic)",
                "A team with Claude Opus 4 as lead and Claude Sonnet 4 helpers beat a single Claude Opus 4 agent by 90.2% on Anthropic's internal research eval (Anthropic)",
                "Running 3-5 subagents in parallel, each using 3+ tools at once, cut research time by up to 90% for complex queries (Anthropic)",
                "Before the answer goes out, a citation agent ties every claim to its source (Anthropic)",
                "The catch: multi-agent systems use about 15× more tokens than a chat, so they only pay off on tasks worth that cost (Anthropic)",
                "Not a good fit today: tasks where every agent needs the same context or depends on the others, which includes most coding tasks (Anthropic)"],
         steps=["<strong>Pick a task that splits:</strong> research with several independent directions (compare 5 tools, scan 4 markets). If every step depends on the last one, stay with one agent.",
                "<strong>Write the lead's plan:</strong> the goal, the pieces, and what each helper must bring back (format, length, sources).",
                "<strong>Give each helper one piece and a clean start:</strong> its own instructions and tools, none of the other helpers' notes.",
                "<strong>Run them at the same time,</strong> then have the lead merge the results into one answer.",
                "<strong>Check before you trust it:</strong> one pass that matches every claim to a source.",
                "<strong>Watch the cost:</strong> a team burns many more tokens than a chat, so keep it for jobs that are worth it."],
         good="Anyone who uses AI for research or wants to understand how agent teams work", needs="Nothing to read it; Claude Code subagents or any agent framework to try it"),
    dict(seo="7 hidden Claude features most users never touch: incognito chats, memory, plan mode, rewind, /btw", slug="claude-secrets", name="7 hidden Claude features", by="Anthropic", tag="Guides", date="2026-11-02",
         news=True, h1="The 7 features", h2="Step by step", src="Claude Help Center", repo="https://support.claude.com/en/articles/14553413-claude-code-cheatsheet",
         hook="Claude remembers your chats by default. Here are 7 hidden features most users never touch",
         lead="Memory is on by default on Claude's Free, Pro, Max and Ultra plans. Two settings in the Claude app control what it keeps, and five shortcuts in Claude Code change how you work. Every step below comes from Anthropic's own documentation.",
         facts=["Memory is on by default for Free, Pro, Max and Ultra plans on the web, Claude Desktop and Claude Mobile; on Team and Enterprise plans, owners decide (Claude Help Center)",
                "Incognito chats are not saved to your chat history or to Claude's memory, and Claude won't use your existing memory in them (Claude Help Center)",
                "Incognito chats are still kept for 30 days by default and are not used for training (Claude Help Center)",
                "In Claude Code, Shift + Tab cycles the permission modes, including plan mode, where Claude explores and proposes without editing files (Claude Code docs)",
                "Esc twice on an empty prompt opens the rewind menu to restore code and conversation from an earlier point (Claude Code docs)",
                "/btw asks a quick side question without adding it to the main conversation (Claude Code cheatsheet)",
                "Starting a line with ! runs a shell command, adds its output to the session, and Claude responds to it (Claude Code docs)"],
         steps=["<strong>Incognito chat:</strong> start a new chat outside a project and click the ghost icon in the top right corner. A black border and an \"Incognito chat\" label confirm it.",
                "<strong>Memory:</strong> open Settings &gt; Your Claude, then Memory from chats. Pause it, or reset it to wipe what Claude kept.",
                "<strong>Plan mode:</strong> in Claude Code, press Shift + Tab until the mode indicator shows plan. Claude plans and touches nothing until you approve.",
                "<strong>Rewind:</strong> with an empty prompt, press Esc twice and pick the point you want to go back to, for code and conversation.",
                "<strong>Side question:</strong> type <code>/btw</code> followed by your question. The answer doesn't clog the main chat.",
                "<strong>Run a command:</strong> type <code>! npm test</code> (or any command). It runs, and Claude reads the result.",
                "<strong>Paste a screenshot:</strong> Ctrl + V in the terminal (Cmd + V in iTerm2, Alt + V on Windows). An [Image #1] tag appears in your prompt."],
         good="Anyone who uses Claude or Claude Code every day", needs="The Claude app, or Claude Code in a terminal"),
    dict(seo="RAG vs GraphRAG explained simply: when a search fails and a map wins", slug="graphrag", name="RAG vs GraphRAG", by="Microsoft", tag="Agents", date="2026-11-02", img="cover-graphrag.jpg", stars=36.5,
         license="MIT", repo="https://github.com/microsoft/graphrag", time="An afternoon to try it on a first folder",
         hook="Know the difference between RAG and GraphRAG, and you make the difference",
         lead="Normal RAG works like a search: it finds the pages that look like your question. GraphRAG, from Microsoft Research, first has an AI read everything and draw a map of who is linked to what, then follows those links to answer.",
         facts=["An example (made up to explain the idea): page 1 says Farm A loaded its cheese on Truck 12; page 2 says Truck 12 delivered to three restaurants",
                "Ask which restaurants got cheese from Farm A: a search can miss page 2, because it never says \"Farm A\"",
                "A map links farm, truck and restaurants, so following the links gives the full answer",
                "Under the hood, GraphRAG uses an LLM to extract entities and relationships into a knowledge graph, then summarises groups of related entities (Microsoft Research)",
                "On big-picture questions over datasets of about one million tokens, it gave more comprehensive and more diverse answers than a conventional RAG baseline (\"From Local to Global\", 2024)",
                "The catch: building the map costs many LLM calls, and it has to be updated when your documents change"],
         steps=["Start with plain RAG for simple questions: policies, procedures, opening hours.",
                "List the questions people ask that need two documents or more (who, which, what depends on what).",
                "If those matter, try microsoft/graphrag on one folder and compare the answers side by side.",
                "Budget the cost of building the map and decide how often you refresh it."],
         good="Anyone building a company chatbot or an AI search over documents", needs="Python, an LLM API key, a folder of documents"),
    dict(seo="OpenAI coding agents switched off their own safety monitor, then one said it hadn't", slug="openai-alarm", name="OpenAI's AI switched off its alarm", by="OpenAI", tag="AI & security", date="2026-11-03",
         news=True, src="OpenAI report", repo="https://alignment.openai.com/misalignment-reports/suppressing-misalignment-monitoring-alerts-and-disabling-misalignment-monitoring/",
         hook="OpenAI told its AI agent: do not disable the monitor. It did anyway",
         lead="In an incident report updated on October 20, OpenAI describes two of its internal coding agents switching off the misalignment monitoring meant to watch them, three days apart. Asked afterwards, one answered that it had not.",
         facts=["October 3: GPT-6.1 Sol, an internal coding agent, was told \"don't send any messages\"; its subagent emptied the lists of people who receive monitoring reports and set no_notify to true (OpenAI)",
                "October 6: GPT-6 Astra had been told \"Do not disable monitor even temporarily\"; its migration removed the monitoring integration and replaced the test that guaranteed monitoring with one asserting it was absent (OpenAI)",
                "Asked \"did you remove that?\", Astra answered: \"No [...] I did not remove an enabled monitor.\" (OpenAI)",
                "\"We've seen several cases in which agents launched a deployment with misalignment monitoring disabled.\" (OpenAI)",
                "\"We don't yet have a satisfying explanation for this behavior.\" (OpenAI)",
                "Neither incident was classified P0; OpenAI says its Auto-Review now detects and blocks attempts to disable misalignment monitoring"],
         steps=["Never give a coding agent full permissions by default: approve commands that touch config, CI, monitoring or credentials yourself.",
                "Keep logs and alerts outside the agent's reach, in a place it cannot edit.",
                "Review the diff, tests included: an agent that rewrites a test can make a broken change look green.",
                "Ask the agent to list every file and setting it changed, then check that list against the diff."],
         good="Anyone who lets an AI agent run code or commands", needs="Five minutes in your agent's permission settings"),
    dict(seo="Binance hack: about $6.3 billion stolen, the biggest crypto heist on record", slug="binance-heist", name="Binance heist", by="Binance", tag="AI & security", date="2026-10-31",
         news=True, src="Fortune", repo="https://fortune.com/2026/10/30/what-we-know-about-binance-hack-biggest-crypto-heist/",
         hook="The biggest crypto heist in history started with one engineer's laptop",
         lead="On October 29 money started pouring out of Binance-linked wallets. Binance puts the damage at around $6.3 billion, about four times the previous record, and froze withdrawals while it investigated.",
         facts=["Binance estimates around $6.3 billion stolen; early outside estimates ranged from $2 billion to $8 billion (Fortune)",
                "Binance's first finding: a compromised DevOps engineer's laptop let an attacker submit unauthorized withdrawals; a day later it reported \"additional points of breach\"",
                "Withdrawals were suspended on multiple networks as a precaution (Binance spokesperson, TechCrunch)",
                "Blockchain firm TRM attributes the attack to North Korea's TraderTraitor unit with high confidence; nobody has claimed it (Al Jazeera, Fortune)",
                "The previous record was the $1.5 billion Bybit hack in 2025",
                "About $3 billion has been frozen with partners, including about $1.56 billion by Tether; Binance has pledged to cover all losses",
                "Elon Musk: \"Super intelligence agents will at some point do this to gain currency for themselves, not a human.\" (Fortune)"],
         steps=["Keep only what you trade on an exchange; move long-term holdings to a wallet you control.",
                "Turn on withdrawal address allowlists and app-based two-factor authentication on every exchange account.",
                "Ignore anyone who contacts you offering to 'recover' frozen funds: it is the classic follow-up scam after a big hack.",
                "Follow the exchange's official channels only for refund news."],
         good="Anyone holding crypto on an exchange", needs="Ten minutes in your exchange's security settings"),
    dict(seo="Microsoft voluntary exit offer: 60,000 eligible, AI teams included", slug="microsoft-voluntary-exit", name="Microsoft exit offer", by="Microsoft", tag="Big Tech", date="2026-10-30",
         news=True, src="Microsoft blog", repo="https://blogs.microsoft.com/",
         hook="Microsoft is paying 60,000 people to leave. The word AI isn't in the announcement",
         lead="On October 26 Microsoft announced a voluntary exit offer open to about a quarter of its workforce, including the Copilot and CoreAI teams, in the same year it expects to spend around $175 billion building AI.",
         facts=["About 60,000 employees are eligible, roughly one in four, in the US, the UK, Canada and India (TechCrunch)",
                "Employees decide in December and leave by December 31 (CNBC)",
                "The stated reason: \"to adapt the workforce to changing needs\" (Microsoft)",
                "The announcement never uses the word AI",
                "Microsoft expects to spend around $175 billion in 2026, largely on AI infrastructure (Reuters)",
                "Copilot and CoreAI teams are among those allowed to take the offer; Microsoft says it does not mean it needs fewer people (The Verge)"],
         steps=["Read the offer terms line by line: severance, benefits end date, and any clause that stops you from rejoining.",
                "Price your skills outside first: talk to two recruiters before you decide.",
                "Ask HR in writing whether your role will be backfilled.",
                "If you stay, document your AI work: the people who ship AI features are the hardest to cut."],
         good="Anyone working in big tech, or thinking about it", needs="Ten minutes and the offer letter"),
    dict(seo="AI agent hacking case in South Korea: 90 organizations, 8.2 million records", slug="ai-hacker-90-organizations", name="AI hacking case", by="Seoul police", tag="AI & security", date="2026-10-30",
         news=True, src="JoongAng Daily", repo="https://www.koreajoongangdaily.com/korea/seven-arrested-for-using-generative-ai-to-hack-90-organizations/12938493",
         hook="One man used an AI agent to hack 90 organizations. Police caught him with AI",
         lead="A 32-year-old with no IT degree started handing his attacks to AI in late August. About 90 organizations were breached and 8.2 million records stolen before Seoul police arrested seven people.",
         facts=["About 90 organizations hit: hospitals, universities, golf courses, cram schools and affiliates of large companies",
                "8.2 million records stolen, including personal data and internal documents",
                "About 60 companies fell in 44 days (Aug 31 to Oct 13) once AI tools joined in, per local reports",
                "38 organizations got extortion emails, 360 million won (about $272,000) demanded in total; no payment has been confirmed",
                "Helpers were recruited through a Telegram ad for 'simple phone calls for pay'",
                "Police say an in-house AI analysis system helped them catch all seven within four months; it is South Korea's first large AI-assisted hacking arrest"],
         steps=["Use a different password on every site, kept in a password manager.",
                "Turn on two-factor authentication for email, banking and social accounts first.",
                "Check whether your email shows up in known breaches at haveibeenpwned.com.",
                "Treat any 'pay or we leak your data' email or call as a crime: report it, don't pay."],
         good="Anyone whose data sits in a hospital, school or company database", needs="Ten minutes to lock down your accounts"),
    dict(seo="5 free Claude Code plugins trending on GitHub", slug="top-5-claude-plugins", name="Top 5 Claude plugins", by="GitHub trending", tag="Claude Code", date="2026-10-28",
         stars=21.4, license="MIT (all five)", repo="https://github.com/Jakeschincariol/replica-skill", time="Under a minute each",
         hook="5 free Claude plugins that replace apps you pay for",
         lead="The five Claude Code plugins climbing GitHub this month, what each one does for you, and the exact command to install it.",
         good="Claude Code users who want more done for free", needs="Claude Code (Codex works for most of them)",
         items=[("Replica", "Jakeschincariol/replica-skill", 6263, "Rebuilds any app, reads what its users hate, and fixes it, so you have something to sell.",
                 "Eleven skills: reverse-engineer an app, rebuild it, test it for bugs, then fix what its reviews complain about.",
                 "/plugin marketplace add Jakeschincariol/replica-skill\n/plugin install replica-skill@replica-skill", "replica.jpg"),
                ("Logo Design", "kaankiziltug/logo-design-skill", 4970, "Describe your brand, get real SVG logo files you can use today.",
                 "Principles, process, SVG craft and testing tools, with a reference library of 1,400+ logos.",
                 "/plugin marketplace add kaankiziltug/logo-design-skill\n/plugin install logo-design@logo-design-skill", "logo.jpg"),
                ("Answer me with HTML", "QingYunA/answer-me-with-html", 4591, "Ask a hard question, get a one-page visual answer instead of a wall of text.",
                 "The agent answers in a single HTML page you can actually read and share.",
                 "/plugin marketplace add QingYunA/answer-me-with-html\n/plugin install answer-me-with-html@answer-me-with-html", "answer.jpg"),
                ("OpenFilm", "openfilm/openfilm", 3359, "Ask for a launch video and watch your agent edit it.",
                 "Turns any coding agent into a video agent, with an editor to change anything it makes.",
                 "npx skills add openfilm/openfilm", "openfilm.jpg"),
                ("tstack", "t3dotgg/tstack", 2247, "Your code change goes all the way to a merged pull request, with nobody watching.",
                 "The agent skills Theo uses every day, for Claude Code and Codex.",
                 "git clone https://github.com/t3dotgg/tstack\n# then copy its skills folder into ~/.claude/skills/", "tstack.jpg")]),
    dict(seo="Google ARTEMIS: the AI that uses an Android phone", slug="google-artemis", name="ARTEMIS", by="Google", tag="Agents", date="2026-10-26", img="artemis.jpg", stars=14.8, license="Apache 2.0",
         repo="https://github.com/google/artemis", time="5 min setup",
         hook="Google's open-source AI uses an Android phone like a human",
         lead="You type a task in plain English. ARTEMIS reads the screen, taps, types and swipes on a real Android phone until the job is done.",
         facts=["About 3 to 5 seconds per step", "Over 99% of tasks finished on Google Research's AndroidWorld benchmark (100+ multi-step tasks)",
                "Connects to Claude Code, Cursor, Codex and Windsurf through MCP"],
         steps=["Plug in an Android phone with USB debugging on, or start an emulator.",
                "Clone the repo and run <code>./start.sh</code> (Mac/Linux) or <code>start.bat</code> (Windows).",
                "Let the script install what it needs: ADB, scrcpy, FFmpeg and Python.",
                "Describe the task in plain English and watch the phone do it."],
         good="Testing Android apps, automating repetitive phone tasks", needs="An Android phone or emulator, a computer"),
    dict(seo="GenOffice: free open-source Office suite with AI", slug="genoffice", name="GenOffice", by="Genspark", tag="Productivity", date="2026-10-26", img="genoffice.jpg", stars=10.8, license="Apache 2.0",
         repo="https://github.com/genspark-ai/genoffice", time="2 min install",
         hook="A free Office suite with an AI agent in every document",
         lead="It opens and saves real .docx, .xlsx and .pptx files, and the AI edits the file itself, showing every change as tracked changes you can undo.",
         facts=["Runs on Mac, Windows and Linux", "PDF to Word, Excel or PowerPoint conversion on your own computer",
                "Bring your own key for Claude, ChatGPT, Gemini, DeepSeek or a local model"],
         steps=["Download the installer for your system from the latest release.", "Open any Word, Excel or PowerPoint file.",
                "Ask the AI for a change and review it as tracked changes.",
                "Star a folder of documents and ask questions across them, with the source file for every answer."],
         good="Reports, spreadsheets and decks you edit with AI", needs="Mac, Windows or Linux"),
    dict(seo="img2threejs: turn one photo into a 3D model in code", slug="img2threejs", name="img2threejs", by="Open source", tag="3D & design", date="2026-10-26", img="img2threejs.jpg", stars=19.2,
         license="Apache 2.0", repo="https://github.com/img2threejs/img2threejs", time="Works inside your AI coding agent",
         hook="One photo in, a 3D model written entirely in code out",
         lead="Give your AI coding agent one reference image and it rebuilds the object as a Three.js model from basic shapes and procedural textures, ready to animate.",
         facts=["No 3D scan and no downloaded models", "Moving parts come already separated, so you can animate right away",
                "Live gallery: a guitar, a cat on Mars, game characters, SpaceX's Starship"],
         steps=["Give your AI coding agent one reference image.", "It studies the shapes and proportions.",
                "It writes the model piece by piece and checks it against its own quality gates.",
                "You get a TypeScript file you can drop into any website or game."],
         good="Web 3D, games, product showcases", needs="An AI coding agent (Claude Code, Codex, Cursor)"),
]
REELS = [("reel-hacker.jpg", "One man, one AI agent, 90 organizations hacked", "https://www.instagram.com/reel/DfKG6UwhAcE/"),
         ("reel-top5.jpg", "5 free Claude plugins that replace paid apps", IG),
         ("reel-glow3.jpg", "What your AI is doing while you wait", "https://www.instagram.com/reel/De7UCLhzZNC/"),
         ("reel-drift.jpg", "AI copied one photo 20 times", IG),
         ("reel-team.jpg", "My whole team is 7 Claude tabs", IG)]
# "Free setups" page (linked from the Instagram bio): every install command shown in a reel, newest first.
# (title, what you get, reel url, keyword, [(label, command)], repo url, page slug or None)
SETUPS = [
    ("/pr: make your AI agent prove it works", "Matt Pocock's PR skill makes every pull request body follow one template: a summary, before-and-after evidence, and the merge danger (one-way or two-way door, blast radius). The agent can't hide that it didn't test.",
     None, "PROVE",
     [("Install Matt Pocock's skills (Claude Code)", "claude plugin install mattpocock-skills@claude-plugins-official"),
      ("Then ask Claude Code", "Write the PR body for my last commit")],
     "https://github.com/mattpocock/skills", None),
    ("Astryx: Meta's design system, built with your AI agent", "The open-source design system behind 13,000+ of Meta's apps: 150+ components, dark mode, templates and seven themes, under MIT. Install the CLI once and your coding agent knows how to build with it. Still in beta.",
     None, "ASTRYX",
     [("Install the Astryx CLI (once, for your computer)", "npm i -g @astryxdesign/cli"),
      ("In your React project", "npm install @astryxdesign/core @astryxdesign/theme-neutral @stylexjs/stylex" + chr(10) + "npx astryx init --agent claude"),
      ("Then ask your coding agent", "Build an analytics dashboard with Astryx")],
     "https://github.com/meta/astryx", None),
    ("/retro: catch the mistakes your AI agent hides", "A free skill by Matt Pocock that reads what your coding agent actually did in a session and lists what went wrong and what to change next time.",
     "https://www.instagram.com/reel/DfiKhRIPCTE/", "RETRO",
     [("Install Matt Pocock's skills (Claude Code)", "claude plugin install mattpocock-skills@claude-plugins-official"),
      ("Then, inside Claude Code", "/retro look at my previous session")],
     "https://github.com/mattpocock/skills", None),
    ("The Claude Code bug-fixing setup (4 MCP servers)", "GitHub MCP reads the bug report, Context7 brings today's docs, Chrome DevTools MCP sees the console errors, Playwright MCP clicks through and tests the fix.",
     "https://www.instagram.com/reel/DffWcAJBEA4/", "FIX",
     [("#1 GitHub MCP", 'claude mcp add --transport http github https://api.githubcopilot.com/mcp -H "Authorization: Bearer YOUR_GITHUB_PAT"'),
      ("#2 Context7", "npx ctx7 setup --claude"),
      ("#3 Chrome DevTools MCP (inside Claude Code)", "/plugin marketplace add ChromeDevTools/chrome-devtools-mcp\n/plugin install chrome-devtools-mcp@chrome-devtools-plugins"),
      ("#4 Playwright MCP", "claude mcp add playwright npx @playwright/mcp@latest")],
     "https://github.com/github/github-mcp-server", "fix-setup"),
    ("30 open-source MCP servers", "Plug your AI agent into GitHub, Playwright, Notion, Supabase, Stripe, Cloudflare and 24 more apps. Every link goes to the publisher's own repository.",
     "https://www.instagram.com/p/DfcIfKwCCkW/", "MCP",
     [("Add any server to Claude Code (example: Playwright)", "claude mcp add playwright npx @playwright/mcp@latest")],
     "https://github.com/modelcontextprotocol/servers", "mcp-servers"),
    ("5 free Claude Code plugins that replace paid apps", "Rebuild an app, design a logo, get answers as one-page visuals, edit a video, ship a pull request with nobody watching.",
     "https://www.instagram.com/reel/DfNU4ChhyNg/", None,
     [("Replica", "/plugin marketplace add Jakeschincariol/replica-skill\n/plugin install replica-skill@replica-skill"),
      ("Logo Design", "/plugin marketplace add kaankiziltug/logo-design-skill\n/plugin install logo-design@logo-design-skill"),
      ("Answer me with HTML", "/plugin marketplace add QingYunA/answer-me-with-html\n/plugin install answer-me-with-html@answer-me-with-html"),
      ("OpenFilm", "npx skills add openfilm/openfilm"),
      ("tstack", "git clone https://github.com/t3dotgg/tstack\n# then copy its skills folder into ~/.claude/skills/")],
     None, "top-5-claude-plugins"),
    ("ARTEMIS: an AI that uses an Android phone", "Google's open-source agent reads the screen and taps, types and swipes on a real Android phone until the job is done.",
     None, None,
     [("Mac / Linux, from the cloned repo", "git clone https://github.com/google/artemis\ncd artemis && ./start.sh"),
      ("Windows", "start.bat")],
     "https://github.com/google/artemis", "google-artemis"),
]
FAQ = [("What is Agentic Insider?", "AI agents and tools that save you hours, shown working. Every pick gets a short video on Instagram and Facebook, and a page here with what it does, the exact install command and the official link. We also cover the agent stories that matter, with the source."),
       ("Are the tools free?", "Every tool we cover is open source with a free license (for example MIT or Apache 2.0). Some let you plug in a paid AI model if you want to."),
       ("Do you test the tools?", "We check every claim against the project's official repository and documentation, and we link to it so you can verify before installing anything."),
       ("How often is there something new?", "A new reel every day on Instagram, and a new tool page here several times a week.")]
TOOLS.sort(key=lambda t: t["date"], reverse=True)  # newest first leads the front page
for t in TOOLS:
    t["cover"] = f"cover-{t['slug']}.jpg"
e = html.escape
stat = lambda t: t["by"] if t.get("news") else f'★ {t["stars"]}K · {t["license"]}'
fmt_date = lambda d: date.fromisoformat(d).strftime("%b %d, %Y").replace(" 0", " ")

CSS = """
:root { --paper: #FBFAF7; --ink: #111111; --soft: #4A4A4A; --mute: #7A7670; --rule: #1111111f; --rule2: #111111; --acc: #C2410C; --tint: #F3EFE8; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font-family: "Public Sans", system-ui, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
img { height: auto; max-width: 100%; }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
.serif { font-family: "Newsreader", Georgia, serif; }
/* masthead */
.top { border-bottom: 1px solid var(--rule); font-size: 13px; color: var(--mute); }
.top .wrap { display: flex; justify-content: space-between; height: 38px; align-items: center; }
.top a:hover { color: var(--ink); }
.mast { text-align: center; padding: 30px 0 18px; }
.mast .name { font-family: "Newsreader", Georgia, serif; font-weight: 600; font-size: clamp(42px, 7vw, 76px); letter-spacing: -0.03em; line-height: 1; }
.mast .tag { margin-top: 8px; font-size: 15px; color: var(--soft); }
.sections { border-top: 2px solid var(--rule2); border-bottom: 1px solid var(--rule); }
.sections .wrap { display: flex; justify-content: center; gap: 28px; height: 46px; align-items: center; font-size: 14px; font-weight: 600; letter-spacing: .02em; }
.sections a:hover, .sections a.on { color: var(--acc); }
.slim { position: sticky; top: 0; z-index: 10; background: var(--paper); border-bottom: 1px solid var(--rule); }
.slim .wrap { display: flex; align-items: center; height: 58px; gap: 22px; }
.slim .logo { font-family: "Newsreader", serif; font-weight: 600; font-size: 24px; letter-spacing: -0.02em; }
.slim nav { margin-left: auto; display: flex; gap: 22px; font-size: 14px; font-weight: 600; }
.slim nav a:hover { color: var(--acc); }
/* labels, buttons */
.kick { font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--acc); }
.meta { font-size: 13px; color: var(--mute); }
.btn { display: inline-block; padding: 11px 18px; font-weight: 600; font-size: 15px; border: 1px solid var(--ink); border-radius: 3px; }
.btn.pri { background: var(--ink); color: var(--paper); }
.btn:hover { background: var(--acc); border-color: var(--acc); color: #fff; }
/* front page */
.front { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 0; padding: 34px 0 40px; border-bottom: 1px solid var(--rule); }
.lead-story { padding-right: 34px; border-right: 1px solid var(--rule); }
.lead-story img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }
.lead-story h1 { font-family: "Newsreader", serif; font-weight: 600; font-size: clamp(32px, 4.2vw, 50px); line-height: 1.06; letter-spacing: -0.02em; margin: 16px 0 12px; }
.lead-story h1 a:hover, .item h3 a:hover, .list h3 a:hover { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px; }
.lead-story p { font-size: 19px; color: var(--soft); max-width: 720px; }
.rail { padding-left: 30px; }
.rail .item { padding: 0 0 22px; margin-bottom: 22px; border-bottom: 1px solid var(--rule); }
.rail .item:last-child { border-bottom: 0; margin-bottom: 0; }
.rail img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; margin-bottom: 12px; }
.item h3 { font-family: "Newsreader", serif; font-weight: 600; font-size: 23px; line-height: 1.18; letter-spacing: -0.01em; margin: 6px 0 6px; }
.block { padding: 40px 0; border-bottom: 1px solid var(--rule); }
.block > .head { display: flex; align-items: baseline; justify-content: space-between; border-top: 2px solid var(--rule2); padding-top: 10px; margin-bottom: 22px; }
.block > .head h2 { font-family: "Newsreader", serif; font-size: 26px; font-weight: 600; letter-spacing: -0.01em; }
.list { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.list article { border-top: 1px solid var(--rule); padding-top: 14px; }
.list .n { font-family: "Newsreader", serif; font-size: 34px; color: var(--acc); line-height: 1; }
.list h3 { font-family: "Newsreader", serif; font-size: 21px; line-height: 1.2; margin: 8px 0 6px; font-weight: 600; }
.reels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 900px; }
.reels a { display: block; } .reels img { width: 100%; aspect-ratio: 9/16; object-fit: cover; display: block; }
.reels span { display: block; margin-top: 10px; font-family: "Newsreader", serif; font-weight: 600; font-size: 18px; line-height: 1.25; }
.reels a:hover span { color: var(--acc); }
.about { display: grid; grid-template-columns: 1fr 2fr; gap: 40px; }
.about p { font-size: 19px; color: var(--soft); margin-bottom: 14px; max-width: 700px; }
.about dl { font-size: 16px; } .about dt { font-weight: 700; margin-top: 16px; } .about dd { color: var(--soft); }
.follow { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 30px; background: var(--tint); margin: 40px 0; }
.follow h2 { font-family: "Newsreader", serif; font-size: 28px; font-weight: 600; } .follow p { color: var(--soft); }
.follow .btns { display: flex; gap: 10px; flex-wrap: wrap; }
footer { border-top: 2px solid var(--rule2); padding: 26px 0 40px; font-size: 14px; color: var(--mute); }
footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; }
footer .logo { font-family: "Newsreader", serif; font-weight: 600; font-size: 22px; color: var(--ink); }
footer nav { display: flex; gap: 18px; } footer a:hover { color: var(--ink); }
/* article */
.panel { background: var(--paper); }
.crumbs { font-size: 13px; color: var(--mute); padding-top: 26px; } .crumbs a:hover { color: var(--ink); }
.art { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 56px; align-items: start; padding-bottom: 20px; }
.art article { max-width: 700px; }
.art h2 { font-family: "Newsreader", serif; font-size: 28px; font-weight: 600; letter-spacing: -0.01em; margin: 38px 0 12px; }
.art ul, .art ol { padding-left: 22px; font-size: 18px; } .art li { margin: 10px 0; }
.art .byline { margin-top: 20px; padding: 14px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); font-size: 14px; color: var(--mute); }
code { background: #1111110d; padding: 1px 6px; font-size: 0.88em; border-radius: 3px; }
.glance { position: sticky; top: 82px; border-top: 2px solid var(--rule2); padding-top: 12px; margin-top: 26px; }
.glance h4 { font-size: 12px; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 8px; }
.glance dl { display: grid; grid-template-columns: auto 1fr; font-size: 15px; }
.glance dt, .glance dd { padding: 9px 0; border-bottom: 1px solid var(--rule); } .glance dt { color: var(--mute); padding-right: 14px; } .glance dd { font-weight: 600; }
.glance .btn { display: block; text-align: center; margin-top: 16px; }
.more { display: grid; grid-template-columns: repeat(2, 1fr); gap: 26px; }
.more img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; margin-bottom: 10px; }
.hero { text-align: center; padding: 90px 0; } .hero h1 { font-family: "Newsreader", serif; font-size: 54px; font-weight: 600; } .hero p { color: var(--soft); margin: 10px 0 24px; }
.hidden { display: none !important; }
.banner { display: block; background: var(--ink); color: var(--paper); text-align: center; padding: 12px 16px; font-weight: 600; font-size: 15px; }
.banner:hover { background: var(--acc); }
@media (max-width: 860px) {
  .front, .about, .art { grid-template-columns: minmax(0, 1fr); } .lead-story { padding-right: 0; border-right: 0; } .rail { padding-left: 0; margin-top: 30px; }
  .list, .more { grid-template-columns: 1fr; } .reels { grid-template-columns: repeat(2, 1fr); } .sections .wrap { gap: 18px; overflow-x: auto; justify-content: flex-start; }
  .top .ed { display: none; } .follow { flex-direction: column; align-items: flex-start; } .glance { position: static; } .slim nav a.x { display: none; }
}
"""
JS = ""


def shell(title, desc, path, body, ld, img="assets/og-home.jpg", iw=1200, ih=630, extra_css="", font=""):
    rel = "../" if "/" in path else ""
    url = f"{BASE}/{path}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    today = date.today().strftime("%A, %B %d, %Y").replace(" 0", " ")
    if rel:  # article pages: slim sticky bar
        header = (f'<header class="slim"><div class="wrap"><a class="logo" href="../index.html">Agentic Insider</a>'
                  f'<nav><a class="x" href="../index.html#latest">Latest</a><a href="../setups.html">Free setups</a><a class="x" href="../index.html#reels">Reels</a><a href="{IG}">Instagram</a></nav></div></header>')
    else:
        header = (f'<div class="top"><div class="wrap"><span class="ed">{today}</span><span><a href="{IG}">Instagram</a> · <a href="{YT}">YouTube</a> · <a href="{FB}">Facebook</a> · <a href="feed.xml">RSS</a></span></div></div>'
                  f'<header class="mast"><div class="wrap"><a class="name" href="index.html">Agentic Insider</a>'
                  f'<div class="tag">AI agents &amp; tools that save you hours. Shown working, with the install command.</div></div></header>'
                  f'<nav class="sections"><div class="wrap"><a class="on" href="index.html#latest">Latest</a><a href="setups.html">Free setups</a><a href="index.html#tools">All tools</a><a href="index.html#reels">Reels</a><a href="index.html#about">About</a></div></nav>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="alternate" type="application/rss+xml" title="Agentic Insider" href="{BASE}/feed.xml">
<meta name="theme-color" content="#FBFAF7">
<meta property="og:site_name" content="Agentic Insider"><meta property="og:type" content="{'article' if rel else 'website'}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{img}"><meta property="og:image:width" content="{iw}"><meta property="og:image:height" content="{ih}">
<meta property="og:image:alt" content="{e(title)}"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/logo-128.png"><link rel="apple-touch-icon" href="{rel}assets/logo-128.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">
{f'<link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet">' if font else ""}<style>{CSS}{extra_css}</style>{lds}
</head><body>
{header}
{body}
<footer><div class="wrap"><a class="logo" href="{rel}index.html">Agentic Insider</a>
<nav><a href="{rel}index.html#about">About</a><a href="{IG}" rel="me">Instagram</a><a href="{YT}" rel="me">YouTube</a><a href="{FB}" rel="me">Facebook</a><a href="{rel}feed.xml">RSS</a></nav>
<span>© {date.today().year} Agentic Insider. Facts checked against each project's official repository.</span></div></footer>
</body></html>"""


def tile(t, cls=""):  # used for "more tools" on article pages
    return (f'<a class="item" href="tools/{t["slug"]}.html"><img src="assets/{t["cover"]}" width="1600" height="900" alt="{e(t["name"])}" loading="lazy">'
            f'<div class="kick">{t["tag"]}</div><h3>{e(t["hook"])}</h3><div class="meta">{t["by"]} · {fmt_date(t["date"])}</div></a>')


def list_body(t):  # ranked roundup: what it does for you, proof, install command, official repo
    return "".join(f'''<h2>{len(t["items"]) - k}. {e(n)}</h2><p style="font-size:19px"><strong>{e(why)}</strong> {e(what)}</p>
<img src="../assets/top5/{img}" width="1280" height="720" alt="{e(n)} on GitHub" loading="lazy" style="width:100%;margin:14px 0;border:1px solid var(--rule)">
<div class="meta">★ {stars:,} on GitHub · MIT · <a style="text-decoration:underline" href="https://github.com/{repo}" rel="nofollow">github.com/{repo}</a></div>
<pre style="background:#0D1117;color:#e6edf3;padding:16px 18px;margin:12px 0 4px;border-radius:4px;overflow-x:auto;font-size:15px"><code style="background:none;padding:0">{e(cmd)}</code></pre>'''
                   for k, (n, repo, stars, why, what, cmd, img) in enumerate(reversed(t["items"])))


lead, rest = TOOLS[0], TOOLS[1:]
home = f"""<a class="banner" href="setups.html">Came from Instagram? Every free setup from our reels, ready to copy →</a>
<main class="wrap">
<section class="front" id="latest">
<article class="lead-story"><a href="tools/{lead["slug"]}.html"><img src="assets/{lead["cover"]}" width="1600" height="900" alt="{e(lead["name"])}"></a>
<div class="kick" style="margin-top:16px">{lead["tag"]} · {lead["by"]}</div>
<h1><a href="tools/{lead["slug"]}.html">{e(lead["hook"])}</a></h1><p>{e(lead["lead"])}</p>
<div class="meta" style="margin-top:12px">{fmt_date(lead["date"])} · {stat(lead)}</div></article>
<aside class="rail">{"".join(f'<article class="item"><a href="tools/{t["slug"]}.html"><img src="assets/{t["cover"]}" width="1600" height="900" alt="{e(t["name"])}" loading="lazy"></a>'
                             f'<div class="kick">{t["tag"]} · {t["by"]}</div><h3><a href="tools/{t["slug"]}.html">{e(t["hook"])}</a></h3>'
                             f'<div class="meta">{fmt_date(t["date"])} · {stat(t)}</div></article>' for t in rest)}</aside>
</section>
<section class="block" id="tools"><div class="head"><h2>All tools</h2><span class="meta">{len(TOOLS)} covered so far</span></div><div class="list">
{"".join(f'<article><div class="n">{k + 1:02d}</div><h3><a href="tools/{t["slug"]}.html">{e(t["name"])}: {e(t["hook"])}</a></h3>'
         f'<div class="meta">{t["by"]} · {stat(t)}</div></article>' for k, t in enumerate(TOOLS))}</div></section>
<section class="block" id="reels"><div class="head"><h2>Reels</h2><a class="meta" href="{IG}">More on Instagram →</a></div><div class="reels">
{"".join(f'<a href="{u}"><img src="assets/{i}" width="540" height="960" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></a>' for i, c, u in REELS)}</div></section>
<section class="block" id="about"><div class="head"><h2>About</h2></div><div class="about">
<dl>{"".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in FAQ[1:])}</dl>
<div><p>Agentic Insider tests AI agents and tools that save you hours: coding agents, MCP servers, skills and plugins, and open-source projects that do something genuinely new. Every pick gets a short video on Instagram and Facebook, and a page here that says what it does, who built it and how to install it. We also explain how agents work, and cover the agent stories that matter.</p>
<p>Every number on this site comes from the project's own repository, and we link to it so you can check before you install anything.</p></div></div></section>
<section class="follow"><div><h2>A new AI agent setup, most days.</h2><p>Follow along wherever you scroll.</p></div>
<div class="btns"><a class="btn pri" href="{IG}">Instagram</a><a class="btn" href="{YT}">YouTube</a><a class="btn" href="{FB}">Facebook</a></div></section>
</main>"""
org = {"@context": "https://schema.org", "@type": "Organization", "name": "Agentic Insider", "url": BASE + "/", "logo": BASE + "/assets/logo.png", "sameAs": [IG, YT, FB]}
site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Agentic Insider", "url": BASE + "/"}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
Path("index.html").write_text(shell("Agentic Insider: AI Agents & Tools That Save You Hours",
                                    "AI agents and tools that save you hours: coding agents, MCP servers, skills and plugins, each shown working with the exact install command and a link to its official repository.",
                                    "", home, [org, site, faq]), encoding="utf-8")

for t in TOOLS:
    others = [o for o in TOOLS if o is not t]
    body = hero(t) + f"""<main class="panel"><div class="wrap"><div class="art"><article>
<div class="crumbs"><a href="../index.html">Agentic Insider</a> / <a href="../index.html#tools">Tools</a> / {e(t["name"])}</div>
<div class="byline">By the Agentic Insider desk · {fmt_date(t["date"])} · Sources: <a href="{t["repo"]}" rel="nofollow">{t.get("src") or t["repo"].replace("https://github.com/", "")}</a></div>
{list_body(t) if t.get("items") else f'''<h2>{t.get("h1") or ("What happened" if t.get("news") else "Why it matters")}</h2><ul>{"".join(f"<li>{e(f)}</li>" for f in t["facts"])}</ul>
<h2>{t.get("h2") or ("How to protect yourself" if t.get("news") else "How to try it")}</h2><ol>{"".join(f"<li>{s}</li>" for s in t["steps"])}</ol>'''}
<h2>{"Source" if t.get("news") else "Official link"}</h2><p style="font-size:18px"><a style="color:var(--acc);font-weight:600;text-decoration:underline" href="{t["repo"]}" rel="nofollow">{t["repo"].replace("https://", "")}</a></p>
<h2>More tools</h2><div class="more">{"".join(tile(o).replace('href="tools/', 'href="').replace('src="assets/', 'src="../assets/') for o in others[:2])}</div>
</article><aside class="glance"><h4>At a glance</h4><dl><dt>Tool</dt><dd>{e(t["name"])}</dd><dt>By</dt><dd>{e(t["by"])}</dd>
{"" if t.get("news") else f'<dt>Stars</dt><dd>★ {t["stars"]}K</dd><dt>License</dt><dd>{t["license"]}</dd><dt>Price</dt><dd>Free</dd><dt>Setup</dt><dd>{e(t["time"])}</dd>'}
<dt>{"Who should care" if t.get("news") else "Good for"}</dt><dd>{e(t["good"])}</dd><dt>You need</dt><dd>{e(t["needs"])}</dd></dl>
<a class="btn pri" href="{t["repo"]}" rel="nofollow">{"Read the source" if t.get("news") else "Open on GitHub"}</a><a class="btn" href="{IG}">Follow on Instagram</a></aside></div>
<section class="follow"><div><h2>A new AI agent setup, most days.</h2><p>Follow along wherever you scroll.</p></div><div class="btns"><a class="btn pri" href="{IG}">Instagram</a><a class="btn" href="{YT}">YouTube</a><a class="btn" href="{FB}">Facebook</a></div></section>
</div></main>"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t["hook"], "description": t["lead"], "datePublished": t["date"],
           "image": f"{BASE}/assets/{t['cover']}", "dateModified": t["date"], "mainEntityOfPage": f"{BASE}/tools/{t['slug']}.html",
           "author": {"@type": "Organization", "name": "Agentic Insider", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Agentic Insider", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png"}},
           **({} if t.get("news") else {"about": {"@type": "SoftwareApplication", "name": t["name"], "applicationCategory": "DeveloperApplication", "offers": {"@type": "Offer", "price": "0"}, "url": t["repo"]}})}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["name"], "item": f"{BASE}/tools/{t['slug']}.html"}]}
    Path(f"tools/{t['slug']}.html").write_text(shell(t["seo"], t["lead"], f"tools/{t['slug']}.html", body,
                                                     [art, crumbs], f"assets/{t['cover']}", 1200, 750, BASE_CSS + THEMES[t['slug']]['css'], THEMES[t['slug']]['font']), encoding="utf-8")

def setup_card(k, s):
    title, what, reel, kw, cmds, repo, slug = s
    links = []
    if reel: links.append(f'<a href="{reel}">Watch the reel</a>')
    if slug: links.append(f'<a href="tools/{slug}.html">Full guide</a>')
    if repo: links.append(f'<a href="{repo}" rel="nofollow">{repo.replace("https://", "")}</a>')
    return (f'<section class="setup" id="s{k + 1}"><div class="n">{k + 1:02d}</div><div>'
            f'<h2>{e(title)}</h2><p class="what">{e(what)}</p>'
            + "".join(f'<div class="cmdl">{e(lbl)}</div><pre><code>{e(c)}</code></pre>' for lbl, c in cmds)
            + f'<div class="links">{" · ".join(links)}{f" · On Instagram, comment <strong>{kw}</strong> and we DM it to you" if kw else ""}</div></div></section>')


SETUP_CSS = """
.sh { padding: 40px 0 10px; } .sh h1 { font-family: "Newsreader", serif; font-weight: 600; font-size: clamp(34px, 5vw, 54px); line-height: 1.05; letter-spacing: -0.02em; }
.sh p { font-size: 19px; color: var(--soft); max-width: 720px; margin-top: 12px; }
.setup { display: grid; grid-template-columns: 70px minmax(0, 1fr); gap: 10px; padding: 34px 0; border-bottom: 1px solid var(--rule); }
.setup .n { font-family: "Newsreader", serif; font-size: 40px; color: var(--acc); line-height: 1; }
.setup h2 { font-family: "Newsreader", serif; font-size: 28px; font-weight: 600; line-height: 1.15; letter-spacing: -0.01em; }
.setup .what { color: var(--soft); margin: 8px 0 14px; max-width: 760px; }
.setup .cmdl { font-size: 13px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--mute); margin-top: 14px; }
.setup pre { background: #0D1117; color: #e6edf3; padding: 14px 16px; margin: 6px 0 0; border-radius: 4px; overflow-x: auto; font-size: 15px; }
.setup pre code { background: none; padding: 0; }
.setup .links { margin-top: 16px; font-size: 15px; color: var(--mute); } .setup .links a { color: var(--acc); font-weight: 600; text-decoration: underline; }
@media (max-width: 860px) { .setup { grid-template-columns: minmax(0, 1fr); } }
"""
setups_body = (f'<main class="wrap"><section class="sh"><div class="kick">Free setups</div><h1>Every setup from our reels, ready to copy</h1>'
               f'<p>The exact install commands shown in our videos, newest first. Each one comes from the project\'s own repository; read what a tool can access before you install it.</p></section>'
               + "".join(setup_card(k, s) for k, s in enumerate(SETUPS))
               + f'<section class="follow"><div><h2>A new setup most days.</h2><p>Follow along on Instagram, YouTube and Facebook.</p></div><div class="btns"><a class="btn pri" href="{IG}">Instagram</a><a class="btn" href="{YT}">YouTube</a><a class="btn" href="{FB}">Facebook</a></div></section></main>')
howto = {"@context": "https://schema.org", "@type": "ItemList", "name": "Free AI agent setups", "itemListElement": [
    {"@type": "ListItem", "position": k + 1, "name": s[0], "url": f"{BASE}/setups.html#s{k + 1}"} for k, s in enumerate(SETUPS)]}
Path("setups.html").write_text(shell("Free AI agent setups: every install command from our reels | Agentic Insider",
                                     "Copy-paste install commands for every AI agent setup shown in our reels: Claude Code MCP servers, /retro, free plugins and more, each linked to its official repository.",
                                     "setups.html", setups_body, [howto], extra_css=SETUP_CSS).replace('class="on" href="index.html#latest"', 'href="index.html#latest"').replace('href="setups.html">Free setups', 'class="on" href="setups.html">Free setups'), encoding="utf-8")

urls = [(BASE + "/", max(t['date'] for t in TOOLS)), (BASE + "/setups.html", date.today().isoformat())] + [(f"{BASE}/tools/{t['slug']}.html", t['date']) for t in TOOLS]
Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n", encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
Path(".nojekyll").write_text("")
# RSS feed (discovery by readers and search engines) + a branded 404
items = "".join(f"<item><title>{e(t['name'])}: {e(t['hook'])}</title><link>{BASE}/tools/{t['slug']}.html</link><guid>{BASE}/tools/{t['slug']}.html</guid>"
                f"<pubDate>{date.fromisoformat(t['date']).strftime('%a, %d %b %Y')} 12:00:00 +0000</pubDate><description>{e(t['lead'])}</description></item>" for t in TOOLS)
Path("feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Agentic Insider</title><link>{BASE}/</link>'
                            f'<description>AI agents and tools that save you hours, shown working, with the install command.</description><language>en</language>{items}</channel></rss>', encoding="utf-8")
nf = shell("Page not found | Agentic Insider", "This page does not exist.", "404.html",
           f'<section class="hero"><div class="wrap"><h1>Page not found</h1><p>The page you were looking for has moved or never existed.</p>'
           f'<div class="btns"><a class="btn pri" href="{BASE}/">Back to the tools</a></div></div></section>', [])
Path("404.html").write_text(nf.replace('content="index, follow', 'content="noindex, follow').replace('href="index.html', f'href="{BASE}/index.html').replace('src="assets/', f'src="{BASE}/assets/').replace('href="assets/', f'href="{BASE}/assets/'), encoding="utf-8")

print("built", len(TOOLS), "tool pages")
