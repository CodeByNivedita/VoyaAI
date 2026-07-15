import streamlit as st
import textwrap
from pathlib import Path
from services.budget_engine import estimate_budget
from services.current_budget import get_current_budget


def load_css():
    css_path = Path("frontend/style.css")

    if css_path.exists():
        with open(css_path) as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )


# ==========================================================
# REUSABLE COMPONENTS
# ==========================================================

def section_title(title, subtitle=""):
    st.markdown(
        f"""
        <div class="section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title, value, icon="✨"):
    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-icon">{icon}</div>
            <div class="info-value">{value}</div>
            <div class="info-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def dashboard_card(title, icon, color="#3B82F6"):

    st.markdown(
        f"""
        <div style="
            background:#162033;
            border-left:6px solid {color};
            padding:18px;
            border-radius:18px;
            margin-bottom:15px;
        ">
            <h3 style="margin:0;color:white;">
                {icon} {title}
            </h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ==========================================================
# NAVBAR
# ==========================================================

from PIL import Image
import streamlit as st



def render_navbar():

    col1, col2, col3 = st.columns([1,5,2])

    with col1:
        st.image("assets/logo.png", width=80)

    with col2:

        st.title("VoyaAI")

        st.caption("Your AI Travel Companion")

    with col3:

        st.markdown(
            "### 🇮🇳 India",
        )

    st.divider()
# ==========================================================
# HERO
# ==========================================================


def render_hero():

    # Hero Badge
    st.markdown(
        """
<div class="hero-badge">
✨ AI Powered Travel Planner
</div>
""",
        unsafe_allow_html=True,
    )

    # Title
    st.markdown(
        """
<h1 style="
text-align:center;
font-size:58px;
font-weight:700;
margin-top:15px;
margin-bottom:10px;
color:white;
">
🌍 Discover Incredible <span style="color:#3B82F6;">India</span>
</h1>
""",
        unsafe_allow_html=True,
    )

    # Subtitle
    st.markdown(
        """
<p style="
text-align:center;
font-size:20px;
color:#CBD5E1;
max-width:750px;
margin:auto;
margin-bottom:40px;
line-height:1.8;
">
Create personalized itineraries, discover attractions,
estimate budgets and plan unforgettable journeys with AI.
</p>
""",
        unsafe_allow_html=True,
    )

    # =============================
    # INPUTS
    # =============================

    c1, c2 = st.columns(2)

    with c1:
        departure_city = st.text_input(
            "🚩 Departure City",
            placeholder="Lucknow"
    )

    with c2:
        destination = st.text_input(
        "📍 Destination",
        placeholder="Manali"
        )

    c3, c4,c5 = st.columns(3)

    with c3:
        days = st.number_input(
        "🗓 Days",
        min_value=1,
        value=3,
    )

    with c4:
        travelers = st.number_input(
            "👥 Travelers",
            min_value=1,
            value=2,
        )

    with c5:
        budget = st.number_input(
            "💰 Budget",
            min_value=1000,
            step=1000,
            value=10000,
        )
    c6, c7 = st.columns(2)

    with c6:

      trip_type = st.selectbox(
        "🔁 Trip Type",
        [
            "Round Trip",
            "One Way",
        ],
    )

    with c7:

     travel_class = st.selectbox(
        "💺 Travel Class",
        [
            "Economy",
            "Business",
        ],
    )


    st.write("")

    generate = st.button(
        "✨ Generate AI Itinerary",
        use_container_width=True,
        type="primary",
    )

    st.write("")
    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        info_card("Cities", "100+", "📍")

    with c2:
        info_card("Hotels", "1000+", "🏨")

    with c3:
        info_card("Attractions", "500+", "🎯")

    with c4:
        info_card("AI Planning", "<5 sec", "🤖")

    if generate:

        if destination.strip() == "":
            st.warning("Please enter a destination.")
            return None

        return f"""
Departure City: {departure_city}

Destination: {destination}

Days: {days}

Travelers: {travelers}

Budget: ₹{budget}

Trip Type: {trip_type}

Travel Class: {travel_class}

Generate a complete personalized itinerary including hotels,
weather, attractions, budget and a day-wise plan.
"""
# ==========================================================
# LOADING
# ==========================================================
import streamlit as st

def render_loading():

    st.markdown(
        """
        <div class="loading-card">

        🤖 AI is planning your journey...

        </div>
        """,
        unsafe_allow_html=True,
    )



def render_trip_banner(data):

    dashboard = data["dashboard"]
    travel = dashboard["travel"]
    images = dashboard.get("images", [])

    observations = data.get("observations", {})

    weather = observations.get("weather")
    route = observations.get("route")
    budget = observations.get("budget")

    # ==================================================
    # HERO IMAGE
    # ==================================================

    if images:
        st.image(
            images[0]["regular"],
            width="stretch",
        )

    # ==================================================
    # TRIP SUMMARY
    # ==================================================

    st.title(f"📍 {travel.destination}")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📅 Days",
            travel.number_of_days,
        )

    with c2:
        st.metric(
            "👥 Travelers",
            travel.number_of_travelers,
        )

    with c3:
        st.metric(
            "💰 Budget",
            f"₹{travel.budget:,}",
        )

    # ==================================================
    # DESTINATION GALLERY
    # ==================================================

    if len(images) > 1:

        st.markdown("## 📸 Destination Gallery")

        gallery = images[1:5]

        cols = st.columns(len(gallery))

        for col, img in zip(cols, gallery):

            with col:

                st.image(
                    img["regular"],
                    width="stretch",
                )

        st.caption(
            f"📷 Photos by {images[0]['photographer']} via Unsplash"
        )

    st.divider()
        
