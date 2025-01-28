def render_sidebar():
    import streamlit_antd_components as sac
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
    category_tree_items = [
        sac.TreeItem(category, children=[sac.TreeItem(column) for column in columns])
        for category, columns in categories.items()
    ]
    selected_columns = sac.tree(
        items=category_tree_items,
        label="Features",
        open_all=False,
        checkbox=True,
    )
    return selected_columns
