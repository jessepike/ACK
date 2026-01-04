# IPE Interface Mockup - Complete Layout

---

**Version:** 1.0  
**Created:** 2024-12-31  
**View:** Discovery Stage - Active on concept.md

---

## Full Interface Layout

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ IPE-demo                                                                          jess@pike  ⚙️  ✕   │ ← Window Chrome
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  [1. Discovery ✓ 4/4]  [2. Solution Design 2/4]  [3. Environment Setup 0/4]  [4. Workflow...]     │ ← Stage Navigation
│       ← Active             ← In Progress             ← Not Started                                 │
│                                                                                                     │
├──────────────┬──────────────────────────────────────────────────────────┬──────────────────────────┤
│              │                                                          │                          │
│  Discovery   │  concept.md                            [WYSIWYG ▼]       │  💬 Agent Chat           │
│              │                                                          │                          │
│  ✓ concept   │ ┌──────────────────────────────────────────────────┐    │ ┌──────────────────────┐ │
│  ✓ research  │ │ Status: [Finalized ▼]  Created: 2024-12-31 [...]│    │ │ @Claude              │ │
│  ✓ validat   │ └──────────────────────────────────────────────────┘    │ │ Research shows 60%   │ │
│  ✓ scope     │                                                          │ │ value cost reduction │ │
│              │ [↶] [↷] | [B] [I] [H] [•] [Link] [Code] | [/]           │ │ 2 min ago            │ │
│  ✓ synthesis │ ────────────────────────────────────────────────────     │ ├──────────────────────┤ │
│              │                                                          │ │ @Human               │ │
│ 📎 Resources │ ▾ What Is It?                              ☑ Done       │ │ Can you validate the │ │
│  🔗 comp...  │   IPE (Integrated Planning Environment) is a            │ │ market size claim?   │ │
│  🔗 market   │   planning layer that orchestrates AI-augmented          │ │ Just now             │ │
│              │   development from concept to implementation-ready       │ ├──────────────────────┤ │
│              │   state. It bridges the gap between... [💬2]            │ │                      │ │
│              │                                                          │ │ [Agent Mode: Fast ▼] │ │
│              │ ▾ Problem Being Solved                     ☑ Done       │ │                      │ │
│              │   AI-augmented solo developers lack a unified           │ │ @mention or /command │ │
│              │   environment for pre-implementation planning. The       │ │                      │ │
│              │   IDE handles code execution, but critical upstream      │ │ [          Send  →]  │ │
│              │   work—research, architecture decisions, context         │ └──────────────────────┘ │
│              │   management—happens in scattered CLIs and docs.        │                          │
│              │                                                          │  Active: 3 users        │
│              │ ▸ Core Features                            ☐ Done       │  • jess (you)           │
│              │   Living documentation, agent orchestration...           │  • @Claude              │
│              │                                                          │  • @ResearchAgent       │
│              │ ▸ Value Proposition                        ☐ Done       │                          │
│              │                                                          │                          │
│              │ ▸ Target User                              ☐ Done       │                          │
│              │                                                          │                          │
│              │ ▸ Success Looks Like                       ☐ Done       │                          │
│              │                                                          │                          │
│              │ ▸ Out of Scope                             ☐ Done       │                          │
│              │                                                          │                          │
│              │                                                          │                          │
│              │                                                          │                          │
├──────────────┴──────────────────────────────────────────────────────────┴──────────────────────────┤
│ ● Saved 3s ago          Editing concept.md - Section: What Is It?              🔔 2   ⚙️   🔄      │ ← Footer
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

