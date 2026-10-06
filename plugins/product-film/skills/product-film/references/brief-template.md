# What to write: the brief

Everything Claude needs to start fits in one message: the brief. Write it once, paste
it after `/product-film`, and Claude does the rest, stopping only for decisions. A good
brief saves hours of back and forth; a vague one ("make a cool video for my app") gets
a film about features nobody asked for.

## The template

Copy this, replace every line, delete lines that do not apply:

```text
/product-film

PRODUCT: <what it is, in one sentence>
PAGE: <the URL of the page the film will sit on>
LENGTH AND FORMATS: <e.g. 50 seconds, landscape and square>
WHO WATCHES: <the buyer: role, company size, situation>

PROBLEMS (3 or 4, in the buyer's words):
1. <problem>
2. <problem>
3. <problem>

HOW THE PRODUCT SOLVES EACH (the screen or flow that shows it):
1. <screen / flow>
2. <screen / flow>
3. <screen / flow>

SIGNATURE MOMENT (the one thing a viewer should remember; must be real today):
<e.g. the whole app switching to the client's brand>

ONE CLIENT TO CARRY THROUGH (fictional): <name, or "none">

CALL TO ACTION: <primary button text> / <secondary button text>
PROOF: <cleared customer logos, a quote you may use, or "none">

STYLE: <problem-led story / crisp real-app / chapter>
MUSIC: <mood and tempo, e.g. upbeat, around 120 BPM; or a track you already licensed>

NEVER SHOW: <beta tags, real customer names, competitors, prices, anything else>
BRAND: <primary colour hex>, <fonts>, <logo file or URL>

SCREENS COME FROM: <a local build of the app at <path or repo>, or design-file exports at <link>>
DEMO DATA: <the app's demo workspace / seed script / fixtures, and any names to replace>

WHO SIGNS OFF: <you, or a named person>
PUBLISHING: <not until I say so>
```

## What each field is for, with a good and a bad answer

| Field | Why Claude needs it | Good | Bad |
|---|---|---|---|
| PRODUCT | one sentence the film must never contradict | "Social media management for agencies: schedule, approve and report across many clients." | "An AI-powered all-in-one platform." |
| PAGE | the only source of claims; every on-screen word must come from it or be approved by you | the exact URL of the landing page the film sits on | the home page when the film goes on the agency page |
| WHO WATCHES | decides the problems, the words, the pace | "Owners of agencies running 10 to 50 client accounts, tired of email approvals." | "Everyone." |
| PROBLEMS | the spine of the film; each becomes a "before" scene | "Clients take days to approve posts over email." | "Approvals feature." |
| HOW IT SOLVES EACH | tells Claude which screens to capture | "The client opens an emailed link and clicks Approve, no account needed." | "Show approvals." |
| SIGNATURE MOMENT | the one thing that makes it memorable; put on the biggest music lift | "The app re-skins to the agency's brand in place." | "Lots of animations." |
| CLIENT | makes four features read as one agency's week | "Quillhaven Coffee (fictional)." | a real customer's name |
| CALL TO ACTION | the film ends on it, pressed on the final beat | "Book a demo / Start free" | "Learn more about our solutions" |
| PROOF | earned after the payoff | "These 8 logos are cleared for the website: <files>." | logos nobody cleared |
| STYLE | decides how features are introduced | "Problem-led story." | "Make it pop." |
| MUSIC | the music decides the structure; licence matters | "Upbeat, 115 to 125 BPM, licence allows web and ads, no remixing needed." | a popular song you do not have rights to |
| NEVER SHOW | becomes a forbidden-strings check on every frame | "No 'beta', no 'Sample data' chips, no real client names." | (left empty, then found in the review) |
| SCREENS COME FROM | real product only; AI-generated UI is never allowed | "Local build of our web app, branch prod, demo workspace." | "Generate some nice screens." |
| WHO SIGNS OFF | decisions and approvals are recorded against a person | "Me." | (left empty) |

## Example 1: problem-led landing-page hero (filled in)

