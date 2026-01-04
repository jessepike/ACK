# IPE Content Editor - Design Specification

---

**Version:** 1.0  
**Created:** 2024-12-31  
**Status:** Design Complete

---

## Overview

The Content Editor is the central workspace where users create, edit, and manage Discovery artifacts and all subsequent stage documentation. It occupies the main content area between the left panel (file browser) and right panel (agent chat).

**Design Principles:**
- Minimalist, distraction-free writing environment
- Progressive disclosure of complexity
- Inline editing with immediate feedback
- Consistent with markdown-first workflows

---

## Layout & Structure

### Editor Position

```
┌─────────────────────────────────────────────────────────┐
│ Top: Stage Tabs                                         │
├──────────┬────────────────────────────┬─────────────────┤
│          │                            │                 │
│  Left    │     CENTER                 │     Right       │
│  Panel   │     CONTENT EDITOR         │     Chat        │
│          │     (THIS COMPONENT)       │     Interface   │
│  Docs &  │                            │                 │
│  Status  │                            │     Agents +    │
│          │                            │     Humans      │
│          │                            │                 │
├──────────┴────────────────────────────┴─────────────────┤
│ Bottom: Footer (status, notifications)                  │
└─────────────────────────────────────────────────────────┘
```

### Editor Canvas Structure

```
┌─────────────────────────────────────────────────┐
│ concept.md                            [Raw ▼]   │ ← Header
├─────────────────────────────────────────────────┤
│ Status: In Progress  Created: 2024-12-31 [...]  │ ← Metadata
├─────────────────────────────────────────────────┤
│ [↶] [↷] | [B] [I] [H] [•] [Link] [Code] | [/]  │ ← Toolbar
├─────────────────────────────────────────────────┤
│                                                 │
│ ▾ What Is It?                          ☐ Done  │
│   [Editable content area]                       │
│                                                 │
│ ▸ Problem Being Solved                 ☐ Done  │
│                                                 │
│ ▾ Core Features                        ☐ Done  │
│   [Editable content area]                       │
│                                                 │
└─────────────────────────────────────────────────┘
       ↑
   Main editing canvas
```

---

## Editing Modes

### Primary Mode: WYSIWYG Markdown

**Default editing experience:**
- Rendered markdown with inline editing
- Headers, bold, italic, lists appear styled
- Click any text to edit directly
- Formatting applied as you type
- Clean, readable presentation

**Behavior:**
- `**text**` renders as **bold** but shows syntax when editing that text
- Headers render at appropriate size
- Lists show bullets/numbers
- Links show as clickable text
- Code blocks have syntax highlighting

### Secondary Mode: Raw Markdown

**Toggle to source view:**
- Plain text markdown with syntax highlighting
- See raw YAML frontmatter
- Direct editing of markdown syntax
- Useful for complex formatting or troubleshooting

**Toggle Control:**
- Dropdown in header: `[WYSIWYG ▼]` → `[Raw ▼]`
- Keyboard shortcut: `Cmd/Ctrl + Shift + M`

---

## YAML Frontmatter Display

### Form Fields (Default)

**Above content, editable fields:**

```
┌─────────────────────────────────────────────────┐
│ Status:     [In Progress      ▼]                │
│ Created:    2024-12-31 [Human]                  │
│ Updated:    2024-12-31 [Claude]                 │
│ Related:    [+ Add link]                        │
│             [research.md] [×]                    │
└─────────────────────────────────────────────────┘
```

**Features:**
- Dropdowns for controlled values (status)
- Date pickers for dates
- Auto-populated author on changes
- Tag-style pills for related documents
- Visual, form-based editing

### Raw YAML (When in Raw Mode)

```yaml
---
status: in-progress
stage: discovery
created: 2024-12-31 [Human]
updated: 2024-12-31 [Claude]
related: [research.md]
---
```

Direct text editing of YAML when in Raw markdown mode.

---

## Toolbar

### Fixed Toolbar Layout

```
[↶] [↷] | [B] [I] [H] [•] [Link] [Code] | [/] 
 ↑   ↑     ↑   ↑   ↑   ↑     ↑      ↑      ↑
Undo Redo Bold Italic Header List Link Code Command
```

**Position:** Fixed at top of editor canvas, always visible

**Controls:**

