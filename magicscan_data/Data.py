import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

MONGO_URL = st.secrets.db.MONGO_URL

chain_ids = {
    1: "Ethereum",
    10: "Optimism",
    8453: "Base",
    8008: "Polynomial",
    11155111: "Sepolia",
    11155420: "Optimism Sepolia",
    84532: "Base Sepolia",
    80008: "Polynomial Sepolia",
}


# data
# @st.cache_data(ttl=600)
def fetch_data():
    client = MongoClient(MONGO_URL, server_api=ServerApi("1"))
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    collection = client["magicscan-backend"]["user-operation-events"]

    pipeline = [
        {
            "$facet": {
                "totalCount": [{"$count": "count"}],
                "chainIdCounts": [
                    {"$group": {"_id": "$chainId", "count": {"$sum": 1}}},
                ],
            }
        }
    ]

    result = list(collection.aggregate(pipeline))[0]
    document_count = result["totalCount"][0]["count"] if result["totalCount"] else 0
    chain_id_counts = {
        chain_ids[item["_id"]]: item["count"] for item in result["chainIdCounts"]
    }

    data = {
        "document_count": document_count,
        "chain_id_counts": chain_id_counts,
    }

    return data


def main():
    st.markdown("## [Magicscan](https://magicscan.xyz)")

    data = fetch_data()

    st.markdown(
        f"<h2 style='text-align: center;'>Total User Operation Events</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h2 style='text-align: center; color: #CF8CEF;'>{data['document_count']:,.0f}</h2>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    chain_id_counts = list(data["chain_id_counts"].items())
    mid_index = len(chain_id_counts) // 2

    with col1:
        for chain_id, count in chain_id_counts[:mid_index]:
            st.markdown(
                f"<h3>{chain_id}</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='text-align: center; color: #C2EC4A;'>{count:,.0f}</h3>",
                unsafe_allow_html=True,
            )

    with col2:
        for chain_id, count in chain_id_counts[mid_index:]:
            st.markdown(
                f"<h3>{chain_id}</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<h3 style='text-align: center; color: #C2EC4A;'>{count:,.0f}</h3>",
                unsafe_allow_html=True,
            )
