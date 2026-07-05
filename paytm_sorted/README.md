# Paytm Sorted: Gen Z UPI Social Splitting & Debt Recovery

A product teardown, strategy deck, and interactive prototype demonstrating how Paytm can capture the under-25 demographic through a native, social bill-splitting layer without compromising its core advertising and credit monetization channels.

## 🔗 Project Links

*   **Lovable Prototype:** [https://sorted-paytm.lovable.app](https://sorted-paytm.lovable.app)
*   **Detailed Case Study:** [case_study.md](case_study.md)
*   **Local HTML Prototype:** [index.html](index.html)

---

## 🛠️ Tech Stack & Tools

*   **Frontend Framework:** React, TypeScript, Tailwind CSS (Lovable.dev)
*   **Prototype Engine:** HTML5, Tailwind CSS CDN, Vanilla Javascript (ES6)
*   **Database Design:** PostgreSQL (Relational schema modeling for transactions and splits)
*   **Protocols & APIs:** NPCI UPI Request Pay API specification, WebSockets for status synchronization

---

## 💡 Product Management Skills Demonstrated

*   **Root Cause Analysis (RCA):** Diagnosed Paytm's low Gen Z UPI volume share (7.9%) by identifying the conflict between rigid multi-product layouts and the student segment's need for simple social payments.
*   **Conversion Funnel Optimization:** Designed a workflow that cuts the steps required to split a bill from 7 manual interactions down to 2 taps.
*   **Behavioral Design & Gamification:** Conceived and implemented the "Split Score" system, utilizing social accountability and peer reputation to drive repayments.
*   **Technical System Design:** Modeled SQL database relations and mapped client-server communications with NPCI's API collect flow.
*   **Monetization Alignment:** Balanced UX simplification with corporate unit economics by retaining ad slots and credit distribution channels, modifying only the targeting logic for the youth segment.

---

## 📋 Root Cause Analysis Summary

Paytm's decline in youth market share is not solved by simply cleaning up the user interface. Paytm relies on unsecured lending and ad revenue (generating ₹2,593 crore in financial services revenue in FY26). The root cause is a lack of dynamic personalization: the app serves the same home screen layout to a 19-year-old student as it does to a 45-year-old merchant. 

**Paytm Sorted** resolves this by acting as a contextual experience layer. It preserves ad banners and credit offers but dynamically filters them (e.g., student credit, concert deals) while making peer-to-peer social payments the primary interaction path.

---

## 🚀 Key Feature Walkthrough

### 1. Onboarding
A lightweight first-run onboarding sequence introduces the key value propositions of automated reminders and Split Score mechanics, dropping the user directly into the Home screen upon completion.

### 2. Home Screen & Monetization Retention
The dashboard features an uncluttered view with a visible balance bar and Split Score card. Crucially, Paytm's core revenue banners remain active, targeted to Gen Z preferences (e.g., Paytm Postpaid advances, Spotify subscriptions, and tech drops).

### 3. Custom Handles
Users can set up `@username.sorted` handles to split expenses and request money without sharing mobile numbers, securing privacy in group situations.

### 4. Split Score
Reputation gamification metrics to resolve payment delays:
*   **Initial state:** Starts at 72 (reflecting "3 late repays this month") with a sparkline history.
*   **Increment:** +1 point for on-time payments or completing group settlements.
*   **Decrement:** -2 points for late payments; -3 points for unresolved disputes past 7 days.
*   **Reputation utility:** High scores unlock merchant discount vouchers. Low scores (under 70) highlight the user in red inside group split views, prompting peer-driven collections.

### 5. Automated Reminders Timeline
Paytm manages collections automatically using a scheduled timeline to reduce social friction:
*   **T+0:** Split request sent.
*   **T+2 days:** Gentle UPI push notification nudge.
*   **T+5 days:** WhatsApp reminder.
*   **T+7 days:** Final warning showing the impending drop in Split Score.

### 6. Technical Split Engine & Math
Supports equal, percentage, and itemized unequal splitting:
*   **Equal Splits:** Divides bill equally among selected contacts.
*   **Manual/Percentage Splits:** Input-driven allocation validated to sum to exactly 100%.
*   **Itemized Splits:** Checkbox grid layout allowing item-level assignment. Taxes and fees are distributed proportionally across selected items.

### 7. NPCI UPI Request Pay API Integration
Converts reminders into actionable payment requests. Tapping a reminder notification opens the debtor's default UPI PIN screen, allowing one-tap settlement.

---

## 💻 Running the Local Prototype

To run the interactive prototype locally:
1. Open the [paytm_sorted](.) directory.
2. Double-click [index.html](index.html) to open it in any web browser.
3. Use the interface to create splits, adjust handle names, simulate payments, and watch the live database schema update dynamically.