Window Dimensions: 1920 x 1080
Left Panel: 280px
Center Content: ~900px (flexible)
Right Panel: 380px
Top Bar: 80px
Footer: 28px
```

---

## Component Breakdown

### Top Bar (Stage Navigation)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ IPE-demo                                                                          jess@pike  ⚙️  ✕   │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  [1. Discovery ✓ 4/4]  [2. Solution Design 2/4]  [3. Environment Setup 0/4]  [4. Workflow Config]  │
│    ↑                      ↑                          ↑                            ↑                │
│    Blue bg               Gray bg                    Gray bg                      Gray bg           │
│    White text            Orange count               Red count                    Red count         │
│    Active                In Progress                Not Started                  Not Started       │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘

Height: 80px
Padding: 16px horizontal, 12px vertical
Font: 14px stage names, 12px counts
```

### Left Panel (File Browser)

```
┌─────────────────┐
│  Discovery      │ ← Stage name (gray text, 12px)
│                 │
│  ✓ concept.md   │ ← Green checkmark, selected (blue highlight)
│  ✓ research.md  │ ← Gray background on hover
│  ✓ validation   │
│  ✓ scope.md     │
│                 │
│  ✓ synthesis    │ ← Synthesis doc (indented or separated)
│                 │
│ 📎 Resources    │ ← Collapsible section
│  🔗 comp-ana... │ ← Truncated filenames
│  🔗 market-rep  │
│                 │
│                 │
│  ⋮              │ ← Scroll indicator if needed
└─────────────────┘

Width: 280px
Item height: 32px
Padding: 8px
Font: 13px
Icons: 16px
```

### Center Content (Editor)

```
┌────────────────────────────────────────────────────────────────┐
│ concept.md                                    [WYSIWYG ▼]      │ ← Document header
├────────────────────────────────────────────────────────────────┤
│ Status: [Finalized ▼]  Created: 2024-12-31 [Human]            │ ← Metadata form
│                         Updated: 2024-12-31 [Claude]           │
│ Related: [research.md ×] [+ Add]                               │
├────────────────────────────────────────────────────────────────┤
│ [↶] [↷] | [B] [I] [H] [•] [Link] [Code] | [/]                │ ← Toolbar
├────────────────────────────────────────────────────────────────┤
│                                                                │
│ ▾ What Is It?                                      ☑ Done     │ ← Section
│   IPE (Integrated Planning Environment) is a planning         │
│   layer that orchestrates AI-augmented development from       │
│   concept to implementation-ready state. It bridges the       │
│   gap between... [💬2]                                        │ ← Comment indicator
│                                                                │
│ ▾ Problem Being Solved                             ☑ Done     │
│   AI-augmented solo developers lack a unified environment     │
│   for pre-implementation planning. The IDE handles code       │
│   execution, but critical upstream work—research,             │
│   architecture decisions, context management—happens in       │
│   scattered CLIs and docs.                                    │
│                                                                │
│ ▸ Core Features                                    ☐ Done     │ ← Collapsed
│   Living documentation, agent orchestration...                │ ← Preview text (gray)
│                                                                │
│ ▸ Value Proposition                                ☐ Done     │
│                                                                │
│ [... more sections ...]                                       │
│                                                                │
└────────────────────────────────────────────────────────────────┘

Width: ~900px (flexible, max 1200px)
Padding: 24px
Line height: 1.6
Font: 15px body, 20px headers
```

### Right Panel (Agent Chat)

```
┌─────────────────────────┐
│ 💬 Agent Chat           │ ← Panel header
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ @Claude             │ │ ← Agent message (left-aligned)
│ │ Research shows 60%  │ │ ← Gray background bubble
│ │ value cost reduction│ │
│ │ 2 min ago           │ │ ← Timestamp (small, gray)
│ └─────────────────────┘ │
│                         │
│   ┌───────────────────┐ │ ← Human message (right-aligned)
│   │ @Human            │ │ ← Blue background bubble
│   │ Can you validate  │ │
│   │ the market claim? │ │
│   │ Just now          │ │
│   └───────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ @ResearchAgent      │ │ ← Different agent
│ │ Looking into that...│ │
│ │ typing...           │ │ ← Typing indicator
│ └─────────────────────┘ │
│                         │
│                         │
│ [Agent Mode: Fast ▼]    │ ← Mode selector
│                         │
│ ┌─────────────────────┐ │ ← Input area
│ │ @mention or /command│ │ ← Placeholder text
│ │                     │ │
│ │                     │ │
│ │          [Send  →]  │ │ ← Send button
│ └─────────────────────┘ │
│                         │
│ Active: 3 users         │ ← Presence indicator
│ • jess (you)            │
│ • @Claude               │
│ • @ResearchAgent        │
└─────────────────────────┘

Width: 380px
Message padding: 12px
Font: 14px
Avatar/badge: 24px
```

