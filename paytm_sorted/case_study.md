# Product Teardown: Paytm UPI for Young India (15-25)

**Author:** Product Management Student  
**Date:** July 2026  
**Lens:** How does Paytm's UPI experience serve India's 350 million 15-25 year olds?  
**Data:** NPCI published data, Paytm investor relations (FY26), industry reports

> [!NOTE]
> This teardown uses public data, app observation, and structured hypotheses. Internal metrics are not claimed. Assumptions are marked clearly.

---

## 1. Product Overview

### What Paytm Does

Paytm is a payments app that lets you send money, pay at shops, recharge your phone, and pay bills using UPI. It also sells financial products like insurance and loans.

### Why It Matters for This Teardown

India has roughly 350 million people aged 15-25. About 67% of India's population is under 35. This is the generation that will decide which payment app wins the next decade.

But Paytm wasn't built for them. It was built for everyone, and it shows.

### Where Paytm Stands Today

| Metric | Number | Source |
|---|---|---|
| UPI market share (volume) | 7.9% | NPCI, May 2026 |
| PhonePe share | 46.2% | NPCI, May 2026 |
| Google Pay share | 32.7% | NPCI, May 2026 |
| Paytm monthly active users | 77 million | Paytm IR, March 2026 |
| Registered merchants | 49 million | Paytm IR, March 2026 |
| FY26 revenue | ₹8,437 crore | Paytm IR |
| FY26 net profit | ₹552 crore | Paytm IR (turnaround from ₹663 cr loss in FY25) |

### What Happened in 2024

RBI restricted Paytm Payments Bank in early 2024 for compliance failures. In April 2026, the banking license was formally cancelled. Paytm migrated to a multi-bank model (Axis, HDFC, SBI, Yes Bank). Market share dropped from ~15% to ~8%. Core UPI services stayed operational throughout.

This matters for young users because many had their first UPI experience on Paytm. The crisis forced them to reconsider whether to stay or switch.

---

## 2. User Segments (15-25 Focus)

### Who Are We Talking About?

India's 15-25 age group includes roughly:
- 50+ million college students
- 30+ million school students with smartphones (15-18)
- 20+ million early-career professionals (first job, 22-25)
- 15+ million gig/freelance workers
- Growing number of teens receiving digital pocket money from parents

UPI adoption in the 18-24 bracket: approximately 28% of Paytm's user base. The 25-34 bracket is 35%. Together, under-35 users make up 63% of Paytm's user base.

### Segment Breakdown

| Segment | What They Use UPI For | How Often | What Frustrates Them | Why They Might Leave |
|---|---|---|---|---|
| **School students (15-17)** | Pocket money from parents, canteen, online shopping | 5-10 txns/month | Can't set up UPI easily without bank account; parents worry about control | FamPay offers teen-specific cards and controls |
| **College students (18-22)** | Food delivery, splitting rent/meals, recharges, subscriptions | 15-30 txns/month | Cluttered home screen; no easy splitting; small amounts feel risky when balance is low | GPay is cleaner; PhonePe has more offers |
| **First-jobbers (22-25)** | Rent, groceries, subscriptions, investments, peer transfers | 30-50 txns/month | No spending insights; no savings tools; feels like an "uncle's app" | Fi, Jupiter offer better money management |
| **Gig workers (18-25)** | Receiving payments, recharges, small purchases | 20-40 txns/month | Settlement delays; hard to track income vs spending | Need earnings dashboard, not payment app |
| **Teens with digital pocket money** | Online purchases, mobile games, subscription top-ups | 5-15 txns/month | Limited access; no spending controls; parents can't see what was spent | FamPay, Junio designed specifically for this |

### The Core Problem

Paytm treats a 19-year-old college student the same way it treats a 45-year-old shop owner. Same home screen. Same feature priority. Same navigation. The app doesn't know or care who you are.

For young users specifically, this creates three problems:
1. **Too much noise.** Gold, insurance, loans, stock trading: irrelevant to someone splitting a Zomato bill.
2. **No money management.** No savings goals, no spending categories, no "how much did I spend this month" that actually makes sense.
3. **No social layer.** Paying friends is the #1 use case for this age group, but the experience is purely transactional. No personality, no context, no memory.

---

## 3. Key User Journeys

### Journey 1: First-Time Setup (18-year-old college freshman)

| Step | What Happens | Where It Breaks |
|---|---|---|
| Download | 80+ MB app, requests 6 permissions upfront | Feels invasive before you've even opened the app |
| Phone verification | OTP, auto-read | Works fine |
| Bank linking | Select bank, SMS verification, fetch accounts | If SIM isn't linked to bank (common for students with parents' accounts), this fails silently |
| UPI PIN setup | Needs debit card last 6 digits + expiry | Most students don't carry their debit card. Dead end. |
| First home screen | Wall of icons: pay, scan, recharge, gold, loans, insurance, games | "Where do I even start?" |

