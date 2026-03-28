---
trigger: always_on
---

# Design System & UI Rules
## 1. Color Palette (Brand Colors)
Use these exact hex codes for the project branding. Do not hallucinate other shades unless requested for hover states.
- **Primary Purple:** `#5A1F8A` (rgb(90, 31, 138)) - HSL: `273 63% 33%`
- **Secondary Pink:** `#E43263` (rgb(228, 50, 99)) - HSL: `345 76% 51%`
- **Tertiary Orange:** `#F09E3F` (rgb(240, 158, 63)) - HSL: `33 87% 59%`
## 2. Brand Gradient
Whenever a "main gradient" or "brand background" is requested, use a linear gradient combining the three colors above:
- **CSS Class:** `.brand-gradient`
- **CSS Rule:** `linear-gradient(135deg, #5A1F8A 0%, #E43263 50%, #F09E3F 100%)`
## 3. Glassmorphism Style Guide
Apply "Glassmorphism" to cards, modals, and sidebars. The components should look like frosted glass floating over the background.
**CSS Classes:**
- `.glass-card` (Dark themed)
- `.glass-card-light` (Light themed)
- `.glass-card-hover` (With hover effect)
**CSS Properties enforced:**
- **Background:** `rgba(20, 20, 20, 0.4)` (Dark) or `rgba(255, 255, 255, 0.1)` (Light).
- **Backdrop Filter:** `backdrop-filter: blur(12px);`.
- **Border:** `1px solid rgba(255, 255, 255, 0.2)`.
- **Shadow:** `box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);`.
- **Rounded Corners:** `border-radius: 16px`.
## 4. Tailwind Configuration
The brand colors are available as Tailwind utilities:
- `text-brand-purple`, `bg-brand-purple`, etc.
- `text-brand-pink`, `bg-brand-pink`, etc.
- `text-brand-orange`, `bg-brand-orange`, etc.