### Footer (Status Bar)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ ● Saved 3s ago          Editing concept.md - Section: What Is It?      🔔 2  ⚙️  🔄 │
│ ↑                       ↑                                               ↑    ↑   ↑  │
│ Status                  Current activity                                Notif Set Sync
│ (green dot)             (gray text)                                                  │
└─────────────────────────────────────────────────────────────────────────────────────┘

Height: 28px
Font: 12px
Icon size: 16px
Padding: 6px horizontal
```

---

## Color Specifications

### Dark Theme Palette

**Backgrounds:**
- `#1a1a1a` - Main window background
- `#1e1e1e` - Panel backgrounds
- `#252526` - Elevated panels (left/right)
- `#2d2d2d` - Hover states
- `#333333` - Input fields

**Borders:**
- `#3e3e42` - Panel dividers
- `#505050` - Input borders
- `#007acc` - Active/focus borders

**Text:**
- `#e0e0e0` - Primary text
- `#a0a0a0` - Secondary text
- `#606060` - Placeholder text
- `#808080` - Muted text

**Accents:**
- `#007acc` - Primary blue (active, links)
- `#4caf50` - Success green (complete)
- `#ff9800` - Warning orange (in progress)
- `#f44336` - Error red (not started)

**Chat Bubbles:**
- `#2d2d2d` - Agent messages
- `#005a9e` - Human messages (darker blue)
- `#3d3d3d` - Hover state

**Syntax (in code blocks):**
- `#569cd6` - Keywords
- `#ce9178` - Strings
- `#6a9955` - Comments
- `#dcdcaa` - Functions

---

## Interaction States

### Stage Tab States

**Default (Not Active):**
```
Background: #1e1e1e
Text: #a0a0a0
Border: none
```

**Hover:**
```
Background: #2d2d2d
Text: #e0e0e0
Cursor: pointer
Scale: 1.02
```

**Active:**
```
Background: #007acc (blue)
Text: #ffffff
Border-bottom: 2px solid #0098ff
Font-weight: 600
```

**Completed:**
```
Background: #2d2d2d
Text: #e0e0e0
Checkmark: #4caf50
Count: #4caf50
```

### File Browser Item States

**Default:**
```
Background: transparent
Text: #e0e0e0
```

**Hover:**
```
Background: #2d2d2d
Cursor: pointer
```

**Selected:**
```
Background: #094771 (dark blue)
Text: #ffffff
Border-left: 3px solid #007acc
```

**Completed (checkmark):**
```
Checkmark color: #4caf50
```

### Editor Section States

**Collapsed:**
```
▸ Section Name            ☐ Done
  Preview text (2-3 lines, #808080)
```

**Expanded:**
```
▾ Section Name            ☐ Done
  [Full editable content]
```

**Complete:**
```
▾ Section Name            ☑ Done
  [Content, green tint on header]
```

---

## Responsive Breakpoints

### Desktop (1920px+)
- All panels visible
- Full stage names
- Complete artifact names
- Max content width: 1200px

### Laptop (1440px)
- Panels slightly narrower
- Stage names abbreviated
- Artifact names may truncate

### Tablet (1024px)
- Right panel collapsible
- Stage dropdown instead of tabs
- Left panel overlay on mobile