def render_dashboard(data):

    observations = data.get("observations", {})

    weather = observations.get("weather")
    budget = observations.get("budget")
    hotels = observations.get("hotels", [])
    attractions = observations.get("attractions", [])
    itinerary = observations.get("itinerary")
    route = observations.get("route")
    

    tab1, tab2, tab3,= st.tabs(
        [
            
            "🏨 Hotels",
            "⭐ Attractions",
            "🗓 Itinerary",
        ]
    )

    

    # ==================================================
    # HOTELS
    # ==================================================

    with tab1:

        render_hotels(hotels)

    # ==================================================
    # ATTRACTIONS
    # ==================================================

    with tab2:

        render_attractions(attractions)

    # ==================================================
    # ITINERARY
    # ==================================================

    with tab3:

        render_itinerary(itinerary)


def render_weather(weather):

    if not weather:
        st.warning("Weather information not available.")
        return

    st.markdown("## 🌤 Current Weather")

    c1, c2 = st.columns([1.2, 1])

    with c1:

        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#2563EB,#38BDF8);
            padding:28px;
            border-radius:22px;
            color:white;
            box-shadow:0 10px 30px rgba(37,99,235,.25);
        ">

        <div style="font-size:22px;font-weight:600;">
            📍 {weather['city']}
        </div>

        <div style="
            font-size:64px;
            font-weight:800;
            margin-top:12px;
            ">
            {weather['temperature']}°C
        </div>

        <div style="
            font-size:22px;
            margin-top:8px;
            ">
            {weather['condition']}
        </div>

        <div style="
            opacity:.9;
            margin-top:8px;
            ">
            {weather['description'].title()}
        </div>

        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.metric(
            "Feels Like",
            f"{weather['feels_like']}°C"
        )

        st.metric(
            "Humidity",
            f"{weather['humidity']}%"
        )

        st.metric(
            "Wind Speed",
            f"{weather['wind_speed']} m/s"
        )

def get_best_transport(route, budget):

    options = route["travel_options"]

    recommendations = []

    for mode, details in options.items():

        score = 0

        # Cheap gets more score
        score += max(0, 5000 - details["fare"]) / 100

        # Faster gets more score
        score += max(0, 20 - details["duration"]) * 2

        # Fits budget
        if details["fare"] <= budget:
            score += 20

        recommendations.append(
            {
                "mode": mode,
                "fare": details["fare"],
                "duration": details["duration"],
                "score": score,
            }
        )

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[0]

