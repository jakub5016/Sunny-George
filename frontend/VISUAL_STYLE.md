# MegaWatt Visual Style Specification

This document defines the visual identity and UI style for **Sunny George** — the MegaWatt solar panel sales assistant. It translates the MegaWatt brand guidelines into concrete rules for the React frontend.

**Brand slogan:** *MegaWatt — Your energy, our passion.*

---

## 1. Brand Core

MegaWatt should feel like a blend of **energy**, **clarity**, **safety**, and **innovation**. The application represents a modern solar technology company that is trustworthy, precise, and approachable.

### Design principles

| Principle | Description |
|-----------|-------------|
| Modern minimalism | Clean layouts, no visual clutter, focus on content |
| Technical professionalism | Structured information, data-driven presentation |
| Transparency | Generous white space, readable typography, honest communication |
| Solar optimism | Warm accents that evoke sunlight and clean energy |

### Application context

Sunny George is a conversational sales assistant. The UI should feel like a professional consultation tool — not a generic chatbot. Panels, forms, and message areas should reinforce MegaWatt's expertise in photovoltaic systems.

---

## 2. Color Palette

### Primary colors

| Name | HEX | Role | UI usage |
|------|-----|------|----------|
| Solar Yellow | `#FFD700` | Energy, sun, optimism, power | Primary CTAs, active states, highlights, accent icons |
| Deep Navy | `#0A2342` | Trust, stability, technology | Headers, navigation, primary text on light backgrounds |
| Pure White | `#FFFFFF` | Clarity, clean energy | Page backgrounds, cards, message bubbles (assistant) |
| Graphite | `#4A4A4A` | Solidity, engineering | Body text, secondary labels, borders, disabled states |

### Extended palette (derived)

| Name | HEX | Usage |
|------|-----|-------|
| Navy Muted | `#1A3A5C` | Hover states on navy elements |
| Yellow Hover | `#E6C200` | Button hover on primary CTAs |
| Yellow Light | `#FFF8DC` | Subtle highlight backgrounds, info banners |
| Navy Tint | `#E8EDF2` | Section backgrounds, input field backgrounds |
| Border Light | `#D1D5DB` | Dividers, input borders |
| Error Red | `#DC2626` | Error messages, validation feedback |
| Success Green | `#16A34A` | Confirmation states, positive metrics |

### Color application rules

- **Backgrounds:** Predominantly white (`#FFFFFF`) with navy-tinted sections (`#E8EDF2`) for visual separation.
- **Text:** Deep Navy (`#0A2342`) for headings; Graphite (`#4A4A4A`) for body copy.
- **Actions:** Solar Yellow (`#FFD700`) for primary buttons (Send, Start, Submit). Text on yellow buttons should be Deep Navy for contrast.
- **Chat messages:**
  - User messages: Deep Navy background, white text.
  - Assistant messages: White or Navy Tint background, Graphite text, optional yellow left border accent.
- **Avoid:** Saturated greens or blues unrelated to the palette; heavy gradients; dark-mode-first layouts (light theme is the default).

---

## 3. Typography

### Font families

| Role | Family | Weights | Source |
|------|--------|---------|--------|
| Headings | **Montserrat** | 700 (Bold), 800 (Extra Bold) | Google Fonts |
| Body | **Open Sans** | 300 (Light), 400 (Regular), 600 (Semi Bold) | Google Fonts |

### Type scale

| Element | Font | Size | Weight | Line height | Color |
|---------|------|------|--------|-------------|-------|
| Page title (h1) | Montserrat | 28–32px | 800 | 1.2 | `#0A2342` |
| Section title (h2) | Montserrat | 20–24px | 700 | 1.3 | `#0A2342` |
| Panel title | Montserrat | 22px | 700 | 1.3 | `#0A2342` |
| Body text | Open Sans | 16px | 400 | 1.6 | `#4A4A4A` |
| Small / caption | Open Sans | 14px | 400 | 1.5 | `#4A4A4A` |
| Button label | Montserrat | 14–16px | 700 | 1 | `#0A2342` |
| Input placeholder | Open Sans | 16px | 300 | 1.5 | `#4A4A4A` at 60% opacity |