| Button | Function | Shortcut | Behavior |
|--------|----------|----------|----------|
| ↶ | Undo | Cmd/Ctrl+Z | Undo last change |
| ↷ | Redo | Cmd/Ctrl+Shift+Z | Redo undone change |
| B | Bold | Cmd/Ctrl+B | Wrap selection in `**` |
| I | Italic | Cmd/Ctrl+I | Wrap selection in `*` |
| H | Header | Cmd/Ctrl+H | Convert to header (cycles H1-H6) |
| • | List | Cmd/Ctrl+L | Create bullet/numbered list |
| Link | Insert Link | Cmd/Ctrl+K | Insert markdown link |
| Code | Code Block | Cmd/Ctrl+` | Wrap in code fence |
| / | Command Palette | / | Open formatting commands |

### Command Palette

**Trigger:** Type `/` in editor

**Quick formatting options:**
```
/h1      Convert to Heading 1
/h2      Convert to Heading 2
/bold    Make text bold
/italic  Make text italic
/link    Insert link
/code    Insert code block
/quote   Insert blockquote
/table   Insert table
/image   Insert image
```

**Behavior:**
- Autocomplete as you type
- Arrow keys to navigate
- Enter to select
- Esc to cancel

---

## Section Interaction

### Collapsed Section

```
▸ Problem Being Solved                 ☐ Done
```

**Behavior:**
- Click header text or arrow to expand
- Shows completion checkbox
- Checkbox is always visible (collapsed or expanded)

### Expanded Section

```
▾ What Is It?                          ☐ Done
  IPE (Integrated Planning Environment) is a planning
  layer that orchestrates AI-augmented development from
  concept to implementation-ready state.
  
  It bridges the gap between... [💬]
```

**Behavior:**
- Click header or arrow to collapse
- Content fully editable
- Click anywhere in content to edit
- Comment indicators (💬) show where comments exist

### Section Completion

**Mark Complete Checkbox:**
- Located in section header, right-aligned
- Available in both collapsed and expanded states
- Requires manual human check
- Checking updates section status
- Section header text changes color:
  - Red (unchecked, empty)
  - Orange (unchecked, has content)
  - Green (checked)

**Visual States:**

```
▸ Problem Being Solved                 ☐     (Red - empty)
▸ Core Features                        ☐     (Orange - content, incomplete)
▸ What Is It?                          ☑     (Green - complete)
```

---

## Comments & Annotations

### Inline Comments (MVP)

**Trigger:**
1. Select text in editor
2. Comment button appears in selection toolbar
3. OR keyboard shortcut: `Cmd/Ctrl+/`

**Comment Interface:**

```
[Selected text highlighted]
                           ┌────────────────────────┐
                           │ 💬 Leave a comment     │
                           │                        │
                           │ @mention agents or     │
                           │ add feedback           │
                           │                        │
                           │        [Cancel] [Add]  │
                           └────────────────────────┘
```

**Comment Display:**

```
It bridges the gap between... [💬3]
                               ↑
                    3 comments on this text
```

**Click indicator to expand:**

```
┌──────────────────────────────────────────┐
│ 💬 Comments (3)                          │
├──────────────────────────────────────────┤
│ @Human: Should we emphasize cost here?   │
│   2 minutes ago                          │
├──────────────────────────────────────────┤
│ @Claude: Good point, research shows      │
│ 60% value cost reduction                 │
│   1 minute ago                           │
├──────────────────────────────────────────┤
│ @Human: Added to Value Prop section      │
│   Just now                               │
├──────────────────────────────────────────┤
│ [Reply...]                               │
└──────────────────────────────────────────┘
```

### Comment Threading

**MVP: Linear threading**
- Comments stack chronologically
- Single reply thread per comment anchor
- No nested sub-threads
- Simple, readable conversation flow

**Future Enhancement (Backlog):**
- Nested replies
- Resolve/unresolve comments
- Comment filtering by author/date

### @Mentions in Comments

**Syntax:** `@AgentName` or `@PersonName`

**Behavior:**
- Autocomplete suggestions appear
- Mentioned entity gets notification
- Agents can respond directly in comment thread
- Creates conversational context around specific text

---

## Auto-Save

### Continuous Save

**Behavior:**
- Saves on every edit (debounced by 1-2 seconds)
- No explicit save button needed
- Status indicator in footer shows save state

**Save States:**

```
Saved                    (Gray - idle)
Saving...                (Orange - in progress)
Saved 2 seconds ago      (Gray - complete)
Error saving             (Red - failure, with retry)
```

**Version Control:**
- Each save creates version snapshot
- Enables undo/redo across sessions
- Change history maintained

---

## Progressive Disclosure

### Default View

**On document open:**
- All sections collapsed
- Only section headers visible
- Completion checkboxes visible
- Metadata form fields shown

```
┌─────────────────────────────────────────────────┐
│ Status: In Progress  Created: 2024-12-31        │
├─────────────────────────────────────────────────┤
│                                                 │
│ ▸ What Is It?                          ☐ Done  │
│ ▸ Problem Being Solved                 ☐ Done  │
│ ▸ Core Features                        ☐ Done  │
│ ▸ Value Proposition                    ☐ Done  │
│ ▸ Target User                          ☐ Done  │
│ ▸ Success Looks Like                   ☐ Done  │
│ ▸ Out of Scope                         ☐ Done  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Expand on-demand:**
- Click section to expand
- Work in that section
- Collapse when done
- Reduces cognitive load