def render_journey(route, travel):

    st.markdown("## 🚩 Journey Planner")

    best = get_best_transport(route, travel.budget)

    st.success(
        f"""
⭐ **AI Recommendation**

🚆 **{best['mode']}**

💰 Fare : ₹{best['fare']:,}

⏱ Travel Time : {best['duration']} hrs

✔ Best balance of cost and travel time.
"""
    )

    st.markdown(
        f"""
### 📍 {route['departure']}

⬇️

### 🏔 {route['destination']}

**Distance : {route['distance']} km**
"""
    )

    options = route["travel_options"]

    default_mode = best["mode"]

    if default_mode not in options:
      default_mode = next(iter(options))

    if "selected_transport" not in st.session_state:
      st.session_state.selected_transport = default_mode

    cols = st.columns(len(options))

    icons = {
        "Car": "🚗",
        "Bus": "🚌",
        "Train": "🚆",
        "Flight": "✈️",
    }

    for col, (mode, details) in zip(cols, options.items()):

        with col:

            selected = (
                st.session_state.selected_transport == mode
            )

            border = "#2563EB" if selected else "#374151"
            bg = "#172554" if selected else "#111827"

            st.markdown(
                f"""
<div style="
background:{bg};
border:2px solid {border};
border-radius:18px;
padding:18px;
text-align:center;
min-height:240px;
">

<h2>{icons.get(mode,'🚘')}</h2>

<h3>{mode}</h3>

<h2 style="color:#34D399;">
₹{details['fare']:,}
</h2>

<p>
⏱ {details['duration']} hrs
</p>

</div>
""",
                unsafe_allow_html=True,
            )

            if selected:

                st.success("✔ Selected")

            else:

                if st.button(
                    "Select",
                    key=f"transport_{mode}",
                    use_container_width=True,
                ):

                    st.session_state.selected_transport = mode
                    st.rerun()

def render_gallery(images):

    if not images:
        return

    st.markdown("## 📸 Destination Gallery")

    # Hero Image
    st.image(
    images[0]["regular"],
    width="stretch",
)

    # Two additional images
    col1, col2 = st.columns(2)

    if len(images) > 1:
        with col1:
            st.image(images[1]["regular"], width="stretch")

    if len(images) > 2:
        with col2:
            st.image(images[2]["regular"], width="stretch")

    st.caption(
        f"📷 Photos by {images[0]['photographer']} via Unsplash"
    )


def render_itinerary(itinerary):

    if not itinerary:
        st.info("No itinerary available.")
        return

    st.markdown("## 🗓 Your Travel Plan")

    for day in itinerary:

        # Support both dict and Pydantic object
        if isinstance(day, dict):
            day_no = day.get("day")
            morning = day.get("morning")
            afternoon = day.get("afternoon")
            evening = day.get("evening")
            cost = day.get("estimated_cost")
        else:
            day_no = day.day
            morning = day.morning
            afternoon = day.afternoon
            evening = day.evening
            cost = day.estimated_cost

        st.markdown(
            f"""
<div style="
background:#111827;
border:1px solid #374151;
border-radius:22px;
padding:24px;
margin-bottom:25px;
">

<h2 style="
color:#60A5FA;
margin-bottom:20px;
">
📅 Day {day_no}
</h2>

<h4>🌅 Morning</h4>
<p>{morning}</p>

<h4>☀ Afternoon</h4>
<p>{afternoon}</p>

<h4>🌆 Evening</h4>
<p>{evening}</p>

<hr>

<h3 style="color:#34D399;">
💰 Estimated Cost : ₹{cost}
</h3>

</div>
""",
            unsafe_allow_html=True,
        )

def render_footer():

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer">

        Built with ❤️ using LangGraph + Gemini + Streamlit

        </div>
        """,
        unsafe_allow_html=True,
    )

def render_trip_summary(summary):

    st.markdown("## 📍 Trip Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        info_card(
            "Destination",
            summary["destination"],
            "📍"
        )

    with c2:
        info_card(
            "Duration",
            summary["duration"],
            "📅"
        )

    with c3:
        info_card(
            "Budget",
            summary["budget"],
            "💰"
        )

    with c4:
        info_card(
            "Weather",
            summary["weather"],
            "🌤"
        )

    st.write("")



def render_attractions(attractions):

    if not attractions:
        st.info("No attractions found.")
        return

    st.markdown("## ⭐ Must Visit Places")

    cols = st.columns(2)

    for i, place in enumerate(attractions):

        with cols[i % 2]:

            st.markdown(f"""
            <div style="
                background:#111827;
                border:1px solid #374151;
                border-radius:20px;
                padding:22px;
                margin-bottom:20px;
                min-height:260px;
            ">

            <h3 style="
                color:white;
                margin-bottom:12px;
            ">
                📍 {place["name"]}
            </h3>

            <p style="color:#FBBF24;">
                ⭐ {place["rating"]} / 5
            </p>

            <p style="color:#D1D5DB;">
                🏷 Type :
                <b>{place["type"]}</b>
            </p>

            <p style="color:#D1D5DB;">
                🎫 Entry Fee :
                <b>₹{place["entry_fee"]}</b>
            </p>

            <p style="color:#D1D5DB;">
                ⏱ Time Needed :
                <b>{place["time_needed"]} hrs</b>
            </p>

            <p style="color:#D1D5DB;">
                🌸 Best Time :
                <b>{place["best_time"]}</b>
            </p>

            <hr>

            <p style="
                color:#9CA3AF;
                font-size:14px;
            ">
                {place["significance"]}
            </p>

            </div>
            """, unsafe_allow_html=True)

def render_hotels(hotels):

    if not hotels:
        st.info("No hotels found.")
        return

    # ---------------------------------
    # Default Selected Hotel
    # ---------------------------------

    if "selected_hotel" not in st.session_state:
        st.session_state.selected_hotel = hotels[0]

    st.markdown("## 🏨 Recommended Hotels")

    cols = st.columns(2)

    for i, hotel in enumerate(hotels):

        with cols[i % 2]:

            selected = (
                st.session_state.selected_hotel["name"]
                == hotel["name"]
            )

            border = "#2563EB" if selected else "#374151"
            bg = "#172554" if selected else "#111827"

            st.markdown(
                f"""
