# MY-SITE Repository Analysis

## Repository: KINGSACCOUNT1/MY-SITE

### 🎯 Key Features Found:

#### 1. **Testimonial Popup System**
- **File**: `static/js/testimonials-popup.js`
- **Features**:
  - 70 real people testimonials with avatars
  - Countries with flags (emoji)
  - Amount earned & invested display
  - Auto-popup every 25 seconds
  - Smooth slide-in animation (left side)
  - Close button functionality
  - Random selection (no repeats until all shown)
  - Professional design with gradients

**Design Details**:
- Position: Fixed bottom-left (20px left, 80px bottom)
- Background: Gradient (135deg, #1a1a2e 0%, #16213e 100%)
- Border: Gold accent (rgba(255, 215, 0, 0.2))
- Animation: translateX slide effect
- Z-index: 9997

#### 2. **Crypto Ticker**
- **File**: `static/js/crypto-ticker.js`
- **Features**:
  - Fixed top position
  - 10 cryptocurrencies (BTC, ETH, USDT, BNB, SOL, XRP, ADA, DOGE, DOT, MATIC)
  - Live price updates every 30 seconds
  - Scrolling animation (seamless loop)
  - Color-coded changes (green/red)
  - Django API integration (/investments/api/ticker/)
  - Fallback prices if API fails

**Design Details**:
- Position: Fixed top (z-index: 9998)
- Background: Gradient (90deg, #1a1a2e 0%, #16213e 100%)
- Animation: 30s linear infinite scroll
- Responsive design

#### 3. **Tawk.to Live Chat**
- **Implementation**: Embedded in base.html
- **Property ID**: 69c1f2a729e9681c3d64de5d
- **Widget ID**: 1jkepnodo
- **Features**:
  - Environment variable support
  - Fallback to hardcoded values
  - Context processor integration
