def get_regulation_and_industry_for_loader() -> tuple[str, str]:
    """Map session state values to correct regulation directory and industry filename for questionnaire loading.

    Returns:
        tuple[str, str]: (regulation_directory, industry_filename)
    """
    import streamlit as st
    import logging
    import time
    logger = logging.getLogger(__name__)
    
    # Simple logging throttle to avoid spam
    current_time = time.time()
    if not hasattr(get_regulation_and_industry_for_loader, '_last_log_time'):
        get_regulation_and_industry_for_loader._last_log_time = 0
        get_regulation_and_industry_for_loader._last_values = None
    
    industry_file_map = {
        "Oil and Gas": "Oil_and_Gas",
        "Banking and finance": "Banking and finance",
        "E-commerce": "E-commerce",
        "General": "npc"  # Map General industry to npc.json file
    }
    regulation_map = {
        "India": "DPDP",
        "Qatar": "PDPPL",  # Default Qatar mapping
        "ndp_qatar": "PDPPL"
    }
    
    # Get the selected country and industry
    selected_country = st.session_state.get('selected_country', '')
    selected_industry = st.session_state.get('selected_industry', '')
    
    # Normalize the selected industry first
    if not selected_industry:
        # Set default industry based on country only if industry is empty
        if selected_country == "Qatar":
            selected_industry = "Oil and Gas"  # Default to Oil and Gas for Qatar
        elif selected_country == "India":
            selected_industry = "Banking and finance"
        else:
            selected_industry = "Oil and Gas"  # Default fallback
    elif selected_industry == "general":
        # Convert lowercase "general" to proper case "General"
        selected_industry = "General"
    
    # Special handling for Qatar: determine regulation based on industry
    if selected_country == "Qatar":
        if selected_industry == "General":
            regulation = "NPC"
        else:
            regulation = "PDPPL"  # Oil and Gas goes to PDPPL
    else:
        regulation = regulation_map.get(selected_country, st.session_state.get('selected_regulation', ''))
    
    # Map the display industry to file industry
    industry = industry_file_map.get(selected_industry, selected_industry)
    
    # DEMO MODE: Force NPC for all selections
    regulation = "NPC"
    industry = "npc"
    
    # Only log if values changed or it's been more than 5 seconds since last log
    current_values = (selected_country, selected_industry, regulation, industry)
    should_log = (
        get_regulation_and_industry_for_loader._last_values != current_values or
        current_time - get_regulation_and_industry_for_loader._last_log_time > 5.0
    )
    
    if should_log:
        logger.info(f"[UTILS] get_regulation_and_industry_for_loader: country='{selected_country}', industry='{selected_industry}'")
        logger.info(f"[DEMO] FORCING NPC regardless of selection")
        logger.info(f"[UTILS] FINAL RESULT: regulation='{regulation}', industry='{industry}'")
        get_regulation_and_industry_for_loader._last_log_time = current_time
        get_regulation_and_industry_for_loader._last_values = current_values
    
    return regulation, industry 