### Content Preview

**When section has content (but collapsed):**

```
▸ What Is It?                          ☐ Done
  IPE (Integrated Planning Environment) is a planning
  layer that orchestrates...
```

Shows first 2-3 sentences as preview text (lighter color).

**When section is empty:**

```
▸ Problem Being Solved                 ☐ Done
```

No preview, just header.

---

## Keyboard Shortcuts

### Navigation
- `Cmd/Ctrl + ↑/↓` - Move between sections
- `Tab` - Expand next section
- `Shift+Tab` - Collapse current section

### Editing
- `Cmd/Ctrl + B` - Bold
- `Cmd/Ctrl + I` - Italic
- `Cmd/Ctrl + K` - Insert link
- `Cmd/Ctrl + H` - Header (cycles levels)
- `Cmd/Ctrl + L` - List
- `Cmd/Ctrl + ` ` - Code block
- `/` - Command palette

### Actions
- `Cmd/Ctrl + Z` - Undo
- `Cmd/Ctrl + Shift + Z` - Redo
- `Cmd/Ctrl + /` - Add comment
- `Cmd/Ctrl + Shift + M` - Toggle raw/WYSIWYG mode

### Document
- `Cmd/Ctrl + S` - Manual save (if enabled)
- `Cmd/Ctrl + P` - Print/export

---

## Visual Design

### Typography

**Headers:**
- H1: 24px, bold
- H2: 20px, bold
- H3: 18px, bold
- Body: 15px, regular
- Code: 13px, monospace

**Spacing:**
- Section padding: 16px vertical
- Paragraph spacing: 12px
- Line height: 1.6

### Colors (Dark Theme)

**Text:**
- Primary: #e0e0e0
- Secondary: #a0a0a0
- Placeholder: #606060

**Section Status:**
- Empty (Red): #f44336
- In Progress (Orange): #ff9800
- Complete (Green): #4caf50

**UI Elements:**
- Background: #1e1e1e
- Panel: #252526
- Border: #3e3e42
- Accent: #007acc

**Syntax Highlighting:**
- Keywords: #569cd6
- Strings: #ce9178
- Comments: #6a9955

### Spacing & Layout

**Editor width:** 60% of center area (flexible)
**Max content width:** 800px (readable line length)
**Padding:** 24px horizontal, 16px vertical

---

## Interaction States

### Hover States
- Section headers: Slight background change
- Toolbar buttons: Background highlight
- Checkboxes: Border color change

### Focus States
- Active section: Subtle border or background
- Text input: Standard cursor
- No intrusive focus indicators

### Loading States
- Document load: Skeleton UI
- Save in progress: Subtle spinner in footer
- No blocking loaders

---

## Future Enhancements (Backlog)

### Editor Features
- **Rich media embedding** - Images, videos, diagrams
- **Table editing** - Visual table builder
- **Markdown preview pane** - Side-by-side view option
- **Version comparison** - Diff view for changes
- **Export options** - PDF, DOCX, HTML

### Comments
- **Resolve/unresolve** - Mark comments as addressed
- **Comment filtering** - By author, date, status
- **Nested threading** - Reply to specific comments
- **Suggestion mode** - Propose edits within comments

### Collaboration
- **Real-time editing** - See others' cursors
- **Presence indicators** - Who's viewing/editing
- **Change tracking** - See who changed what
- **Comment notifications** - Alert when mentioned

### AI Integration
- **Smart suggestions** - AI suggests content as you write
- **Grammar/style** - Real-time writing assistance
- **Content generation** - `/generate` command for AI content
- **Summarization** - Auto-summarize long sections

### Accessibility
- **Screen reader support** - Full ARIA labels
- **Keyboard navigation** - Navigate without mouse
- **High contrast mode** - Accessibility themes
- **Font size control** - User-adjustable sizing

---

## Technical Considerations

### Editor Library Options
- **ProseMirror** - Robust, extensible WYSIWYG
- **CodeMirror** - Excellent for raw markdown mode
- **TipTap** - Modern, Vue-compatible ProseMirror wrapper
- **Monaco** - VS Code's editor (might be overkill)

### Data Format
- Store as markdown files with YAML frontmatter
- Real-time parsing of frontmatter into form fields
- Bidirectional sync between form and YAML

### Performance
- Debounce auto-save (1-2 second delay)
- Virtual scrolling for very long documents
- Lazy load collapsed sections
- Optimize re-renders on each keystroke

---

## Success Metrics

**Usability:**
- Time to complete first artifact
- Clicks required to mark section complete
- Errors in markdown syntax (should be zero)

**Efficiency:**
- Keyboard shortcut usage
- Command palette adoption
- Comment usage frequency

**Quality:**
- Document completeness at finalization
- Number of revisions needed
- User satisfaction with editing experience

---

**End of Content Editor Specification**