<div style="
background:{bg};
border:2px solid {border};
border-radius:20px;
padding:22px;
margin-bottom:20px;
min-height:270px;
">

<div style="
font-size:22px;
font-weight:700;
color:white;
margin-bottom:10px;
">
🏨 {hotel["name"]}
</div>

<span style="
background:#2563EB;
color:white;
padding:6px 12px;
border-radius:15px;
font-size:14px;
">
{hotel["category"]}
</span>

<br><br>

<p style="color:#D1D5DB;">
💰 <b>₹{hotel['price_per_night']:,}</b> / Night
</p>

<p style="color:#D1D5DB;">
📍 {hotel["address"]}
</p>

<p style="color:#D1D5DB;">
🛏 Total Rooms :
<b>{hotel["rooms"]}</b>
</p>

</div>
""",
                unsafe_allow_html=True,
            )

            if selected:

                st.success("✔ Selected")

            else:

                if st.button(
                    "Select",
                    key=f"hotel_{i}",
                    use_container_width=True,
                ):

                    st.session_state.selected_hotel = hotel
                    st.rerun()


import streamlit as st


def render_budget(budget, route, travel):

    selected_transport = st.session_state.get(
    "selected_transport",
    "Car",
)

    selected_hotel = st.session_state.get(
    "selected_hotel",
)

    budget = get_current_budget(
    travel,
    route,
    selected_transport,
    selected_hotel,
)

    if not budget:
        st.warning("Budget information not available.")
        return

    
    
    fare_per_person = route["travel_options"][selected_transport]["fare"]

    
    # ---------------------------------
    # Budget Header
    # ---------------------------------

    st.markdown("## 💰 Budget Breakdown")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "🏨 Hotel",
            f"₹{budget['hotel_budget']:,}"
        )

        st.metric(
            "🍽 Food",
            f"₹{budget['food_budget']:,}"
        )

        st.metric(
            "🚕 Transport",
            f"₹{budget['transport_budget']:,}"
        )

    with c2:

        st.metric(
            "🎯 Activities",
            f"₹{budget['activities_budget']:,}"
        )

        st.metric(
            "🛍 Misc",
            f"₹{budget['misc_budget']:,}"
        )

        st.metric(
            "📅 Daily",
            f"₹{budget['daily_budget']:,}"
        )

    st.divider()

    st.success(
        f"₹{budget['total_budget']:,}"
    )

    # ---------------------------------
    # Transport Calculation
    # ---------------------------------

    st.info(
        f"""
### 🚕 Transport Cost

**{selected_transport}**

₹{fare_per_person:,} × {travel.number_of_travelers} Traveler(s)

× {budget["trip_multiplier"]} ({travel.trip_type})

= **₹{budget["transport_budget"]:,}**
"""
    )

    # ---------------------------------
    # Budget Comparison
    # ---------------------------------

    difference = budget["difference"]

    if difference >= 0:

        st.success(
            f"""
🟢 Within Budget

You still have **₹{difference:,}** remaining.
"""
        )

    else:

        st.error(
            f"""
🔴 Over Budget

You need **₹{-difference:,}** more.
"""
        )
def render_foods(foods):

    st.markdown("## 🍽 Local Food")

    cols = st.columns(3)

    for i, food in enumerate(foods):

        cols[i % 3].success(food)

def render_packing(items):

    st.markdown("## 🎒 Packing Checklist")

    for item in items:

        st.checkbox(item, value=True)


def render_tips(tips):

    st.markdown("## 💡 Travel Tips")

    for tip in tips:

        st.info(tip)