### Mobile (768px - Future)
- Single column layout
- Bottom navigation
- Swipe between panels
- Stage selector at top

---

## Annotations & Dimensions

```
┌─────────────────────────────────────────────────────────────────┐
│                         1920px                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                        80px                                 │ │ Top Bar
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────┬────────────────────────────────────────┬─────────────┐ │
│  │    │                                        │             │ │
│  │280 │              ~900px                    │    380px    │ │ Main Content
│  │px  │           (flexible)                   │             │ │ 944px height
│  │    │                                        │             │ │
│  │    │                                        │             │ │
│  └────┴────────────────────────────────────────┴─────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                        28px                                 │ │ Footer
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
    Total height: 1080px (80 + 944 + 28 + padding)
```

---

## Typography Scale

**Headers:**
- H1: 24px / 600 weight / 1.3 line-height
- H2: 20px / 600 weight / 1.4 line-height
- H3: 18px / 600 weight / 1.4 line-height

**Body:**
- Primary: 15px / 400 weight / 1.6 line-height
- Secondary: 14px / 400 weight / 1.5 line-height
- Small: 13px / 400 weight / 1.4 line-height
- Tiny: 12px / 400 weight / 1.3 line-height

**Code:**
- Inline: 13px / 400 weight / monospace
- Block: 13px / 400 weight / 1.5 line-height / monospace

**UI Elements:**
- Buttons: 14px / 500 weight
- Labels: 12px / 500 weight / uppercase / 0.5px letter-spacing
- Placeholders: 14px / 400 weight / italic

---

## Spacing System

**Base unit:** 4px

**Scale:**
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- 2xl: 48px

**Component Spacing:**
- Panel padding: 16px (md)
- Section spacing: 24px (lg)
- Element margin: 8px (sm)
- Inline spacing: 4px (xs)

---

## Icon Library

**Suggested:** Lucide Icons or Heroicons

**Icons Used:**
- ✓ Checkmark (completion)
- ▸ ▾ Arrows (expand/collapse)
- 💬 Comment bubble
- 🔗 Link
- 📎 Attachment
- ⚙️ Settings
- 🔔 Notifications
- 🔄 Sync
- ↶ ↷ Undo/Redo
- → Send
- ✕ Close

**Size:** 16px default, 24px for prominent actions

---

## Animation & Transitions

**Duration:**
- Fast: 150ms (hover states)
- Normal: 250ms (panel transitions)
- Slow: 400ms (page transitions)

**Easing:**
- Ease-out: UI element appearances
- Ease-in-out: State changes
- Spring: Smooth, natural motion (optional)

**Animations:**
- Stage switch: Fade content (250ms)
- Dropdown open: Slide down (150ms)
- Section expand: Height animation (200ms)
- Hover: Background color (150ms)
- Save indicator: Pulse (1s cycle)

---

## Accessibility Features

**Keyboard Navigation:**
- Tab order: Stage tabs → Left panel → Editor → Chat → Footer
- Skip to content link
- Focus visible indicators (blue outline)

**Screen Reader:**
- ARIA labels on all interactive elements
- Live regions for status updates
- Semantic HTML structure
- Descriptive link text

**Contrast:**
- Minimum 4.5:1 for normal text
- 3:1 for large text
- 3:1 for UI components

**Reduced Motion:**
- Respect prefers-reduced-motion
- Disable animations if set
- Instant transitions instead

---

## Loading States

**Initial Load:**
```
┌─────────────────────────────────────┐
│                                     │
│        [IPE Logo/Spinner]           │
│                                     │
│     Loading IPE-demo project...     │
│                                     │
└─────────────────────────────────────┘
```

**Stage Switch:**
```
[Skeleton UI showing panel outlines]
Fade in actual content after 200ms
```

**Document Load:**
```
Editor shows loading skeleton
Sections appear progressively
```

**Agent Response:**
```
Typing indicator: "..."
Pulse animation while waiting
```

---

**End of Interface Mockup**