### Typography rules

- Use Montserrat only for headings, labels, and button text.
- Use Open Sans for all conversational content, descriptions, and form input.
- Limit heading levels to h1–h3 in the application.
- Prefer sentence case for UI labels (e.g. "Send message", not "SEND MESSAGE").

---

## 4. Logo

### Structure

The MegaWatt logo consists of two parts:

1. **Logomark (symbol):** A stylized letter "M" where one leg flows into a sun ray or simplified photovoltaic panel shape.
2. **Logotype (wordmark):** "Mega" in Deep Navy (heavier weight) + "Watt" in Solar Yellow (lighter weight).

### Usage in the application

| Context | Specification |
|---------|---------------|
| Header | Logomark + wordmark, left-aligned; max height 40px |
| Favicon | Logomark only |
| Loading state | Logomark centered with subtle pulse animation |
| Chat avatar (assistant) | Logomark in a circular navy container |

### Clear space and constraints

- Maintain clear space equal to the height of the "M" in the logomark on all sides.
- Do not stretch, rotate, or recolor individual logo elements outside the defined palette.
- On yellow backgrounds, use the navy logomark variant only.

---

## 5. Layout and Spacing

### Grid and structure

- **Max content width:** 960px for the main chat area; 1200px for full-page layouts.
- **Page padding:** 24px on mobile, 40px on desktop.
- **Section spacing:** 32px between major blocks (chat window, input form, voice recorder).
- **Component spacing:** 16px between related elements; 8px for tight groupings.

### White space

Digital materials should breathe. Prefer fewer elements per screen with ample padding over dense layouts. Empty states should feel intentional, not broken.

### Responsive behavior

- Single-column layout on viewports below 768px.
- Chat window scrolls independently; input area remains fixed at the bottom on mobile.
- Touch targets: minimum 44×44px for buttons and interactive controls.

---

## 6. UI Components

### Buttons

| Variant | Background | Text | Border | Usage |
|---------|------------|------|--------|-------|
| Primary | `#FFD700` | `#0A2342` | none | Send, Start chat, Confirm |
| Secondary | transparent | `#0A2342` | 2px `#0A2342` | Cancel, secondary actions |
| Disabled | `#E8EDF2` | `#4A4A4A` at 50% | none | Inactive states |

- Border radius: 8px
- Padding: 12px 24px
- Hover (primary): background `#E6C200`
- Focus: 2px outline in Solar Yellow with 2px offset

### Form inputs

- Background: `#FFFFFF` or `#E8EDF2`
- Border: 1px `#D1D5DB`; focus border: 2px `#0A2342`
- Border radius: 8px
- Padding: 12px 16px
- Textarea minimum height: 80px (3 rows)

### Chat window

- Container: white card with 1px `#D1D5DB` border or subtle shadow (`0 2px 8px rgba(10, 35, 66, 0.08)`)
- Border radius: 12px
- Message spacing: 12px between messages
- User bubble: `#0A2342` background, white text, right-aligned
- Assistant bubble: `#E8EDF2` background, `#4A4A4A` text, left-aligned; optional 3px left border in `#FFD700`
- Timestamps and metadata: 12px Open Sans Light, `#4A4A4A` at 70% opacity

### Cards and panels

- Background: `#FFFFFF`
- Border radius: 12px
- Shadow: `0 2px 8px rgba(10, 35, 66, 0.08)`
- Panel title: Montserrat Bold, Deep Navy
- Panel description: Open Sans Regular, Graphite

### Voice recorder

- Record button: circular, 56px diameter, Solar Yellow background, navy microphone icon
- Recording state: pulsing yellow ring animation
- Transcript display: italic Open Sans Light below the message

### Loading and error states

- **Loading:** Centered logomark with "Loading…" in Open Sans; avoid generic spinners when possible.
- **Error:** Red text (`#DC2626`) on `#FFF8DC` background banner; include actionable guidance.
- **Empty chat:** Friendly prompt in Open Sans: "Ask Sunny George about solar panels, savings, or installation."