**Drop-off hypothesis:** 25-35% of first-time young users fail to complete bank linking on the first attempt. The debit card requirement alone blocks a significant portion.

### Journey 2: Splitting a Dinner Bill (4 friends, ₹1,200 total)

| Step | What Happens | Where It Breaks |
|---|---|---|
| Calculate split | Open calculator app. ₹1,200 / 4 = ₹300 each. | Already outside Paytm. |
| Find each friend | Search contacts, find UPI ID or phone number | If friend isn't in contacts by name you recognize, you scroll and guess |
| Send ₹300 to friend 1 | Enter amount, type note, enter PIN | Works, but takes 30+ seconds per person |
| Repeat 2 more times | Same flow, 3 separate transactions | 2 minutes total. Tedious. No record that these were a "group split" |
| Track who paid | Nothing. No shared record. | "Did everyone pay their share?" requires group chat follow-up |

**Reality:** Most young users don't split through UPI. They Venmo-style it: one person pays, others transfer whenever they remember. Money gets lost in the shuffle. Splitwise (separate app) has ~5 million Indian users partly because UPI apps don't solve this.

### Journey 3: Monthly Subscription Management (Spotify + Netflix + Cloud storage)

| Step | What Happens | Where It Breaks |
|---|---|---|
| Subscription renews | Auto-debit via UPI Autopay | Works if set up correctly |
| Check what you're paying for | Open transaction history, scroll through dozens of entries | No filter for "subscriptions only." Mixed in with chai payments. |
| Cancel a subscription | Can't do it from Paytm. Go to each service individually. | Paytm has no subscription management view |
| Budget for subscriptions | Manually add up recurring charges | No auto-detection of recurring payments |

**Key gap:** Young users have 3-7 digital subscriptions averaging ₹200-800/month total. No UPI app gives them a clear "here's what you're paying for every month" view.

### Journey 4: "Am I Broke?" Check (End-of-month anxiety)

