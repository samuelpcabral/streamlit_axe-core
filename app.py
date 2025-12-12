import streamlit as st
from datetime import datetime
from scripts.run_axe_core import execute_axe_core
from scripts.parse_log import get_violations, issues_for_dataframe


col1, col2, col3 = st.columns([1, 2, 1])
st.set_page_config(layout="wide")


# Initialize sessions states
if 'log_history' not in st.session_state:
    st.session_state['log_history'] = "--- Console Started ---\n"
if 'desktop_width' not in st.session_state:
    st.session_state.desktop_width = "1920"
if 'desktop_height' not in st.session_state:
    st.session_state.desktop_height = "1080"


# Functions
def reset_desktop_values():
    """Resets the desktop resolution values in session state."""
    st.session_state.desktop_width = "1920"
    st.session_state.desktop_height = "1080"


# User Interface
with col2:
    st.title("Run Axe-Core accessibility tests", text_alignment="center")

# User input
with col2:
    url = st.text_input("Enter the URL to test")
    mode = st.radio("Select browser mode", ["desktop", "mobile"], horizontal=True)

with col3:
    with st.container(border=True, vertical_alignment="center"):
        if mode == "mobile":
            st.markdown("##### Select mobile device :material/mobile_2:")
            device = st.radio("models:", ["Pixel 7", "Galaxy S8", "Galaxy Z Fold 5",
                                          "iPhone 12 Pro", "iPhone 14 Pro Max", "iPad Mini", "iPad Air"])
            width = None
            height = None
        else:
            st.markdown("##### Select desktop resolution :material/desktop_windows:")
            width = st.text_input("Width: :material/fit_page_width:", key='desktop_width')
            height = st.text_input("Height: :material/fit_page_height:", key='desktop_height')
            device = None
            st.button("Reset Values", on_click=reset_desktop_values)

# Button actions
result = None
with col2:
    valid_url = ('http://', 'https://')
    with st.spinner("#### Running tests... :material/directions_run: Please wait!"):
        if st.button("Run Axe-Core"):
            if mode == "desktop" and not (width.isdigit() and height.isdigit()):
                st.warning("Please enter a valid resolution")
            elif not url or not url.startswith(valid_url):
                st.warning("Please enter a valid URL")
            else:
                timestamp = datetime.now().strftime("%H:%M:%S")
                new_log = f"[{timestamp}] Starting test for: {url}\n"
                st.session_state['log_history'] = new_log + st.session_state['log_history']
                axe_core_result = execute_axe_core(url, mode=mode, device=device, width=width, height=height)
                count, result = get_violations(axe_core_result)
                elements = issues_for_dataframe(result)
                elements_count = len(elements)
                new_log = f"[{timestamp}] Total of {count} violations found in {elements_count} elements\n"
                st.session_state['log_history'] = new_log + st.session_state['log_history']
                st.success("Test completed successfully, see results below!")

# Show results for each violation
if result:
    blank_space = "&nbsp;" * 10
    with st.spinner("#### Loading violations... :material/data_table: Please wait!"):
        with st.expander(f"Total of {count} violations found.{blank_space}:blue[click to open]",
                         expanded=False, icon=":material/view_list:"):
            st.dataframe(result["violations"], height="content", row_height=50,
                         column_order=["id", "impact", "description", "help", "helpUrl", "tags"],
                         column_config={
                             "helpUrl": st.column_config.LinkColumn("Help URL"),
                             "tags": st.column_config.ListColumn("Tags")
                         }
                         )
# Show result for each element with issues
    with st.spinner("#### Loading all elements... :material/data_table: Please wait!"):
        with st.expander(f"Total of {elements_count} elements with issues.{blank_space}:blue[click to open]",
                         expanded=False, icon=":material/view_list:"):
            st.dataframe(elements, height="content", row_height=50,
                         column_order=["id", "impact", "failureSummary", "html", "target", "description", "help",
                                       "helpUrl", "nodes", "tags"],
                         column_config={
                             "failureSummary": "Failure Summary",
                             "helpUrl": st.column_config.LinkColumn("Help URL"),
                             "tags": st.column_config.ListColumn("Tags")
                         }
                         )

st.markdown("---")

# Display the text area for log history which is always visible
st.subheader("Execution Logs")
st.text_area(
    label="Console Output",
    value=st.session_state['log_history'],
    height=300,
    disabled=True
)