---

## 7. Imagery and Iconography

### Photography (when used)

- High-quality daylight photos of real installations.
- Natural lighting; avoid heavy filters.
- Subjects: rooftops, panels, satisfied homeowners, service vehicles.

### Icons

- Style: outlined, 2px stroke, rounded caps.
- Color: Deep Navy default; Solar Yellow for active or emphasis states.
- Size: 20px inline, 24px in buttons.

### Data visualization

- Charts in offers and savings estimates: navy-and-white aesthetic with yellow highlights for key metrics.
- Axis labels: Open Sans 12px; data points: Montserrat Bold.

---

## 8. Tone of Voice (UI Copy)

All user-facing text — labels, placeholders, assistant responses, error messages — should follow MegaWatt's communication style.

| Trait | Guideline | Example |
|-------|-----------|---------|
| Expert but accessible | Explain technical concepts as customer benefits | "A 6 kW system can cut your bill by up to 40%" instead of "Installed capacity: 6 kWp" |
| Concrete | Lead with numbers — time, savings, efficiency | "Installation in 2–3 days" |
| Trust-building | Emphasize end-to-end support | "We're with you from design to grid connection" |
| Warm professionalism | Friendly without being casual | "How can I help you explore solar today?" |

### Copy patterns

- **Greeting:** "Welcome to MegaWatt. I'm Sunny George — your solar advisor."
- **CTA buttons:** Action-oriented verbs — "Send", "Start conversation", "Get a quote".
- **Errors:** Explain what happened and what to do next — never blame the user.
- **End of conversation:** "Thank you for chatting with MegaWatt. We'll be here when you're ready."

---

## 9. Design Tokens (CSS Variables)

Recommended token definitions for implementation:

```css
:root {
  /* Colors */
  --color-solar-yellow: #FFD700;
  --color-solar-yellow-hover: #E6C200;
  --color-solar-yellow-light: #FFF8DC;
  --color-deep-navy: #0A2342;
  --color-navy-muted: #1A3A5C;
  --color-navy-tint: #E8EDF2;
  --color-pure-white: #FFFFFF;
  --color-graphite: #4A4A4A;
  --color-border: #D1D5DB;
  --color-error: #DC2626;
  --color-success: #16A34A;

  /* Typography */
  --font-heading: "Montserrat", sans-serif;
  --font-body: "Open Sans", sans-serif;

  /* Spacing */
  --space-xs: 8px;
  --space-sm: 12px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;

  /* Radii */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-card: 0 2px 8px rgba(10, 35, 66, 0.08);
  --shadow-elevated: 0 4px 16px rgba(10, 35, 66, 0.12);

  /* Layout */
  --content-max-width: 960px;
  --page-padding: 24px;
}
```

---

## 10. Accessibility

- Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text (WCAG AA).
- Solar Yellow buttons must use Deep Navy text to meet contrast requirements.
- All interactive elements must be keyboard-navigable with visible focus indicators.
- Form fields require associated `<label>` elements.
- Voice recorder must provide text alternatives for audio content (transcripts).

---

## 11. Brand Touchpoints (Reference)

These guidelines originate from MegaWatt's broader identity system. The frontend should stay consistent with:

| Touchpoint | Key visual traits |
|------------|-------------------|
| Service vehicles | White vans, large yellow logo, navy tagline |
| Workwear | Navy polo shirts, yellow embroidered logo |
| Website | Generous white space, daylight photography, yellow CTAs |
| Documentation | Clean navy-and-white offers with savings charts |

---

## 12. Implementation Checklist

When styling a new component, verify:

- [ ] Colors come from the defined palette (no ad-hoc hex values)
- [ ] Headings use Montserrat; body text uses Open Sans
- [ ] Primary actions use Solar Yellow with navy text
- [ ] Spacing follows the 8px grid (8, 12, 16, 24, 32, 40)
- [ ] Border radius is 8px (controls) or 12px (cards)
- [ ] UI copy matches the tone of voice guidelines
- [ ] Focus states and contrast ratios meet accessibility requirements
