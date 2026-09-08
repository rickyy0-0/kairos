import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    # Color Palette: Sky & Atmosphere Theme
    SKY_DEEP = RGBColor(15, 23, 42)       # Slate / Deep Atmosphere Navy (#0f172a)
    SKY_NAVY = RGBColor(24, 39, 75)       # Rich Sky Navy (#18274b)
    SKY_BLUE = RGBColor(14, 165, 233)     # Bright Sky Azure (#0ea5e9)
    SKY_CERULEAN = RGBColor(2, 132, 199)  # Deep Sky Cerulean (#0284c7)
    SKY_CYAN = RGBColor(6, 182, 212)      # Cloud Cyan (#06b6d4)
    SKY_LIGHT = RGBColor(224, 242, 254)   # Soft Ice Blue (#e0f2fe)
    SKY_WHITE = RGBColor(248, 250, 252)   # Pure Cloud White (#f8fafc)
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate Muted (#94a3b8)
    ACCENT_EMERALD = RGBColor(16, 185, 129) # Nature Green (#10b981)
    ACCENT_AMBER = RGBColor(245, 158, 11)   # Sun Amber (#f59e0b)
    ACCENT_CORAL = RGBColor(244, 63, 94)    # Heat Coral (#f43f5e)

    blank_slide_layout = prs.slide_layouts[6]

    def add_header(slide, category, title, subtitle=None):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(8.0), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SKY_CYAN
        p_cat.font.name = "Arial"

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = SKY_WHITE
        p_title.font.name = "Arial"

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.font.name = "Arial"

    def create_card(slide, left, top, width, height, bg_color=SKY_NAVY, border_color=SKY_BLUE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def set_slide_background(slide, color=SKY_DEEP):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1, SKY_DEEP)

    # Accent decorative glow bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    bar.fill.solid()
    bar.fill.fore_color.rgb = SKY_BLUE
    bar.line.fill.background()

    # Title & Subtitle text box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(3.8))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p_badge = tf1.paragraphs[0]
    p_badge.text = "NATIONAL URBAN CLIMATE DECISION INTELLIGENCE PLATFORM"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = SKY_CYAN
    p_badge.font.name = "Arial"
    p_badge.space_after = Pt(14)

    p_main = tf1.add_paragraph()
    p_main.text = "KAIROS INDIA"
    p_main.font.size = Pt(44)
    p_main.font.bold = True
    p_main.font.color.rgb = SKY_WHITE
    p_main.font.name = "Arial"
    p_main.space_after = Pt(8)

    p_desc = tf1.add_paragraph()
    p_desc.text = "Data-Driven Urban Heat Detection, Explainable Physical Cause Attribution, Multi-Vector Impact Prediction & Optimal Cooling Capital Allocation"
    p_desc.font.size = Pt(16)
    p_desc.font.color.rgb = SKY_LIGHT
    p_desc.font.name = "Arial"
    p_desc.space_after = Pt(20)

    p_foot = tf1.add_paragraph()
    p_foot.text = "Covering All 28 States & 8 Union Territories • 12+ Pre-Calibrated Metros • Knapsack Budget Optimizer • Grounded AI Engine"
    p_foot.font.size = Pt(12)
    p_foot.font.color.rgb = TEXT_MUTED
    p_foot.font.name = "Arial"

    # =========================================================================
    # SLIDE 2: THE PROBLEM / CRISIS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2, SKY_DEEP)
    add_header(s2, "The Climate Challenge", "The Urban Heatscape Crisis Facing Indian Cities", "Why passive temperature reporting fails municipal decision makers")

    cards_data_s2 = [
        {"title": "1. Severe Thermal Anomalies", "desc": "Urban heat islands elevate local surface temperatures by +4°C to +8°C above rural baselines, trapping deadly heat in high-density informal and commercial settlements.", "stat": "+6.5°C", "sub": "Peak Surface Delta", "color": ACCENT_CORAL},
        {"title": "2. Power Grid Overload", "desc": "HVAC cooling spikes trigger massive electrical transmission loss and costly peak-hour brownouts, straining state electricity utilities and spiking citizen bills.", "stat": "₹34+ Cr/yr", "sub": "Cooling Waste in Metros", "color": ACCENT_AMBER},
        {"title": "3. Water Depletion Nexus", "desc": "Extreme ambient heat drives uncoordinated municipal water use and HVAC chiller evaporation, depleting precious urban aquifers in drought-vulnerable zones.", "stat": "1,400+ ML", "sub": "Annual Heat Water Surge", "color": SKY_CYAN},
        {"title": "4. Social Vulnerability", "desc": "Informal workers, elderly residents, and children lack mechanical air conditioning, suffering elevated heatstroke risks with distant emergency hospital access.", "stat": "3.2M+", "sub": "Exposed Citizens in Risk Zones", "color": ACCENT_EMERALD}
    ]

    for i, card in enumerate(cards_data_s2):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.6)
        create_card(s2, left, top, Inches(5.6), Inches(2.4))
        
        tbox = s2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(2.0))
        tf = tbox.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = card["title"]
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = SKY_WHITE
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = card["desc"]
        p1.font.size = Pt(11)
        p1.font.color.rgb = SKY_LIGHT
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = f"{card['stat']}  •  {card['sub']}"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = card["color"]

    # =========================================================================
    # SLIDE 3: THE KAIROS SOLUTION ARCHITECTURE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3, SKY_DEEP)
    add_header(s3, "Product Architecture", "The KAIROS End-to-End Climate Intelligence Pipeline", "Transforming raw GIS satellite telemetry into actionable municipal cooling investments")

    steps = [
        {"num": "01", "name": "DETECT", "desc": "Spatial GIS thermal grid detecting microclimate hotspots at high geographic resolution."},
        {"num": "02", "name": "EXPLAIN", "desc": "6-Factor physical cause attribution decomposing heat drivers summing to strictly 100%."},
        {"num": "03", "name": "PREDICT", "desc": "Multi-vector impact quantifying excess energy loss (GWh), water stress, and health risks."},
        {"num": "04", "name": "SIMULATE", "desc": "Thermodynamic digital twin with interactive sliders for live Before vs After cooling."},
        {"num": "05", "name": "OPTIMIZE", "desc": "Knapsack algorithmic budget allocator maximizing protected lives under municipal caps."}
    ]

    for i, st in enumerate(steps):
        left = Inches(0.8 + i * 2.38)
        top = Inches(2.1)
        create_card(s3, left, top, Inches(2.2), Inches(4.6), bg_color=SKY_NAVY, border_color=SKY_BLUE)

        tbox = s3.shapes.add_textbox(left + Inches(0.15), top + Inches(0.2), Inches(1.9), Inches(4.2))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = st["num"]
        p0.font.size = Pt(28)
        p0.font.bold = True
        p0.font.color.rgb = SKY_CYAN
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = st["name"]
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = SKY_WHITE
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = st["desc"]
        p2.font.size = Pt(11)
        p2.font.color.rgb = SKY_LIGHT

    # =========================================================================
    # SLIDE 4: INDIA-WIDE MULTI-CITY COVERAGE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4, SKY_DEEP)
    add_header(s4, "National Scope", "India-Wide Geographic & Climate Zone Coverage", "Supporting all 28 States & 8 Union Territories with pre-calibrated and dynamic modeling")

    # Left Card: Coverage Details
    create_card(s4, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9))
    tbox_l = s4.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.1), Inches(4.5))
    tf_l = tbox_l.text_frame
    tf_l.word_wrap = True

    p0 = tf_l.paragraphs[0]
    p0.text = "Universal Geographic Hierarchy"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = SKY_WHITE
    p0.space_after = Pt(10)

    bullets_s4 = [
        ("Cascading Location Selector", "Navigate seamlessly from India → State/UT → City → Grid Sectors with persistent breadcrumbs."),
        ("12+ Pre-Calibrated Major Metros", "Chennai, Bengaluru, Mumbai, Delhi, Jaipur, Hyderabad, Ahmedabad, Kolkata, Pune, Kochi, Lucknow, Nagpur."),
        ("Dynamic Town/City Fallback", "Type ANY Indian town or city to automatically synthesize a modeled microclimate profile on the fly."),
        ("Regional Electricity Tariffs", "Tariffs calibrated per state (e.g. ₹8.20/kWh in TN, ₹8.50/kWh in KA) for precise financial accounting."),
        ("Climate Zone Diversity", "Tailored physical equations for Coastal Maritime, Semi-Arid, Tropical Savanna, and Indo-Gangetic Plains.")
    ]

    for title, bdesc in bullets_s4:
        p = tf_l.add_paragraph()
        p.text = f"• {title}: {bdesc}"
        p.font.size = Pt(11)
        p.font.color.rgb = SKY_LIGHT
        p.space_after = Pt(8)

    # Right Card: Metro Quick Comparison Preview
    create_card(s4, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9))
    tbox_r = s4.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.5))
    tf_r = tbox_r.text_frame
    tf_r.word_wrap = True

    p0 = tf_r.paragraphs[0]
    p0.text = "Regional Microclimate Baseline Examples"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = SKY_CYAN
    p0.space_after = Pt(12)

    metros_data = [
        ("Chennai (Tamil Nadu)", "Tropical Maritime", "39.3°C Avg", "Water Stress 78/100", "High Albedo Focus"),
        ("Bengaluru (Karnataka)", "Elevated Savanna", "33.4°C Avg", "Water Stress 72/100", "Canopy Expansion"),
        ("Jaipur (Rajasthan)", "Arid / Semi-Desert", "45.7°C Avg", "Water Stress 85/100", "Dry Cool Roofs Only"),
        ("Delhi (National Capital)", "Subtropical Continental", "42.8°C Avg", "Water Stress 82/100", "Transit Shade Shelters")
    ]

    for city, climate, temp, water, action in metros_data:
        p = tf_r.add_paragraph()
        p.text = f"📍 {city}"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = SKY_WHITE
        p_sub = tf_r.add_paragraph()
        p_sub.text = f"    Climate: {climate} | {temp} | {water} | Strategy: {action}"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(8)

    # =========================================================================
    # SLIDE 5: SPATIAL GIS THERMAL MAPPING
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5, SKY_DEEP)
    add_header(s5, "Spatial Intelligence", "Interactive GIS Thermal Mapping & Multi-Spectral Layers", "High-resolution microclimate choropleth mapping across city neighborhoods")

    gis_features = [
        {"title": "Multi-Spectral Layer Switcher", "desc": "Toggle seamlessly between Heat Severity, Satellite LST, Vegetation (NDVI), Impervious Surface, Population Density, Health Risk, and Before/After Simulation."},
        {"title": "Interactive Zone Inspection", "desc": "Click any grid polygon to instantly view localized surface temperature, canopy coverage, cooling access deficits, and physical infrastructure statistics."},
        {"title": "Dynamic City Auto-Centering", "desc": "Selecting any Indian metropolis automatically pans and zooms the interactive CARTO dark vector canvas to local neighborhood boundaries."},
        {"title": "Immediate Hotspot Quick-Jump", "desc": "Top municipal hotspot quick-jump pills allow city planners to navigate directly to critical thermal stress epicenters in 1-click."}
    ]

    for i, feat in enumerate(gis_features):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.9 + row * 2.5)
        create_card(s5, left, top, Inches(5.6), Inches(2.3))

        tbox = s5.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = feat["title"]
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = SKY_WHITE
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = feat["desc"]
        p1.font.size = Pt(11)
        p1.font.color.rgb = SKY_LIGHT

    # =========================================================================
    # SLIDE 6: 6-FACTOR CAUSE ATTRIBUTION ENGINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6, SKY_DEEP)
    add_header(s6, "Physical Explainability", "6-Factor Root Cause Attribution Engine (Sum to 100%)", "Answering WHY specific neighborhoods overheat using physical energy balance differentials")

    causes = [
        ("1. High Impervious Surface & Low Albedo", "Dark asphalt roads and bare rooftops absorb shortwave solar radiation and re-emit longwave thermal radiation.", "28% – 38%"),
        ("2. Vegetation Canopy Deficit", "Depleted tree canopy eliminates natural evapotranspiration and critical solar shading over pavements.", "22% – 32%"),
        ("3. Built Density & Thermal Mass", "Dense concrete structures with low sky-view factor trap heat and prevent convective airflow.", "14% – 20%"),
        ("4. Anthropogenic & Traffic Heat", "Dense vehicular traffic and split-unit air conditioning exhaust inject direct sensible heat.", "10% – 16%"),
        ("5. Elevation & Terrain Microclimate", "Low-lying inland valleys and wind-blocked corridors trap stagnant heated air masses.", "4% – 8%"),
        ("6. Historical Regional Baseline Deficit", "Compounding multi-day summer thermal inertia exceeding regional climate comfort baselines.", "4% – 8%")
    ]

    for i, (ctitle, cdesc, cshare) in enumerate(causes):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 3.95)
        top = Inches(1.9 + row * 2.55)
        create_card(s6, left, top, Inches(3.75), Inches(2.35))

        tbox = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(3.35), Inches(2.05))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = ctitle
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = SKY_WHITE
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = cdesc
        p1.font.size = Pt(10)
        p1.font.color.rgb = SKY_LIGHT
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = f"Typical Impact Share: {cshare}"
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = SKY_CYAN

    # =========================================================================
    # SLIDE 7: MULTI-VECTOR IMPACT MODELING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7, SKY_DEEP)
    add_header(s7, "Consequence Prediction", "Multi-Vector Impact Modeling: Energy, Water & Health", "Quantifying the exact price of inaction across three vital municipal sectors")

    impacts = [
        {
            "sector": "⚡ ENERGY & POWER GRID",
            "title": "HVAC Electricity Waste & Grid Strain",
            "points": [
                "Quantified with Cooling Degree Days (CDD) above 28°C baseline",
                "Temperature-Electricity Elasticity Curve modeling peak substation risks",
                "Monetized using local state electricity tariffs (₹/kWh)",
                "Calculates grid carbon emissions (Tonnes CO₂/year)"
            ],
            "color": ACCENT_AMBER
        },
        {
            "sector": "💧 WATER STRESS NEXUS",
            "title": "Heat-Induced Municipal Water Depletion",
            "points": [
                "Calculates millions of liters (ML/yr) of heat-driven surge demand",
                "Decomposes cooling HVAC, domestic hydration, and landscaping loss",
                "Water-Intervention Compatibility Matrix to prevent aquifer depletion",
                "Flags drought-stressed cities (e.g. Jaipur, Chennai, Ahmedabad)"
            ],
            "color": SKY_CYAN
        },
        {
            "sector": "🏥 HEAT-HEALTH VULNERABILITY",
            "title": "Epidemiological Risk Index (0-100)",
            "points": [
                "Evaluates elderly (>60y), child (<5y), and informal outdoor laborers",
                "Incorporates hospital accessibility distance and emergency transit time",
                "Tracks night-time thermal retention preventing physiological recovery",
                "Identifies critical emergency zones requiring misting & hydration shelters"
            ],
            "color": ACCENT_CORAL
        }
    ]

    for i, imp in enumerate(impacts):
        left = Inches(0.8 + i * 3.95)
        top = Inches(1.9)
        create_card(s7, left, top, Inches(3.75), Inches(4.9))

        tbox = s7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.35), Inches(4.5))
        tf = tbox.text_frame
        tf.word_wrap = True

        p_sec = tf.paragraphs[0]
        p_sec.text = imp["sector"]
        p_sec.font.size = Pt(11)
        p_sec.font.bold = True
        p_sec.font.color.rgb = imp["color"]
        p_sec.space_after = Pt(4)

        p_title = tf.add_paragraph()
        p_title.text = imp["title"]
        p_title.font.size = Pt(13)
        p_title.font.bold = True
        p_title.font.color.rgb = SKY_WHITE
        p_title.space_after = Pt(12)

        for pt in imp["points"]:
            p = tf.add_paragraph()
            p.text = f"• {pt}"
            p.font.size = Pt(10)
            p.font.color.rgb = SKY_LIGHT
            p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: 13 PROVEN COOLING INTERVENTIONS CATALOG
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8, SKY_DEEP)
    add_header(s8, "Solution Catalog", "13 Field-Calibrated Cooling Interventions", "Empirical cooling efficacy, unit costs, water footprints, and financial payback periods")

    catalog_samples = [
        ("High-Albedo Cool Roof Coating", "Cool Surface / Albedo", "₹110 / m²", "2.1°C – 2.8°C", "2.2 – 3.2 Years (Highest ROI)"),
        ("Native Urban Micro-Forests", "Nature-Based", "₹3,200 / tree", "2.4°C – 3.5°C", "Compounding Ecological Asset"),
        ("Reflective Pavement Sealants", "Cool Surface / Albedo", "₹185 / m²", "1.7°C – 2.4°C", "4.5 – 6.0 Years (Zero Water)"),
        ("Permeable Pervious Pavers", "Nature-Based", "₹750 / m²", "1.2°C – 1.9°C", "Aquifer Recharge Benefit"),
        ("Tensile Architectural Shade", "Architectural / Shade", "₹48,000 / unit", "3.5°C – 4.8°C", "Immediate Pedestrian Comfort"),
        ("Smart Solar Misting Shelters", "Emergency Response", "₹85,000 / unit", "4.0°C – 6.5°C", "Extreme Heat Wave Protection")
    ]

    for i, (name, cat, cost, cooling, payback) in enumerate(catalog_samples):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 3.95)
        top = Inches(1.9 + row * 2.55)
        create_card(s8, left, top, Inches(3.75), Inches(2.35))

        tbox = s8.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(3.35), Inches(2.05))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = name
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = SKY_WHITE
        p0.space_after = Pt(2)

        p_cat = tf.add_paragraph()
        p_cat.text = cat.upper()
        p_cat.font.size = Pt(9)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SKY_CYAN
        p_cat.space_after = Pt(6)

        p_stats = tf.add_paragraph()
        p_stats.text = f"Unit Cost: {cost}  |  ΔT: {cooling}\nPayback: {payback}"
        p_stats.font.size = Pt(10)
        p_stats.font.color.rgb = SKY_LIGHT

    # =========================================================================
    # SLIDE 9: THERMODYNAMIC BEFORE-VS-AFTER SIMULATOR
    # =========================================================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9, SKY_DEEP)
    add_header(s9, "Digital Twin Simulation", "Real-Time Thermodynamic Before vs After Simulator", "Interactive sliders enabling city planners to test microclimate interventions live")

    # Left Card: Sliders
    create_card(s9, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9))
    tbox_sl = s9.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.1), Inches(4.5))
    tf_sl = tbox_sl.text_frame
    tf_sl.word_wrap = True

    p0 = tf_sl.paragraphs[0]
    p0.text = "Interactive Intervention Sliders"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = SKY_WHITE
    p0.space_after = Pt(12)

    sliders = [
        ("Tree Canopy Expansion (+%)", "Adjust urban forestry density along streets and parks (0% → 50%)"),
        ("Cool Roof Deployment (%)", "Reflective elastomer coating on tin and concrete roofs (0% → 100%)"),
        ("Reflective Pavements (%)", "High-albedo sealants across parking lots and avenues (0% → 100%)"),
        ("Extensive Green Roofs (%)", "Drought-tolerant vegetative layers with drip systems (0% → 50%)"),
        ("Tensile Shade Structures (Units)", "High-UV fabric canopies over transit stops and markets (0 → 50 units)")
    ]

    for sname, sdesc in sliders:
        p = tf_sl.add_paragraph()
        p.text = f"🎛️ {sname}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SKY_CYAN
        p_sub = tf_sl.add_paragraph()
        p_sub.text = f"    {sdesc}"
        p_sub.font.size = Pt(10)
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_after = Pt(6)

    # Right Card: Instant Simulated Results
    create_card(s9, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9))
    tbox_res = s9.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.5))
    tf_res = tbox_res.text_frame
    tf_res.word_wrap = True

    p0 = tf_res.paragraphs[0]
    p0.text = "Instant Thermodynamic Physics Output"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_EMERALD
    p0.space_after = Pt(12)

    sim_metrics = [
        ("Surface Temperature Drop (ΔT)", "43.8°C → 40.6°C (-3.2°C Cooling)", ACCENT_EMERALD),
        ("HVAC Energy Reduction", "380,000 kWh/yr saved (16.4% reduction)", ACCENT_AMBER),
        ("Annual Financial Utility Savings", "₹31.2 Lakh / year direct bill savings", SKY_WHITE),
        ("Protected Population Exposure", "31,240 citizens shielded from severe heat", SKY_CYAN),
        ("Capital Investment & Payback", "₹78 Lakh capex with a 2.5-year ROI payback", SKY_LIGHT)
    ]

    for mtitle, mval, col in sim_metrics:
        p = tf_res.add_paragraph()
        p.text = f"✓ {mtitle}:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = SKY_WHITE
        p_val = tf_res.add_paragraph()
        p_val.text = f"    {mval}"
        p_val.font.size = Pt(11)
        p_val.font.color.rgb = col
        p_val.space_after = Pt(6)

    # =========================================================================
    # SLIDE 10: KNAPSACK MUNICIPAL BUDGET OPTIMIZER
    # =========================================================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10, SKY_DEEP)
    add_header(s10, "Capital Optimization", "Knapsack Algorithmic Budget Optimizer", "Maximizing cooling impact, energy relief, and saved lives under municipal financial limits")

    opt_features = [
        {
            "title": "Flexible Budget Scenarios",
            "desc": "Planners can select predefined budget packages (₹1 Cr, ₹2.5 Cr, ₹5 Cr, ₹10 Cr, ₹25 Cr) or enter custom capital constraints."
        },
        {
            "title": "Multi-Objective Strategies",
            "desc": "Choose between: Best Overall Balanced Impact, Maximum Temperature Drop, Max Population Protected, Max Energy Savings, or Max Health Protection."
        },
        {
            "title": "Itemized Portfolio Allocations",
            "desc": "The engine returns a deterministic zone-by-zone portfolio with exact intervention types, capex allocations, and unallocated contingency reserves."
        },
        {
            "title": "Quantified Resilience Shift",
            "desc": "City Resilience Score jumps (e.g. 54.2 → 88.5, +34.3 points) with total protected citizens, annual MWh saved, and avoided hospitalizations."
        }
    ]

    for i, opt in enumerate(opt_features):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.9 + row * 2.5)
        create_card(s10, left, top, Inches(5.6), Inches(2.3))

        tbox = s10.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.1), Inches(1.9))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = opt["title"]
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = SKY_WHITE
        p0.space_after = Pt(6)

        p1 = tf.add_paragraph()
        p1.text = opt["desc"]
        p1.font.size = Pt(11)
        p1.font.color.rgb = SKY_LIGHT

    # =========================================================================
    # SLIDE 11: MULTI-CITY BENCHMARK & GROUNDED AI ASSISTANT
    # =========================================================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11, SKY_DEEP)
    add_header(s11, "Advanced Intelligence", "Multi-City Benchmarking & Grounded AI Assistant", "Cross-metropolitan comparisons and natural language decision support without hallucinations")

    # Left: Multi-City Benchmarking
    create_card(s11, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.9))
    tbox_m = s11.shapes.add_textbox(Inches(1.05), Inches(2.1), Inches(5.1), Inches(4.5))
    tf_m = tbox_m.text_frame
    tf_m.word_wrap = True

    p0 = tf_m.paragraphs[0]
    p0.text = "Side-by-Side Multi-City Benchmark"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = SKY_CYAN
    p0.space_after = Pt(10)

    b_pts = [
        ("2 to 4 City Selection", "Select and compare any Indian cities simultaneously on thermal distress, water stress, and resilience."),
        ("Comparative Bar & Radar Visuals", "Direct visualization of temperature deltas, annual cooling power loss (GWh), and capital investment needs."),
        ("Data-Grounded AI Synthesis", "Automated narrative synthesizing regional climate divergence, water constraints, and policy recommendations.")
    ]
    for btitle, btext in b_pts:
        p = tf_m.add_paragraph()
        p.text = f"📊 {btitle}: {btext}"
        p.font.size = Pt(11)
        p.font.color.rgb = SKY_LIGHT
        p.space_after = Pt(8)

    # Right: Grounded AI Assistant
    create_card(s11, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.9))
    tbox_ai = s11.shapes.add_textbox(Inches(7.05), Inches(2.1), Inches(5.2), Inches(4.5))
    tf_ai = tbox_ai.text_frame
    tf_ai.word_wrap = True

    p0 = tf_ai.paragraphs[0]
    p0.text = "Grounded Natural Language Assistant"
    p0.font.size = Pt(16)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_AMBER
    p0.space_after = Pt(10)

    ai_pts = [
        ("100% Data-Grounded", "Formulates answers strictly from computed spatial grids, tariffs, and physics equations—zero hallucinated numbers."),
        ("Zone Comparison Queries", "Ask 'Why is Zone A-17 hotter than Zone N-09?' to get exact temperature, albedo, and canopy differentials."),
        ("Budget Allocation Queries", "Ask 'How should we spend ₹5 Crore?' to receive structured intervention portfolios and ROI breakdowns."),
        ("Clickable Zone References", "Every mentioned zone in AI answers includes clickable pills navigating directly to physical cause deep-dives.")
    ]
    for atitle, atext in ai_pts:
        p = tf_ai.add_paragraph()
        p.text = f"🤖 {atitle}: {atext}"
        p.font.size = Pt(11)
        p.font.color.rgb = SKY_LIGHT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: IMPACT SUMMARY & VISION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12, SKY_DEEP)
    add_header(s12, "Impact & Vision", "KAIROS: Transforming Urban Heat Resilience Across India", "From reactive disaster relief to proactive, scientific municipal climate investment")

    summary_cards = [
        {"num": "13", "label": "Dedicated Pages", "desc": "From GIS heat maps and 6-factor causes to Knapsack budget optimization and AI decision assistant."},
        {"num": "36", "label": "States & UTs", "desc": "Pan-India coverage supporting pre-calibrated major metros and dynamic modeled town searches."},
        {"num": "100%", "label": "Explainable Physics", "desc": "Deterministic 6-factor cause attribution and degree-day energy models with zero fabricated outputs."},
        {"num": "3.5x", "label": "Cooling ROI", "desc": "High-albedo cool roofs and optimized shading portfolios deliver rapid 2.2–3.2 year financial payback."}
    ]

    for i, sc in enumerate(summary_cards):
        left = Inches(0.8 + i * 2.95)
        top = Inches(1.9)
        create_card(s12, left, top, Inches(2.75), Inches(3.2))

        tbox = s12.shapes.add_textbox(left + Inches(0.15), top + Inches(0.2), Inches(2.45), Inches(2.8))
        tf = tbox.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = sc["num"]
        p0.font.size = Pt(36)
        p0.font.bold = True
        p0.font.color.rgb = SKY_CYAN
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = sc["label"]
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = SKY_WHITE
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = sc["desc"]
        p2.font.size = Pt(10)
        p2.font.color.rgb = SKY_LIGHT

    # Bottom Callout Banner
    create_card(s12, Inches(0.8), Inches(5.35), Inches(11.7), Inches(1.45), bg_color=SKY_NAVY, border_color=SKY_BLUE)
    tbox_bot = s12.shapes.add_textbox(Inches(1.05), Inches(5.45), Inches(11.2), Inches(1.25))
    tf_bot = tbox_bot.text_frame
    tf_bot.word_wrap = True

    p_bot0 = tf_bot.paragraphs[0]
    p_bot0.text = "KAIROS — DECISION INTELLIGENCE FOR CLIMATE-RESILIENT CITIES"
    p_bot0.font.size = Pt(13)
    p_bot0.font.bold = True
    p_bot0.font.color.rgb = SKY_CYAN
    p_bot0.space_after = Pt(4)

    p_bot1 = tf_bot.add_paragraph()
    p_bot1.text = "Enabling municipal corporations, state disaster management authorities, and smart city missions across India to deploy cooling capital with maximum scientific efficacy and public health protection."
    p_bot1.font.size = Pt(11)
    p_bot1.font.color.rgb = SKY_WHITE

    # Save presentation
    output_path = "/Users/rickyvinod/kairos/KAIROS_Urban_Heat_Intelligence.pptx"
    prs.save(output_path)
    print(f"✓ Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()
