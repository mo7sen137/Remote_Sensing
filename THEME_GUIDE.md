# 🎨 Professional Cyberpunk Theme Guide

## Updated Design System (May 2026)

The application now features a **professional cyberpunk-inspired dark theme** with neon colors optimized for satellite imagery analysis.

---

## 🌈 Color Palette

### Primary Colors
- **Background:** Deep Black (#0a0e27) with purple gradient overlay
- **Accent 1:** Neon Green (#00ff88) - Primary action indicators
- **Accent 2:** Neon Cyan (#00ffff) - Headers and main highlights
- **Accent 3:** Neon Magenta (#ff00ff) - Secondary actions and emphasis
- **Accent 4:** Neon Lime (#00ffaa) - Success and positive status

### Text Colors
- **Primary Text:** Light Purple (#e0e0ff)
- **Secondary Text:** Muted Gray (#d0d0e8)
- **Accent Text:** Neon Green (#00ffaa)

### Component Colors
- **Water:** Cyan Blue
- **Agriculture:** Forest Green
- **Urban:** Bright Red
- **Desert:** Golden Yellow

---

## 🎭 Design Elements

### Typography
```css
Fonts:
- Headers: 'Orbitron' (bold, futuristic)
- Body: 'Space Mono' (monospace, clean)
- Letter spacing: 1-2px (technical feel)
```

### Effects
- **Glow Effects:** Neon text shadow with cyan-magenta transitions
- **Box Shadows:** Layered shadows with neon outlines
- **Animations:** Subtle pulsing and glowing effects
- **Transitions:** 0.3-0.4s cubic-bezier for smooth interactions

### Interactive Elements

#### Buttons
```
Default: Blue-Magenta gradient
Hover: Cyan-Magenta gradient with glow
Active: Scaled up with enhanced shadow
```

#### Inputs
```
Border: Neon Green (#00ff88)
Focus: Changes to Neon Magenta (#ff00ff)
Background: Semi-transparent dark overlay
```

#### Metrics Cards
```
Background: Dark with purple tint
Left Border: Neon Green (5px)
Top Border: Neon Magenta (2px)
Shadow: Layered neon glow effect
```

---

## 📊 CSS Classes Styling

### `.stMetric`
- Gradient background (dark purples)
- Multi-color border system
- Hover lift effect (-3px transform)
- Responsive text sizing

### `.stButton > button`
- Vibrant gradient (magenta-cyan)
- Text-transform uppercase
- Letter-spacing for technical feel
- Complex box-shadow layering
- Cubic-bezier timing for bouncy feel

### `.stTabs [data-baseweb="tab-list"]`
- Dark background with green border
- Individual tab styling
- Selected state with full gradient
- Hover effects with glow

### `.stDataFrame`
- Dark background with double gradient
- Magenta-Cyan header gradient
- Hover row highlighting
- Alternating border colors

### `.stFileUploader`
- Dashed green border
- Transparent green background
- Responds to hover with magenta transformation

---

## 🎯 Page Layouts

### Home Page
- Large neon title with animation
- 4-column metrics dashboard
- Workflow visualization box
- Expandable technical sections
- Professional footer CTA

### Upload Page
- Two-column layout (bands + metadata)
- Custom info boxes with gradients
- Progress indicator (X/6 bands)
- Upload summary metrics

### Classification Page
- Model selection dropdown
- Processing pipeline visualization
- Real-time job status display
- Classification execution button

### Results Page
- Classification map display
- Interactive legend with colors
- Detailed statistics table
- Multi-format export buttons

---

## 🚀 Usage

### Running the App
```bash
streamlit run app/main.py
```

### Accessing via Browser
- **Local:** http://localhost:8502
- **Network:** http://[YOUR_IP]:8502

### Features
✨ Hover effects on all interactive elements
✨ Smooth page transitions
✨ Real-time progress visualization
✨ Responsive mobile-friendly layout
✨ Dark mode optimized (never changes)

---

## 🔧 Customization

### To Change Colors
Edit `/app/main.py` in the CSS section:
```python
# Replace color hex codes in:
# - Primary colors (#00ff88, #00ffff, #ff00ff)
# - Text colors (#e0e0ff, #d0d0e8)
# - Gradients and transitions
```

### To Modify Animations
Edit keyframes in CSS:
```python
@keyframes neon-glow { ... }
@keyframes pulse { ... }
```

### To Adjust Typography
Modify font imports and sizing:
```python
@import url('https://fonts.googleapis.com/css2?...')
font-family: 'Font-Name', fallback;
font-size: calculated-size;
```

---

## 📈 Performance Notes

- **CSS-only theming** (no JavaScript needed)
- **Native Streamlit components** (fully compatible)
- **GPU-optimized gradients** (hardware acceleration)
- **Smooth 60fps animations** on modern browsers

---

## 🎨 Comparison: Before → After

| Aspect | Before | After |
|--------|--------|-------|
| Background | Navy blue (#1a1f3a) | Deep black gradient |
| Accents | Red (#e94560) | Neon Green + Cyan + Magenta |
| Typography | Default | Orbitron + Space Mono |
| Effects | Basic | Advanced glow + animations |
| Interactivity | Simple | Complex transitions |
| Professional Level | Medium | **PREMIUM** 🌟 |

---

## 📞 Support

For theme issues or customization needs, refer to:
- Main application: `/app/main.py` (lines 1-350)
- Configuration: `/config.py`
- Examples: `/COMPLETE_OVERVIEW.md`

---

**Last Updated:** May 5, 2026  
**Theme Version:** 2.0 - Cyberpunk Professional Edition  
**Status:** ✅ Production Ready
