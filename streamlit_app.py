import streamlit as st
import json
from typing import Dict, Any, List
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
import os
import re



os.environ["DEEPSEEK_API_KEY"] = "sk-2e541143af014ebf8f70681786bf2ca2"
os.environ["OPENAI_API_KEY"] = "sk-2e541143af014ebf8f70681786bf2ca2"



# Reuse the existing logic and agents by importing from api.py
# Note: api.py is written as a script, but we only need the definitions (agents, helper funcs, constants)
# We'll defensively import the symbols we need and avoid executing the CLI loop in api.py by guarding usage here.


available_categories = [
    {"id": 1, "name": "Revenue"},
    {"id": 2, "name": "Revenue & Sales"},
    {"id": 3, "name": "Capital Expenditure"}
]

def create_assumptions_payload(
    collected_data: Dict[str, Any], 
    organisation_id: int, 
    forecast_measure_id: int,
    categories: List[Dict[str, Any]] = None
) -> List[Dict]:
    """
    Create multiple API payloads from collected data - one for each driver
    
    Args:
        collected_data: Dictionary containing assumption data
        organisation_id: Organization ID for the payload
        forecast_measure_id: Forecast measure ID for the payload
        categories: List of category objects with 'id' and 'name' keys
    """
    
    payloads = []
    
    # Get all drivers or use Assumption_name as a single driver
    drivers = []
    if "Drivers" in collected_data and isinstance(collected_data["Drivers"], list) and len(collected_data["Drivers"]) > 0:
        drivers = collected_data["Drivers"]
    else:
        drivers = [collected_data.get("Assumption_name", "")]
    
    # Handle category logic
    category_name = collected_data.get("Category", "")
    category_id = None
    is_new_category = False
    
    # Check if categories list is provided and not empty
    if categories and isinstance(categories, list) and len(categories) > 0:
        # Find if the category exists in the provided list
        matching_category = next(
            (cat for cat in categories 
             if cat.get("name", "").lower() == category_name.lower()), 
            None
        )
        
        if matching_category:
            # Category exists - use ID and set is_new to False
            category_id = matching_category.get("id")
            is_new_category = False
        else:
            # Category doesn't exist - set is_new to True and use name
            is_new_category = True
    else:
        # No categories provided - treat as new category
        is_new_category = True
    
    # Create a payload for each driver
    for driver in drivers:
        payload = {
            "organisation_id": organisation_id,
            "forecast_measure_id": forecast_measure_id,
            "name": driver,  # Use the driver name
            "account_name": driver,  # Use the driver name
            "aggregation": collected_data.get("Aggregation", "sum"),
            "balance_sheet": False,
            "category_id": category_id,
            "category_name": category_name,
            "comment": "",
            "data": [
                {"date": "01-03-2026", "backendDateFormat": "31-03-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-04-2026", "backendDateFormat": "30-04-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-05-2026", "backendDateFormat": "31-05-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-06-2026", "backendDateFormat": "30-06-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-07-2026", "backendDateFormat": "31-07-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-08-2026", "backendDateFormat": "31-08-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-09-2026", "backendDateFormat": "30-09-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-10-2026", "backendDateFormat": "31-10-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-11-2026", "backendDateFormat": "30-11-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-12-2026", "backendDateFormat": "31-12-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-01-2027", "backendDateFormat": "31-01-2027", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-02-2027", "backendDateFormat": "28-02-2027", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True}
            ],
            "is_new": is_new_category,
            "is_percentage": False,
            "measure_unit": "",
            "notes": "",
            "order": -1,
            "profit_and_loss": False,
            "type": "assumption",
            "values": [
                {"date": "01-03-2026", "backendDateFormat": "31-03-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-04-2026", "backendDateFormat": "30-04-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-05-2026", "backendDateFormat": "31-05-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-06-2026", "backendDateFormat": "30-06-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-07-2026", "backendDateFormat": "31-07-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-08-2026", "backendDateFormat": "31-08-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-09-2026", "backendDateFormat": "30-09-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-10-2026", "backendDateFormat": "31-10-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-11-2026", "backendDateFormat": "30-11-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operad": None, "readonly": True},
                {"date": "01-12-2026", "backendDateFormat": "31-12-2026", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-01-2027", "backendDateFormat": "31-01-2027", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True},
                {"date": "01-02-2027", "backendDateFormat": "28-02-2027", "amount": 0, "methodology": 3, "methodology_data": "Manual input", "isChecked": False, "isEdited": False, "is_actual": False, "linked_operand": None, "readonly": True}
            ]
        }
        payloads.append(payload)
    
    return payloads



REQUIRED_FIELDS = [ "Category", "Aggregation", "Drivers"]


def check_completion_trigger(user_input):
    """Check if user indicates they're done providing details"""
    input_lower = user_input.lower()
    for pattern in COMPLETION_TRIGGERS:
        if re.search(pattern, input_lower):
            return True
    return False

def detect_sophistication_level(user_input):
    """Detect if user wants basic or detailed approach"""
    input_lower = user_input.lower()
    detailed_keywords = ["detailed", "comprehensive", "granular", "thorough", "in-depth", "deep", "deeper"]
    basic_keywords = ["basic", "simple", "quick", "high-level", "overview"]

    for keyword in detailed_keywords:
        if keyword in input_lower:
            return "detailed"
    for keyword in basic_keywords:
        if keyword in input_lower:
            return "basic"
    return None

def extract_key_metrics_from_conversation():
    """Extract key metrics mentioned in the conversation"""
    metrics = []
    # Use Streamlit session state's conversation history to ensure context is preserved
    history = st.session_state.get("conversation_history", [])
    for message in history:
        content = message["content"].lower()
        # Look for metric mentions
        if any(term in content for term in ["user", "subscriber", "revenue", "watch", "engagement", "retention", "churn"]):
            # Extract potential metrics
            if "active user" in content or "mau" in content:
                metrics.append("Monthly Active Users")
            if "sign-up" in content or "subscriber" in content:
                metrics.append("New Subscribers")
            if "watch time" in content or "engagement" in content:
                metrics.append("Watch Time")
            if "revenue" in content:
                metrics.append("Revenue")
            if "retention" in content or "churn" in content:
                metrics.append("Retention Rate")

    return list(set(metrics))  # Remove duplicates

AVAILABLE_CATEGORIES = [
    "Revenue",
    "Expenses",
    "Cost of Goods Sold",
    "Operating Costs",
    "Marketing Spend",
    "Customer Acquisition",
    "Churn & Retention",
    "Headcount",
    "Production Volume",
    "Inventory",
    "Pricing",
    "Sales Pipeline",
    "Customer Support",
    "Content Performance",
    "Cash Flow"
]

conversation_history = []


# ---- Enhanced Trigger Detection ----
COMPLETION_TRIGGERS = [
    r"(that'?s all|that should do it|i think that'?s it)",
    r"(ready to move on|let'?s proceed|continue|next)",
    r"(sounds good|looks good|that works)",
    r"(i'?m done|finished|complete)",
    r"(go ahead|proceed|move forward)",
    r"(move to (?:retention|revenue|content|another area))",
    r"(let'?s move (?:on|to|forward))"
]

# ---- Agents ----
Assumption_agent = Agent(
    name="Forecast Assumption Agent",
    role="Conversational guide for building forecasting assumptions.",
    model=DeepSeek(),
    instructions=[
        "You are Dash, a friendly and engaging forecasting assistant modelling monthly revenue.",
        "Your goal is to gather just enough information to create useful forecasting assumptions.",
        "Use a warm, conversational tone — feel human, not scripted.",
        "Vary your wording so questions don't sound repetitive (mix casual and formal phrasings).",
        "Skip questions if the user already provided enough information.",
        "Acknowledge off-topic inputs briefly, then gently guide user back to the goal.",
        "Summarize what you've learned every 2-3 messages to keep context clear.",
        "When you have enough detail, naturally transition to suggesting key drivers or confirming assumptions."
    ]
)



Suggestion_agent = Agent(
    name="Suggestion Agent",
    role="Analyzes conversation history to extract assumption parameters and drivers.",
    model=DeepSeek(),
    instructions=[
        "Analyze the complete conversation history to identify what was actually discussed.",
        "Create a professional, descriptive assumption name based ONLY on the business context discussed.",
        "DO NOT invent metrics or values that weren't mentioned in the conversation.",
        "Assign a relevant Category based on the topics discussed.",
        "Category MUST be plain text and should NOT include any special characters like &, %, @, # etc.",
        "Infer the optimal Aggregation method based on the types of metrics mentioned, Aggregation can only be Sum, Average or Closing Balance. So choose between them.",
        "Extract all business drivers explicitly mentioned in the conversation AND suggest additional relevant drivers based on context (but avoid unrelated or invented ones).",
        "Suggested drivers must make logical sense for the industry and business focus discussed.",
        "Prefer broad, meaningful drivers (e.g., 'Marketing Spend', 'Customer Acquisition Rate') rather than overly specific or fabricated metrics.",
        "Output explicit and suggested drivers together as a single array, marking suggested drivers with '(suggested)'."
        "DO NOT add drivers that weren't mentioned - only include what was actually discussed.",
        "If no specific drivers were mentioned, return an empty array for drivers.",
        "Format output as VALID JSON with: assumption_name, category, aggregation, drivers (as an array).",
        "Ensure the JSON is properly formatted and can be parsed without errors."
    ]
)

Confirmation_agent = Agent(
    name="Confirmation Agent",
    role="Handles user confirmation and modification requests for suggested assumptions.",
    model=DeepSeek(),
    instructions=[
        "Interpret user responses to suggested assumptions.",
        "Detect if user wants to confirm, modify, or reject suggestions.",
        "For modifications, identify which field(s) need changing.",
        "Extract new values from user input when provided.",
        "SPECIAL HANDLING FOR DRIVERS:",
        "- If user says 'add more drivers', 'more drivers', 'include [specific driver]', understand they want to ADD to existing drivers",
        "- If user says 'remove [driver]', 'delete [driver]', understand they want to REMOVE specific drivers", 
        "- If user suggests specific drivers, extract them and add to existing list",
        "- If user asks for 'more relevant drivers', suggest additional context-appropriate drivers",
        "For dairy farming milk production, suggest drivers like: Feed quality and availability, Animal health and veterinary care, Breeding and calving cycles, Milking equipment efficiency, Labor availability, Weather conditions, Water availability, Milk quality standards, Regulatory compliance, Market demand fluctuations",
        "For drivers modifications, output intent: 'add_drivers', 'remove_drivers', or 'replace_drivers'",
        "For non-drivers field changes, output intent: 'change'",
        "For confirmation, output intent: 'confirm'",
        "Output JSON with: intent, target_field, new_value (if provided), drivers_to_add (array), drivers_to_remove (array).",
        "Example response for 'add more drivers': {'intent': 'add_drivers', 'drivers_to_add': ['Feed quality', 'Animal health']}",
        "Example response for 'looks good': {'intent': 'confirm'}"
    ]
)

st.set_page_config(page_title="Forecast Assumption Agent", page_icon="🤖", layout="wide")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history: List[Dict[str, str]] = []
if "context_data" not in st.session_state:
    st.session_state.context_data: Dict[str, Any] = {
        "industry": None,
        "business_focus": None,
        "sophistication_level": "basic",
        "tracked_metrics": [],
        "key_metrics_discussed": [],
        "additional_details": {},
    }
if "current_phase" not in st.session_state:
    st.session_state.current_phase = "industry"
if "detailed_mode" not in st.session_state:
    st.session_state.detailed_mode = False
if "detailed_depth" not in st.session_state:
    st.session_state.detailed_depth = 0
if "sufficient_detail" not in st.session_state:
    st.session_state.sufficient_detail = False
if "user_selected_category" not in st.session_state:
    st.session_state.user_selected_category = None
if "collected_data" not in st.session_state:
    st.session_state.collected_data: Dict[str, Any] = {}
if "max_detailed_depth" not in st.session_state:
    st.session_state.max_detailed_depth = 3

st.title("🤖 Dash — Forecast Assumption Agent")
st.caption("Chat to define assumptions, choose a category, confirm, and get API payloads.")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    reset = st.button("Reset Conversation", use_container_width=True)
    if reset:
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Helper to run the assumption agent with current context
def run_assumption_agent() -> str:
    prompt_context = {
        "current_phase": st.session_state.current_phase,
        "context_data": st.session_state.context_data,
        "conversation_history": st.session_state.conversation_history[-6:],
        "detailed_mode": st.session_state.detailed_mode,
        "detailed_depth": st.session_state.detailed_depth,
    }
    resp = Assumption_agent.run(json.dumps(prompt_context, indent=2))
    return getattr(resp, "content", str(resp))

# Chat UI
chat = st.container()
with chat:
    for message in st.session_state.conversation_history:
        if message["role"] == "agent":
            st.chat_message("assistant").markdown(message["content"]) 
        else:
            st.chat_message("user").markdown(message["content"]) 

    # Generate an agent message for the current phase if needed
    if not st.session_state.sufficient_detail and (len(st.session_state.conversation_history) == 0 or st.session_state.conversation_history[-1]["role"] == "user"):
        agent_text = run_assumption_agent()
        st.session_state.conversation_history.append({"role": "agent", "content": agent_text})
        st.chat_message("assistant").markdown(agent_text)

    user_text = st.chat_input("Type your reply…")
    if user_text:
        st.session_state.conversation_history.append({"role": "user", "content": user_text})
        # Completion trigger
        if check_completion_trigger(user_text):
            st.session_state.sufficient_detail = True
        # Phase transitions
        if st.session_state.current_phase == "industry" and not st.session_state.context_data["industry"]:
            lower = user_text.lower()
            if "saas" in lower:
                st.session_state.context_data["industry"] = "SaaS"
            elif "streaming" in lower or "video" in lower:
                st.session_state.context_data["industry"] = "Video Streaming"
            else:
                st.session_state.context_data["industry"] = user_text
            st.session_state.current_phase = "business_focus"
        elif st.session_state.current_phase == "business_focus" and not st.session_state.context_data["business_focus"]:
            if "video" in user_text.lower() and "stream" in user_text.lower():
                st.session_state.context_data["business_focus"] = "Video Streaming Platform"
            else:
                st.session_state.context_data["business_focus"] = user_text
            st.session_state.current_phase = "sophistication"
        elif st.session_state.current_phase == "sophistication" and not st.session_state.context_data.get("sophistication_level"):
            sophistication = detect_sophistication_level(user_text)
            if sophistication:
                st.session_state.context_data["sophistication_level"] = sophistication
                st.session_state.detailed_mode = (sophistication == "detailed")
                st.session_state.current_phase = "metrics"
            else:
                st.session_state.context_data["sophistication_level"] = "basic"
                st.session_state.detailed_mode = False
                st.session_state.current_phase = "metrics"
        elif st.session_state.current_phase == "metrics":
            metrics = extract_key_metrics_from_conversation()
            st.session_state.context_data["key_metrics_discussed"] = metrics
            if st.session_state.detailed_mode and st.session_state.detailed_depth < st.session_state.max_detailed_depth:
                st.session_state.detailed_depth += 1
                st.session_state.context_data.setdefault("detailed_answers", []).append({
                    "depth": st.session_state.detailed_depth,
                    "question": st.session_state.conversation_history[-2]["content"] if len(st.session_state.conversation_history) >= 2 else "",
                    "answer": user_text,
                })
            else:
                if len(st.session_state.context_data.get("key_metrics_discussed", [])) >= 2:
                    st.session_state.sufficient_detail = True
                elif len(st.session_state.conversation_history) > 8:
                    st.session_state.sufficient_detail = True
        st.rerun()

# Category selection phase (after sufficient detail)
if st.session_state.sufficient_detail and st.session_state.user_selected_category is None and not st.session_state.collected_data:
    st.subheader("Select a Category")
    st.write("I notice we have these categories available in our system:")
    category = st.selectbox("Choose an existing category or leave empty for suggestion", ["(Suggest for me)"] + AVAILABLE_CATEGORIES)
    if category and category != "(Suggest for me)":
        st.session_state.user_selected_category = category
        st.success(f"Using '{category}' as your category.")
    if st.button("Continue", type="primary"):
        st.session_state.user_selected_category = st.session_state.user_selected_category or None
        st.rerun()

# Suggestion phase
if st.session_state.sufficient_detail and not st.session_state.collected_data:
    st.subheader("Suggestion")
    st.info("Analyzing your conversation to suggest the best assumption setup…")
    st.session_state.context_data["key_metrics_discussed"] = extract_key_metrics_from_conversation()
    suggestion_context = {
        "business_context": st.session_state.context_data,
        "conversation_summary": "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.conversation_history]),
        "key_metrics": st.session_state.context_data["key_metrics_discussed"],
        "user_selected_category": st.session_state.user_selected_category,
    }
    suggestion_response = Suggestion_agent.run(json.dumps(suggestion_context, indent=2))

    final_category = st.session_state.user_selected_category
    try:
        json_str = getattr(suggestion_response, "content", str(suggestion_response)).strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0].strip()
        suggestion_data = json.loads(json_str)
        if not final_category:
            final_category = suggestion_data.get("category", "N/A")
        st.session_state.collected_data = {
            "Assumption_name": suggestion_data.get("assumption_name"),
            "Category": final_category,
            "Aggregation": suggestion_data.get("aggregation"),
            "Drivers": suggestion_data.get("drivers", []),
        }
    except Exception:
        metrics = st.session_state.context_data.get("key_metrics_discussed", [])
        industry = st.session_state.context_data.get("business_focus") or st.session_state.context_data.get("industry", "Business")
        if metrics:
            assumption_name = f"{metrics[0]} Forecast for {industry}"
        else:
            assumption_name = f"{industry} Performance Forecast"
        if not final_category:
            if any(m in ["Revenue", "ARPU"] for m in metrics):
                final_category = "Revenue"
            elif any(m in ["Monthly Active Users", "New Subscribers", "Retention Rate"] for m in metrics):
                final_category = "User Metrics"
            elif any(m in ["Watch Time", "Engagement"] for m in metrics):
                final_category = "Content Performance"
            else:
                final_category = "Operational"
        st.session_state.collected_data = {
            "Assumption_name": assumption_name,
            "Category": final_category,
            "Aggregation": "Sum",
            "Drivers": [],
        }

    with st.expander("Suggested Assumption", expanded=True):
        cd = st.session_state.collected_data
        st.write(f"Assumption Name: **{cd.get('Assumption_name', 'N/A')}**")
        st.write(f"Category: **{cd.get('Category', 'N/A')}**")
        st.write(f"Aggregation: **{cd.get('Aggregation', 'N/A')}**")
        drivers = cd.get("Drivers", [])
        if drivers:
            st.write("Drivers:")
            st.write(", ".join(drivers))
        else:
            st.write("Drivers: None")

# Confirmation and modifications
if st.session_state.collected_data and "confirmed" not in st.session_state:
    st.subheader("Confirm or Modify")
    st.write("- Say 'yes' or 'looks good' to confirm\n- Suggest changes like 'make the category more specific'\n- Or ask to add/remove drivers")
    feedback = st.text_input("Your feedback")
    col1, col2 = st.columns(2)
    if col1.button("Submit Feedback"):
        confirmation_response = Confirmation_agent.run(json.dumps({
            "suggestion": st.session_state.collected_data,
            "user_feedback": feedback,
            "previous_changes": 0,
        }))
        try:
            confirmation_data = json.loads(getattr(confirmation_response, "content", str(confirmation_response)))
            intent = confirmation_data.get("intent")
            if intent == "confirm":
                st.session_state.confirmed = True
                st.success("Perfect! Your assumption is locked in and ready for forecasting!")
            elif intent == "change":
                target_field = confirmation_data.get("target_field")
                new_value = confirmation_data.get("new_value")
                if target_field and new_value:
                    st.session_state.collected_data[target_field] = new_value.strip()
                    st.info(f"Updated {target_field} to: {st.session_state.collected_data[target_field]}")
            elif intent == "add_drivers":
                to_add = confirmation_data.get("drivers_to_add", [])
                if to_add:
                    st.session_state.collected_data.setdefault("Drivers", []).extend(to_add)
                    st.info(f"Added drivers: {', '.join(to_add)}")
            elif intent == "remove_drivers":
                to_remove = confirmation_data.get("drivers_to_remove", [])
                if to_remove:
                    current = st.session_state.collected_data.get("Drivers", [])
                    st.session_state.collected_data["Drivers"] = [d for d in current if d not in to_remove]
                    st.info(f"Removed drivers: {', '.join(to_remove)}")
            elif intent == "replace_drivers":
                # Support agent returning a replacement list in drivers_to_add or new_drivers
                new_list = confirmation_data.get("new_drivers")
                if not new_list:
                    new_list = confirmation_data.get("drivers_to_add")
                if isinstance(new_list, list) and new_list:
                    st.session_state.collected_data["Drivers"] = [str(d).strip() for d in new_list if str(d).strip()]
                    st.info("Replaced drivers with provided list.")
                else:
                    st.warning("No drivers provided to replace.")
            else:
                st.warning("I want to make sure I get this right. Could you tell me what you'd like to change?")
        except Exception:
            st.warning("Sorry, I'm having trouble understanding. Could you rephrase that?")
    if col2.button("Confirm Now", type="primary"):
        st.session_state.confirmed = True
        st.success("Perfect! Your assumption is locked in and ready for forecasting!")

# Final output and payloads
if st.session_state.collected_data and st.session_state.get("confirmed"):
    st.subheader("Finalized Assumption")
    for field in REQUIRED_FIELDS:
        if field == "Drivers":
            drivers = st.session_state.collected_data.get(field, [])
            st.write(f"{field}: {', '.join(drivers) if drivers else 'None discussed'}")
        else:
            st.write(f"{field}: {st.session_state.collected_data.get(field, 'Not set')}")

    st.divider()
    st.subheader("Create API Payloads")
    with st.form("payload_form"):
        org_id = st.number_input("Organisation ID", min_value=1, value=34)
        forecast_id = st.number_input("Forecast Measure ID", min_value=1, value=234)
        categories_json = st.text_area(
            "Available categories (JSON array with id, name)",
            value=json.dumps([
                {"id": 1, "name": "Revenue"},
                {"id": 2, "name": "Revenue & Sales"},
                {"id": 3, "name": "Capital Expenditure"},
            ], indent=2),
            height=150,
        )
        submitted = st.form_submit_button("Generate Payloads", type="primary")
    if submitted:
        try:
            available_categories = json.loads(categories_json)
            payloads = create_assumptions_payload(
                st.session_state.collected_data, int(org_id), int(forecast_id), available_categories
            )
            st.success(f"API Payloads created successfully! Number of payloads: {len(payloads)}")
            for i, payload in enumerate(payloads, start=1):
                with st.expander(f"Payload {i}: {payload.get('name')}"):
                    st.write(f"Assumption Name: {payload['name']}")
                    st.write(f"Category Name: {payload['category_name']}")
                    st.write(f"Category ID: {payload['category_id']}")
                    st.write(f"Is New: {payload['is_new']}")
                    st.write(f"Aggregation: {payload['aggregation']}")
                    st.code(json.dumps(payload, indent=2), language="json")
        except Exception as e:
            st.error(f"Failed to create payloads: {e}")

st.caption("Run with: streamlit run streamlit_app.py")