| Step | What Happens | Where It Breaks |
|---|---|---|
| Open app | Home screen shows promotions, not your balance | Your financial state isn't the first thing you see |
| Check balance | Tap on bank account to see balance | Balance is accurate but without context ("₹2,400 left" means nothing without knowing what's coming) |
| Review spending | Open transaction history | Chronological list. No categories. Hard to see patterns. |
| Understand where money went | Manually count food, transport, shopping entries | Paytm added AI spend analytics (Nov 2025) but it's buried in settings |

**Note:** Paytm does have AI-powered spend categorization since the November 2025 redesign. But it's not prominent. A 20-year-old won't dig through settings to find it. If it's not on the home screen, it doesn't exist for this demographic.

### Journey 5: Failed Payment Panic (₹500 stuck)

| Step | What Happens | Emotional State |
|---|---|---|
| Payment times out | Screen shows "Transaction pending" | Heart rate goes up |
| Check bank account | ₹500 debited. Merchant says not received. | Panic. "I just lost ₹500." |
| Open Paytm | Transaction shows "Pending" or "Processing" | "What do I do now?" |
| Look for help | Find support section, raise complaint | Relief if clear. Despair if generic. |
| Wait for refund | 3-7 business days | For a student living on ₹5,000/month, ₹500 stuck for a week is 10% of their budget |

**Context:** UPI ecosystem-wide failure rates are down to ~0.7-0.8% (Technical Decline). But at 16+ billion monthly UPI transactions, that's still 100+ million failed transactions per month across India. For a young user with a thin balance, even one failure creates lasting anxiety.

---

## 4. Feature Breakdown

### What Paytm Offers vs. What Young Users Actually Need

| Feature | Exists? | Useful for 15-25? | Problem |
|---|---|---|---|
| Scan & Pay | Yes | Yes, daily | Works well. No complaints. |
| Send money to contacts | Yes | Yes, primary use case | Works but no memory of frequent contacts or context |
| Transaction history | Yes | Somewhat | Cluttered. No easy categorization for this user. |
| AI Spend Analytics | Yes (Nov 2025) | Very useful if found | Buried. Not on home screen. Most young users don't know it exists. |
| Bill splitting | No | Critical gap | Not available. Users switch to Splitwise or group chat math. |
| Savings goals/jars | No | High demand | FamPay and international apps (Revolut, Cash App) offer this. Paytm doesn't. |
| Subscription tracker | No | Needed | No way to see all recurring payments in one place. |
| UPI Lite (PIN-less <₹1,000) | Yes | Yes for small payments | Low awareness. Smart auto-select mode helps but isn't explained. |
| Rewards/Cashback | Yes | Mildly | ₹1-2 scratch cards feel insulting. Not motivating. |
| Gold/Insurance/Loans | Yes | Not relevant | Adds clutter for a 20-year-old. Active noise. |
| Personalised home screen | No | Critical gap | Same interface for a student and a merchant. |
| Parental controls (teen accounts) | No | Needed for 15-17 | FamPay offers this. Paytm doesn't serve this segment. |
| Payment notes/context | Basic | Useful | Notes exist but aren't searchable or organized. |

### The Feature Gap Summary

Paytm has payment infrastructure that works. The problem isn't capability. The problem is that nothing is built around how young users actually think about money:
- They think in terms of "can I afford this" not "transaction ID XYZ789"
- They think in groups, not individuals
- They want to save for things (a trip, a gadget), not just spend
- They want to know where their money went without doing accounting

---

## 5. UX Critique (Youth Perspective)

### Home Screen Problem

Open Paytm. Count the distinct tappable elements on the home screen.

The November 2025 redesign made it cleaner, but a young user still sees: scan, pay, recharge, electricity, DTH, gas, insurance, gold, stocks, loans, credit card, FASTag, movie tickets, travel, and multiple promotional banners.

Google Pay shows: a search bar, recent contacts, a scan button, and a few payment shortcuts. That's it.

For a 20-year-old sending ₹200 to a friend, Paytm's home screen is a shopping mall when they need a corridor.

### Trust Signals That Work

| Signal | Does Paytm Have It? | Does It Work for Young Users? |
|---|---|---|
| Green checkmark on success | Yes | Yes. Universal. |
| Sound confirmation | Yes | More useful for merchants than consumers |
| Transaction ID visible | Yes | Young users don't note these down. They screenshot. |
| Instant SMS from bank | Not Paytm's control | Very important. The bank SMS is the real trust signal. |
| Clear failure explanation | Improved post-2025 | Better than before but still too technical for anxious users |

### What's Missing for Young Users

1. **Balance visibility on home screen.** Young users check their balance before every payment. Make it visible without extra taps.
2. **Spending context.** Not "₹240 to Swiggy" but "Food: ₹2,400 this month (₹600 more than last month)."
3. **Predictive warnings.** "You have 8 days left this month and ₹1,800 remaining. At your current pace, you'll run short by the 27th."
4. **Failure recovery that speaks human.** Not "Transaction declined by beneficiary bank (error code U30)" but "Your bank couldn't process this right now. This usually fixes itself in 10 minutes. Your money hasn't left your account."

---

## 6. Behavioral Insights

### How UPI Apps Shape Young Users' Money Habits

| Principle | How It Shows Up | Why It Matters for 15-25 |
|---|---|---|
| **Habit loop** | Scan QR, enter amount, PIN, done. Repeated daily. | This age group is forming lifelong payment habits right now. The app they use at 20 is the app they'll default to at 30. |
| **Pain of small losses** | ₹500 stuck in a failed payment feels worse than ₹500 well spent | Students on tight budgets feel payment failures 5x more than working adults. ₹500 is 2 days of food. |
| **Social proof** | "Everyone at college uses GPay" or "PhonePe has more cashback" | Peer app choice matters enormously in this age group. It's tribal. |
| **Default bias** | First UPI app you set up stays as default forever | Whoever captures a user at 18 keeps them. Onboarding friction at this stage is existential. |
| **Variable rewards** | Scratch cards with random cashback after payments | ₹1-2 rewards create negative sentiment ("is that all?"). Paytm's reward system actively annoys young users. |
| **Endowment effect** | Transaction history, saved contacts, linked accounts | Switching costs exist but are low. A user with 6 months of history on GPay won't move to Paytm for a ₹10 cashback. |
| **Mental accounting** | Young people think "food budget" not "total outflow" | No UPI app helps users create mental accounts. This is an open opportunity. |

### The Big Behavioral Insight

Young users don't think of UPI as "banking." They think of it as "paying." The difference matters. Banking implies seriousness, complexity, and caution. Paying implies speed, simplicity, and social context.

Paytm's UX feels like banking. GPay's feels like paying. That's why GPay is more popular with young users despite fewer features.

---

## 7. Growth Dynamics

### How Young Users Choose a UPI App

| Acquisition Channel | Strength for Paytm | Reality |
|---|---|---|
| Campus word-of-mouth | Weak | GPay and PhonePe dominate college campuses |
| First app parents install | Medium | Paytm has brand recognition from the wallet era (2015-2018) |
| Merchant QR codes | Strong (49M merchants) | But QR codes work with any UPI app, so this doesn't lock users in |
| Referral rewards | Medium | Standard across all apps |
| Pre-installed on phone | Weak | GPay is pre-installed on most Android phones in India |

### Why Young Users Stay or Leave

| Stay Factor | Leave Factor |
|---|---|
| Already set up, works fine | Friend group uses a different app |
| Familiar from parents' usage | Home screen is too busy |
| Good recharge deals | Failed payment with bad error message |
| Wide merchant acceptance | No useful features beyond basic payments |

### The Network Effect Problem for Youth

UPI is interoperable. A Paytm user can pay a PhonePe QR and vice versa. This means there's no "I need Paytm because my friends use it" effect. The network effect belongs to UPI the protocol, not Paytm the app.

For young users, app choice comes down to: which app feels right? And right now, Paytm doesn't feel like it was made for them.

---

## 8. Monetization

### How Paytm Makes Money (Simplified)

| Revenue Stream | FY26 Number | Relevant to Youth? |
|---|---|---|
| Financial services distribution (loans, insurance, mutual funds) | ₹2,593 crore (+52% YoY) | Not yet. These users are too young for most financial products. |
| Merchant device subscriptions (Soundbox, POS) | ~60% EBITDA margins, 15.1M devices | Not directly relevant to consumer experience |
| Payment processing margins | 4+ bps on GMV | Indirectly relevant. Paytm earns more on non-UPI payments (cards, wallets). |
| Advertising | Growing | Relevant. Young users see ads in the app. |

### The Youth Monetization Problem

UPI payments earn Paytm ₹0 in merchant fees (zero MDR policy). A college student who makes 20 UPI payments a month generates zero direct revenue for Paytm.

Young users become valuable only when they:
- Start earning (22-25): eligible for credit products
- Build financial needs: insurance, investments, savings
- Create data: spending patterns that enable targeted offers

This means Paytm's strategy for young users should be: **acquire cheap now, monetize later.** But if the experience is bad at 20, they won't be around at 25 when the money gets real.

---

## 9. Key Problems (Youth-Focused)

### Problem 1: The App Wasn't Built for You

Paytm's home screen serves merchants, middle-aged bill payers, and investment seekers with equal priority. For a 20-year-old, 60-70% of the home screen is irrelevant. Gold investment, insurance, loan offers, FASTag, gas bill payment: none of these matter to a college student.

**Impact:** Young users feel like they're using their parents' app. Brand perception shifts from "useful" to "dated."

### Problem 2: Splitting Doesn't Exist

The #1 social payment use case for 18-25 year olds is splitting a bill among friends. Paytm has no group split feature. Users calculate manually, send individual payments, and track who paid through WhatsApp messages.

Splitwise has ~5 million users in India specifically because UPI apps haven't solved this.

### Problem 3: No Way to Save for Things

FamPay lets teens create savings "stashes" with goals (new earbuds: ₹2,000, trip fund: ₹5,000). Revolut has Vaults. Cash App has savings.

Paytm has nothing. For a demographic that's learning money management for the first time, the absence of any savings tool is a missed opportunity to build long-term engagement.

### Problem 4: Spending Visibility Is Buried

Paytm added AI spend categorization in November 2025. It auto-categorizes transactions into shopping, food, bills, etc. This is exactly what young users need.

But it's buried in the app. Not on the home screen. Not in the notification. Not in the post-payment flow. A feature that isn't visible doesn't exist for young users.

### Problem 5: Payment Failure Hits Harder

When a ₹500 payment fails for a professional earning ₹80,000/month, it's an inconvenience. When it fails for a student living on ₹5,000-8,000/month, it's a crisis. 10% of their monthly budget is now "stuck."

Paytm's error handling has improved (distinguishes technical vs. user errors, offers bank switching, prevents duplicate charges). But the language is still too formal and the refund timeline (3-7 bank working days) feels like forever to a 20-year-old.

### Problem 6: Rewards Feel Like a Joke

₹1-2 scratch card cashback on a ₹500 payment. Young users have reported this creates negative sentiment on app store reviews. It would be better to give nothing than to give ₹1 with a celebratory animation.

### Problem 7: No Identity

GPay is "the clean one." PhonePe is "the one with offers." CRED is "the cool one." Paytm is "the one my parents use."

For the 15-25 demographic, app identity matters. Paytm has no youth-facing brand positioning, no young ambassador, no design language that signals "this is for you."

---

## 10. Improvement Ideas

| # | Problem | Solution | Impact | Effort |
|---|---|---|---|---|
| 1 | Home screen clutter | Age and usage-based home screen. Show scan, pay, split, spending summary to young users. Hide insurance, loans, gold unless they search for it. | Reduces cognitive load. Makes the app feel personal. | Medium |
| 2 | No bill splitting | Built-in split: enter total, select friends, auto-calculate, send requests, track settlements. Group history persists. | Captures the #1 unmet social payment need. Drives P2P volume. | Medium |
| 3 | No savings goals | "Stash" feature: set a goal (₹5,000 for new earbuds), auto-transfer small amounts weekly from linked account. Visual progress bar. | Builds financial habits early. Creates engagement beyond payments. | Medium |
| 4 | Spending data is hidden | Post-payment nudge: "You've spent ₹1,200 on food this week. That's ₹400 more than usual." Monthly summary on home screen. | Turns data Paytm already has into visible value. | Low |
| 5 | Failed payment anxiety | Plain-language error messages. Live refund tracker. Estimated refund date in hours, not "business days." | Directly reduces churn from failed transactions in the most price-sensitive segment. | Low-Medium |
| 6 | Useless rewards | Replace ₹1 scratch cards with progress-based rewards: "5th payment this week: ₹10 off your next recharge." Predictable, not random. | Feels fair instead of insulting. Drives frequency. | Low |
| 7 | No subscription view | Auto-detect recurring UPI Autopay mandates. Show in one screen: "Netflix ₹199, Spotify ₹119, iCloud ₹75. Total: ₹393/month." | Gives young users control over subscriptions they forget about. | Low |
| 8 | Teen users excluded | Partner with banks for minor-friendly UPI accounts. Parental approval flow. Spending limits. Parent dashboard. | Captures users at 15 instead of 18. FamPay proves demand exists (10M+ downloads). | High |
| 9 | No payment personality | Custom payment messages, reactions to received payments, payment streaks with friends ("you've paid Arjun 12 times this month"). | Makes payments social, not just transactional. Aligns with how young people communicate. | Low-Medium |
| 10 | "Uncle's app" brand perception | Youth-specific visual theme option. Campus ambassador program. Student verification for exclusive deals. | Brand perception change is slow but compounds. | Medium |

---

## The One Idea: Paytm Sorted

### Root Cause Analysis

Why is Paytm losing the 15-25 demographic to Google Pay and PhonePe?

```
[Core Problem]
Low engagement and market share (7.9%) among users aged 15-25.
      │
      ▼
[Symptom]
Young users prefer minimalist interfaces (Google Pay) or transactional utility.
      │
      ▼
[First-Level Cause]
Paytm's home screen is cluttered with services irrelevant to this group, such as gold investments, business insurance, and home loans.
      │
      ▼
[Second-Level Cause]
Paytm needs to show these products to generate revenue. The company cannot simply remove them without hurting financial product distribution (which brought in ₹2,593 crore in FY26).
      │
      ▼
[Root Cause]
Paytm has a single, rigid user experience for both a 45-year-old shop owner and a 19-year-old student. The app lacks the flexibility to personalize the interface based on age and behavior while retaining core monetization channels.
```

The solution is not to launch a separate app or strip away ads. The solution is **Paytm Sorted**: an in-app experience layer that filters and restructures the interface for young users.

---

### Product Skills Applied in This Design

Building Paytm Sorted required combining several core product management disciplines:

*   **Conversion Funnel Optimization:** Reduced the steps required to split a bill from 7 manual interactions (calculating, searching contacts, sending individual requests) to 2 taps.
*   **Behavioral Design:** Used gamification (Split Score) to solve the social friction of debt collection, replacing awkward personal reminders with automated system notifications.
*   **System Design & Data Modeling:** Structured the relational database schema and API flow to show that the feature is technically feasible within standard UPI architecture.
*   **Monetization Alignment:** Maintained Paytm's advertising and credit distribution pipelines by altering the targeting logic rather than removing the slots.

---

### Core Feature Specifications

#### 1. Custom Handles for Privacy
Sharing phone numbers to collect payments exposes contact details in public groups. Users can create a custom handle:
*   Format: `@username.sorted` (e.g., `@karan.sorted`).
*   Acts as an alias linked to the user's primary UPI ID.
*   Allows users to join group splits, send requests, and pay friends without sharing mobile numbers.

#### 2. Split Score (Reputation Meter)
To solve the issue of friends delaying repayments, Paytm Sorted introduces a **Split Score**:
*   Initial State: The user starts with a score of **72** with the note **"3 late repays this month"** and a compact history sparkline.
*   Score Bounds: Bounded between 0 and 100.
*   Deterministic Rules:
    *   On-time repayment: `+1`
    *   Group settlement completed: `+1`
    *   Late repayment (past due date): `-2`
    *   Unresolved dispute after T+7 days: `-3`
*   System feedback: Changing score triggers an in-app toast, an activity record, and a notification update.
*   Peer pressure utility: Users with a score of 95+ receive merchant vouchers. Users below 70 are highlighted in red on group split screens, alerting others that they are slow to pay back.

#### 3. Automatic Reminder Timeline
A dedicated landing strip and request view explain the automated reminder cadence:
*   **T+0:** Request sent via UPI Request Pay API.
*   **T+2 days:** Gentle UPI push notification nudge.
*   **T+5 days:** WhatsApp reminder alert.
*   **T+7 days:** Final escalation with Split Score impact warning.

*Note: These are prototype simulations only and do not trigger real WhatsApp messages or affect actual bank credit scores.*

---

### Mini-App Navigation & Architecture

The prototype is built as a state-machine-driven app mounted inside the phone frame, using the following screen states:

```
[Onboarding] ──> [Home] ──> [Groups] ──> [Group Detail] ──> [Split Summary]
                   │           │               │
                   ▼           ▼               ▼
              [Notifications] [Requests]     [Scan Bill]
                   │           │               │
                   ▼           ▼               ▼
               [Profile]  [Split Score]  [Group History]
```

Navigation is managed via state transitions instead of traditional URL routes. The persistent bottom tab bar includes:
*   **Home:** Quick actions, balance card, Split Score summary, recent activity list, and a carousel of targeted ads (vouchers, concert tickets, tech deals).
*   **Groups:** View active groups (e.g., Hostel Block C, Trip to Goa). Supports group search and group creation templates (Hostel, Society, Trip, Roommates).
*   **Scan:** Simulated camera capture followed by receipt editing. Users can edit item names, adjust prices, and assign specific items to specific members using a checkbox grid. Taxes are automatically allocated proportionally.
*   **Requests:** Lists incoming and outgoing requests with filters (Pending, Overdue, Paid, Disputed). Outgoing requests show the scheduled reminder timeline.
*   **Profile:** Manage the `@handle`, edit notification preferences, toggle dark/light theme, and access the Split Score Detail screen.

---

### Technical Architecture of Paytm Sorted Split

The splitting engine handles unequal splits, group storage, and real-time NPCI payment requests.

```
[Paytm Sorted UI] ──> [Split Engine] ──> [NPCI UPI Request Pay API]
                           │
                           ▼
                 [Sorted PostgreSQL DB]
                 (Users, Groups, Balances)
```

#### Database Schema

Paytm Sorted uses five core tables to manage splits:

```sql
-- Users Table
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    handle VARCHAR(30) UNIQUE NOT NULL, -- e.g., @karan.sorted
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    split_score INT DEFAULT 72 CHECK (split_score BETWEEN 0 AND 100),
    avg_settlement_time_seconds INT DEFAULT 0
);

-- Groups Table
CREATE TABLE groups (
    group_id VARCHAR(50) PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Group Members Table
CREATE TABLE group_members (
    group_id VARCHAR(50) REFERENCES groups(group_id),
    user_id VARCHAR(50) REFERENCES users(user_id),
    PRIMARY KEY (group_id, user_id)
);

-- Transactions Table
CREATE TABLE transactions (
    txn_id VARCHAR(50) PRIMARY KEY,
    group_id VARCHAR(50) REFERENCES groups(group_id),
    payer_id VARCHAR(50) REFERENCES users(user_id),
    total_amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Splits Table (Individual breakdown)
CREATE TABLE splits (
    split_id VARCHAR(50) PRIMARY KEY,
    txn_id VARCHAR(50) REFERENCES transactions(txn_id),
    debtor_id VARCHAR(50) REFERENCES users(user_id),
    split_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PAID', 'EXPIRED')),
    settled_at TIMESTAMP
);
```

#### Unequal Split Calculation Logic

The Split Engine handles three types of splits: equal, percentage-based, and itemized.

**Equal Split Calculation:**
$$Split\ Amount = \frac{Total\ Amount}{Number\ of\ Members}$$

**Percentage-Based Split:**
$$Individual\ Debt = Total\ Amount \times Percentage$$
*(System validates that the sum of all individual percentages equals exactly 100% before executing)*

**Itemized Split (Item-level allocation):**
$$\text{For each item } i, \text{ Cost per sharing member } = \frac{Price_i}{Count_{consumers}}$$
$$\text{User Debt} = \sum (\text{Cost per sharing member for each item consumed})$$

*Example itemized calculation:*
*   Bill total: ₹1,000 (Item 1: Pizza ₹800 eaten by Karan and Sneha; Item 2: Coke ₹200 drunk only by Sneha)
*   Karan's share: $\frac{800}{2} = ₹400$
*   Sneha's share: $\frac{800}{2} + 200 = ₹600$

#### NPCI UPI Request Pay API Integration Flow

Instead of generating text reminders, Paytm Sorted uses NPCI's native **UPI Request Pay API** (collect transactions) to trigger push alerts on the debtor's phone:

1.  **Initiation:** The Split Engine calls Paytm's PSP server with the collect payload.
2.  **NPCI Request:** The PSP server hits NPCI's API endpoint `/v2/requestPay`.
3.  **Payload Structure:**
    *   `payerVpa`: Debtor's handle (e.g., `sneha@ptaxis`)
    *   `payeeVpa`: Payer's handle (e.g., `karan@ptaxis`)
    *   `amount`: Calculated split share (e.g., `300.00`)
    *   `note`: Split reference (e.g., "Sorted: Dinner Split at Le Meridien")
    *   `expiry`: Set to 72 hours.
4.  **Delivery:** The debtor receives a native OS push notification from their default UPI app.
5.  **Settlement:** Tapping the notification opens the PIN screen. Entering the PIN transfers the money directly to the payer's account.
6.  **Callback & Update:** Once settled, NPCI sends a callback. Paytm's server updates the `splits` table status to `PAID` and triggers a real-time WebSocket update to the group UI.

---

### Realistic Money Impact

UPI peer-to-peer transactions have zero merchant discount rate (zero MDR) and yield zero direct revenue. However, Paytm Sorted drives indirect monetization through three channels:

#### 1. Expanded Payment Margins via Postpaid Conversion
By integrating **Paytm Postpaid** (unsecured BNPL credit line) directly into the Split Summary screen, young users are prompted to settle splits using credit when their bank balance is low. 
*   Payment processing margins on standard UPI: ~0 bps.
*   Payment processing margins on Postpaid/Credit lines: **15–18 bps**.
*   Financial impact: Converting 5% of monthly split volumes to Paytm Postpaid drives direct transaction fee revenue.

#### 2. Advertising Revenue Retention
Instead of hiding ads to clean up the UI, Paytm Sorted filters ads to display high-intent consumer deals (e.g., food coupons, tech drops, gig tickets).
*   Standard ad click-through rate (CTR) on cluttered pages: ~0.4%.
*   Targeted Gen Z ad CTR in Sorted mode: **1.5% – 2.0%**.
*   Financial impact: Maintains ad inventory yield without increasing user churn.

#### 3. Sourcing Commissions on Micro-Lending
The cash flow trends collected from Split Score histories and Spending Pulse analytics enable precise risk profiling. Paytm can cross-sell education loans and personal credit lines from partner NBFCs (e.g., Credit Saison, KreditBee) at the exact moment a user experiences a cash flow gap.
*   Lending sourcing commissions: **1.5% - 2.5%** of loan volume.
*   Financial impact: Increases high-margin distribution revenue (which grew to ₹2,593 crore in FY26).

---

### Execution Plan and Timeline

| Phase | Timeline | Deliverables | Target Audience |
|---|---|---|---|
| **Phase 1** | Month 0-2 | Custom handle database schema, backend registration API, handle availability checker. | Internal developers, closed beta (10k users) |
| **Phase 2** | Month 2-4 | Equal/unequal Split Engine calculations, database migration, local storage for groups, and group creation UI. | 10 selected college campuses (100k users) |
| **Phase 3** | Month 4-6 | NPCI Request Pay integration, Split Score calculation engine, real-time push notification rules. | Open public beta (under-25 age group) |
| **Phase 4** | Month 6-8 | Native ad/credit module targeting engine, final dashboard polishing. | Full release to all under-25 users |

### Quantitative Metrics to Validate Success

Paytm's product team must monitor these metrics post-launch to evaluate viability:

1.  **Group Split Adoption Rate:**
    $$\frac{\text{Monthly Active Users executing a Group Split}}{\text{Total Monthly Active Users in 15-25 bracket}}$$
    *Target: 15% adoption within 6 months of Phase 4 release.*
2.  **Average Time to Settle (T2S):**
    *Target: Average settlement time drops below 4 hours (current informal industry baseline is 28 hours).*
3.  **Viral K-Factor:**
    $$K = i \times c$$
    *(where $i$ is number of split requests sent per user, and $c$ is the conversion rate of non-Paytm users downloading the app to pay)*
    *Target: K > 1.2 (drives organic growth without paid user acquisition).*
4.  **Ad CTR and Credit Conversion:**
    *Target: Maintain or improve home screen ad revenue and loan sourcing volumes by verifying that targeted Gen Z ads convert at a 1.5x higher rate than generic banners.*

---

## 11. What I Learned


### On the UPI Ecosystem

UPI is designed to be interoperable, which means no single app can own the payment experience. The protocol benefits everyone equally. This forces apps to compete on everything except the payment itself: design, features, trust, and identity.

For young users, this means switching apps costs nothing technically. The only switching cost is habit and history. If Paytm can't create habit and history worth staying for, young users will default to whatever their friends use.

### What Surprised Me

1. **Zero MDR makes young users a cost center.** Every UPI payment a college student makes costs Paytm money to process but generates no revenue. The only way to justify serving this segment is lifetime value, and that requires them to still be using Paytm in 5 years.

2. **FamPay proved the model.** A startup with a fraction of Paytm's resources built a teen-focused payment product with 10M+ downloads. The demand exists. Paytm just hasn't addressed it.

3. **Splitting is still unsolved.** In 2026, after 8 years of UPI, there is still no native splitting feature in any major UPI app. Splitwise exists as a separate app because this gap persists. This is low-hanging fruit.

4. **The app you use at 20 is the app you use at 30.** Default bias is the strongest behavioral force in payments. Whoever captures a user during college years has them for a decade. Paytm is losing this window.

### Tradeoffs I Noticed

| Tradeoff | Why It's Hard |
|---|---|
| Youth focus vs. revenue pressure | Young users don't generate revenue today. Boards want quarterly results. |
| Clean UI vs. cross-selling surface | Every feature removed from the home screen is a lost monetization opportunity. |
| Personalization vs. engineering cost | Building mode-based experiences is more complex than one-size-fits-all. |
| Savings features vs. regulatory scope | Any savings product needs careful regulatory positioning (is it a deposit? a wallet?). |
| Splitting vs. individual payments | Group features are harder to build and test than 1-to-1 flows. |

### What I'd Explore Next

1. **User interviews with 18-22 year olds:** What app do they open first when splitting a bill? Why? What would make them switch?
2. **FamPay competitive analysis:** How does a startup with limited resources build better youth UX than Paytm with 77 million users?
3. **International case studies:** How did Cash App capture American youth? What did Revolut do for European under-25s? Are those patterns transferable to India?
4. **Paytm's data advantage:** Does Paytm's existing spend categorization data give it a head start on Spending Pulse vs. building from scratch?

---

## Data Appendix

### Paytm Financial Summary (FY 2026)

| Metric | FY 2026 | FY 2025 | Change |
|---|---|---|---|
| Revenue | ₹8,437 crore | ~₹6,900 crore | +22% |
| Net Profit | ₹552 crore | -₹663 crore | Turnaround |
| EBITDA | ₹502 crore | -₹1,506 crore | +₹2,008 crore |
| Financial Services Revenue | ₹2,593 crore | ~₹1,706 crore | +52% |

### UPI Market Share (May 2026)

| App | Share |
|---|---|
| PhonePe | 46.2% |
| Google Pay | 32.7% |
| Paytm | 7.9% |
| Navi | 3.6% |
| super.money | 1.8% |
| Others | ~8.8% |

### Operating Metrics (March 2026)

| Metric | Value |
|---|---|
| Monthly Transacting Users | 77 million |
| Registered Merchants | 49 million |
| Subscription Devices | 15.1 million |
| Total Transactions (FY26) | 1,822 crore |
| Merchant GMV (FY26) | ₹6.5 lakh crore |

### India Youth Demographics

| Metric | Estimate |
|---|---|
| Population aged 15-25 | ~350 million |
| Population under 35 | ~67% of total |
| Smartphone penetration (18-25) | ~85% in urban, ~55% in semi-urban |
| UPI users under 25 (estimated) | ~28% of total UPI user base |

### Key Timeline

| Date | Event |
|---|---|
| 2022 | RBI bans PPBL from onboarding new customers |
| Jan 2024 | RBI restricts PPBL from accepting new deposits |
| 2024 | Paytm migrates to multi-bank TPAP model |
| Nov 2025 | Major app redesign with AI spend analytics |
| Apr 2026 | RBI cancels PPBL banking license |
| Jul 2026 | Paytm secures Luxembourg payment license |

*Sources: NPCI, Paytm Investor Relations, Economic Times, LiveMint, Business Standard, NDTV Profit, Entrackr*

---

> [!NOTE]
> This teardown is built on public data and hypothesis-driven analysis. No internal metrics are claimed. Where numbers are estimated, they are marked as assumptions.

*Portfolio project. Feedback welcome.*
