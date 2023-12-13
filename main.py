import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import json
import glob 

# Custom CSS
custom_css = """
<style>
    /* Your custom CSS goes here */
    .st-emotion-cache-1y4p8pa {
        max-width: 70rem
    }
</style>
"""


# List of Schema available
top_20_target_classes = [
    "ListItem",
    "ImageObject",
    "BreadcrumbList",
    "Organization",
    "WebPage",
    "SearchAction",
    "Offer",
    "Person",
    "ReadAction",
    "Product",
    "EntryPoint",
    "PostalAddress",
    "Article",
    "WebSite",
    "CollectionPage",
    "NewsArticle",
    "SiteNavigationElement",
    "ContactPoint",
    "Rating",
    "Place",
]

class Node:
    def __init__(self, id, generation, parent=None, value=-1) -> None:
        self._id = id
        self._generation = generation
        self._parent = parent
        self._value = value

    def __eq__(self, __value: object) -> bool:
        return self._id == __value._id

    def __repr__(self) -> str:
        return self._id


def item_generator(json_input, lookup_key, depth=None):
    if depth is None:
        depth = 0
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield from item_generator(v, lookup_key, depth + 1)
        yield (depth, json_input)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key, depth)

target_classes = []
for file in glob.glob("assets/plots/*.svg"):
    fname = file.split("assets/plots/")
    if len(fname) > 1:
        fname = fname[1]
    else:
        # Handle the case where the substring is not found
        fname = "default_value"  # Replace "default_value" with the appropriate default value or handle the situation accordingly
    cname = fname.split("_plot.svg")[0]
    target_classes.append(f"schema:{cname}")
target_classes.sort()

# sunburst
data_plotly_sunburst = {"ids": [], "names": [], "parents": [], "values": []}
with open("data/count.json", "r") as file:
    parsed_json = json.load(file)

    itemlist = sorted(item_generator(parsed_json, "children"), key=lambda x: x[0])

    nodelist = []
    for generation, parent in itemlist:
        if parent.get("value") is None:
            parent["value"] = 0

        parent_node = Node(parent["@id"], generation, value=parent["value"])
        if parent_node not in nodelist:
            # print(f"Adding {parent_node} to {nodelist}")
            nodelist.append(parent_node)

        if "children" in parent.keys():
            for child in parent.get("children"):
                if child.get("value") is None:
                    child["value"] = 0
                child_node = Node(
                    child["@id"], generation, parent=parent["@id"], value=child["value"]
                )
                nodelist.append(child_node)

    for node in nodelist:
        id = node._id
        if id in data_plotly_sunburst["ids"]:
            id = f"{node._id} {node._parent} {node._generation}"
        data_plotly_sunburst["ids"].append(id)
        data_plotly_sunburst["names"].append(node._id)
        data_plotly_sunburst["values"].append(node._value)
        data_plotly_sunburst["parents"].append(node._parent)

# Define content show, sidebar
def main():
    content_sidebar()
    return None

# Side Content
def content_sidebar():

    # Display custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    st.sidebar.title("Here you can select different operation realise on the data")
    with st.sidebar:
        selected_tab = option_menu(
            menu_title = "Summary",
            options=["Welcome page","Data from 2022","New Data from 2023","Comparison between the two dataset"],
        )
    if selected_tab =="Welcome page":
        content_welcome()
    if selected_tab =="Data from 2022":
        content_2022()
    if selected_tab =="New Data from 2023":
        content_2023()
    if selected_tab =="Comparison between the two dataset":
        content_comparison()


# Welcome page Content
def content_welcome():

    # Content
    st.title("""TheMiKroloG: The Microdata Knowledge Graph""")
    st.markdown("[Previous demo in Dash](https://schema-obs-demo.onrender.com/) ")

# Comparison page Content
def content_comparison():

    

    # Content
    st.title("""In this page we compare the two Dataset from 2022 and 2023""")




    
# 2022 Analyse page Content 
def content_2022():
    

    # Content
    st.title("""Schema.org annotations observatory in 2022""")
    st.write("### Deep dive into WebDataCommons JSON-LD markup")
    st.markdown("---")
    st.markdown(
        """
        Per-class top-10 property combinations.
        In the following upset plots, you can select a Schema.org class and display the most used property combinations (top-10).
        All these 776 plots have been rendered based on the Schema.org characteristic sets we pre-computed and made available at [https://zenodo.org/records/8167689](https://zenodo.org/records/8167689)
        
        """
    )
    select=st.selectbox("",top_20_target_classes)
    select="schema\:"+select
    st.write('You selected:', select)


    st.markdown(
        """
        In the following sunburst plot, the count of typed entities is displayed through the 'value' attribute.
        """
    )

    st.markdown("---")

    figure=px.sunburst(
        data_plotly_sunburst,
        ids="ids",
        names="names",
        parents="parents",
        values="values",
    )
    style={
        "padding": 10,
        "width": "100%",
        # "height": "70vh",
        # "width": "70vw",
        "display": "inline-block",
        "vertical-align": "right",
    },

    # Display the Plotly figure using st.plotly_chart
    st.plotly_chart(figure, use_container_width=True, style=style)

# 2023 Analyse page Content 
def content_2023():
    

    # Content
    st.title("""Schema.org annotations observatory in 2023""")
    st.write("### Deep dive into WebDataCommons JSON-LD markup")
    st.markdown("---")
   
    col1, col2 = st.columns(2)

    with col1:
        figure=px.sunburst(
            data_plotly_sunburst,
            ids="ids",
            names="names",
            parents="parents",
            values="values",
        )
        style={
            "padding": 10,
            "width": "100%",
            # "height": "70vh",
            # "width": "70vw",
            "display": "inline-block",
            "vertical-align": "right",
        },

        # Display the Plotly figure using st.plotly_chart
        st.plotly_chart(figure, use_container_width=True, style=style)

    with col2:
        st.markdown(
        """
        Per-class top-10 property combinations.
        In the following upset plots, you can select a Schema.org class and display the most used property combinations (top-10).
        All these 776 plots have been rendered based on the Schema.org characteristic sets we pre-computed and made available at [https://zenodo.org/records/8167689](https://zenodo.org/records/8167689)
        
        """
        )
        select2=st.selectbox("",top_20_target_classes)
        st.write('You selected:', select2)

# Run the app
if __name__ == '__main__':
    main()