```text
/product-film

PRODUCT: Social media management for agencies: schedule, approve and report across many client accounts.
PAGE: https://www.example.com/agencies
LENGTH AND FORMATS: 50 seconds, landscape and square
WHO WATCHES: owners and account leads at agencies with 10 to 50 client accounts

PROBLEMS:
1. Clients take days to approve posts over email
2. Every client's posts are mixed in one calendar
3. Clients see the tool's branding instead of the agency's
4. Report day means hours in spreadsheets

HOW THE PRODUCT SOLVES EACH:
1. The client opens an emailed link and clicks Approve, no account needed (Post Approval screen)
2. A workspace per client; the switcher shows each one (workspace switcher)
3. White label: the app in the agency's own logo and colours (re-skin on a tenant domain)
4. Reports the client can open, exported as PDF or slides (Analytics, Export menu)

SIGNATURE MOMENT: the real app re-skinning from our brand to the agency's, in place
ONE CLIENT TO CARRY THROUGH: Quillhaven Coffee (fictional)

CALL TO ACTION: Book a demo / Start free
PROOF: the 8 customer logos cleared for the website (files in brand/logos)

STYLE: problem-led story
MUSIC: upbeat, around 123 BPM, licence allows web and ads

NEVER SHOW: "beta", "Sample data", real customer names, prices
BRAND: #FF6900, Bricolage Grotesque and DM Sans, logo at brand/wordmark.svg

SCREENS COME FROM: a local build of the web app (repo at ../app, branch prod)
DEMO DATA: the app's demo workspace; rename the demo brand to Quillhaven Coffee

WHO SIGNS OFF: me
PUBLISHING: not until I say so
```

## Example 2: a single feature launch (filled in)

```text
/product-film

PRODUCT: A content calendar for small marketing teams.
PAGE: https://www.example.com/features/bulk-scheduling
LENGTH AND FORMATS: 30 seconds, landscape, square and 9:16
WHO WATCHES: social media managers who schedule 50+ posts a week

PROBLEMS:
1. Scheduling a month of posts one by one takes an afternoon

HOW THE PRODUCT SOLVES IT:
1. Upload a CSV, pick time slots, approve 40 posts at once (Bulk Upload screen, then the filled calendar)

SIGNATURE MOMENT: the empty calendar filling with 40 posts in one beat
ONE CLIENT TO CARRY THROUGH: none

CALL TO ACTION: Try bulk scheduling
PROOF: none

STYLE: crisp real-app
MUSIC: energetic, around 120 BPM

NEVER SHOW: "beta", the pricing page
BRAND: #2563EB, Inter, logo at assets/logo.svg

SCREENS COME FROM: a local build of the app (repo at ../web, branch main)
DEMO DATA: the seed script `npm run seed:demo`

WHO SIGNS OFF: our head of marketing, Priya
PUBLISHING: not until I say so
```

## Example 3: a brand introduction (filled in)

```text
/product-film

PRODUCT: An invoicing app for freelancers.
PAGE: https://www.example.com
LENGTH AND FORMATS: 45 seconds, landscape and square
WHO WATCHES: first-time visitors who freelance and hate chasing payments

PROBLEMS:
1. Making an invoice takes too long
2. Clients pay late
3. Taxes are a mess at year end

HOW THE PRODUCT SOLVES EACH:
1. An invoice from a template in three clicks
2. Automatic reminders and a pay-now link
3. A yearly summary ready for the accountant

SIGNATURE MOMENT: a "Paid" stamp landing on the invoice on the music's biggest hit
ONE CLIENT TO CARRY THROUGH: none

CALL TO ACTION: Start free
PROOF: none

STYLE: chapter (a title card per feature, playful stickers)
MUSIC: warm and upbeat, around 110 BPM

NEVER SHOW: real client names, bank details
BRAND: #10B981, Manrope, logo at brand/logo.svg

SCREENS COME FROM: design-file exports at <link> (the app is being rebuilt)
DEMO DATA: the fictional client "Northfield Studio" already in the designs

WHO SIGNS OFF: me
PUBLISHING: not until I say so
```

## After the brief

Claude replies with questions for anything missing, then works through the steps in
`walkthrough.md`. The messages you will type after the brief are short; see
`recipes.md`. The ones you will use most:

```text
Show me.
Approve with your recommended defaults.
Push them further.
Print the approval command.
Run the delivery and open the folder.
```
