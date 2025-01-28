import streamlit as st
import streamlit_antd_components as sac

# Corrected categories dictionary with camel case
categories = {
    "AllocationAcc": ["AllocationAccountID"],
    "Book": ["Book", "BookParty"],
    "Borrower": ["BorrowerID", "BorrowerName"],
    "Broker": ["BrokerName", "BrokerFee", "BrokerCurrency"],
    "ClearingHouse": ["ClearingHouseName", "Clearing3D", "ClearingStatus"],
    "Client": ["ClientName", "ClientRegionID"],
    "CountsAndFlags": ["TradeCount", "LateFlag", "NetTradeFlag", "CancelTradeFlag", "AppendedFlagsLatest"],
    "CounterParty": ["CounterPartyName", "CounterPartyType", "AggregationMode"],
    "Dates": ["StartDate", "ExpiryDate", "EndDate", "OrderDateTime", "MessageTimestamp"],
    "Economics": ["Quantity", "Price", "Notional", "Abstract"],
    "Entity": ["EntityName"],
    "Events": ["TradeStatus", "BusinessEvent", "EventType", "Action"],
}

# Create category tree items
category_tree_items = [
    sac.TreeItem(category, children=[sac.TreeItem(column) for column in columns])
    for category, columns in categories.items()
]

# Render the tree in the Streamlit sidebar
selected_columns = sac.tree(
    items=category_tree_items,
    label="Features",
    open_all=False,
    checkbox=True,
)

st.write("Selected Columns:", selected_columns)
