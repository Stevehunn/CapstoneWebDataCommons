import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import json
import glob
import re

# Custom CSS
custom_css = """
<style>
    /* Your custom CSS goes here */
   [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 95%
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

def extraire_contenu_apres_backslash(ma_ligne):
    # Regex pour supprimer tout le contenu avant le dernier caractère '\'
    nouveau_contenu = re.sub(r'^.*\\', '', ma_ligne)
    return nouveau_contenu

def construire_chemin_complet(contenu_apres_backslash):
    regexSelect = contenu_apres_backslash +"_plot.svg"
    regexSelect ="assets/plots//" +regexSelect

    return regexSelect

target_classes = []
for file in glob.glob("""assets/plots//*.svg"""):
    fname = file.split("""assets/plots//""")[0]
    cname = fname.split("""_plot.svg""")[0]
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

    st.sidebar.title("Here you can navigate throught the demo")
    with st.sidebar:
        selected_tab = option_menu(
            menu_title = "Summary",
            options=["Welcome page","Data from 2022","New Data from 2023","Comparison between the two dataset","New style of chart"],
        )
    if selected_tab =="Welcome page":
        content_welcome()
    if selected_tab =="Data from 2022":
        content_2022()
    if selected_tab =="New Data from 2023":
        content_2023()
    if selected_tab =="Comparison between the two dataset":
        content_comparison()
    if selected_tab =="New style of chart":
        content_new_style()


# Welcome page Content
def content_welcome():

    # Content
    st.title("""TheMiKroloG: The Microdata Knowledge Graph""")

    st.write("## Introduction")
    st.write("""Welcome to an immersive experience that transcends the boundaries of time! In this cutting-edge technical demo, we invite you to explore the rich tapestry of web data collected through the "Common Crawl" initiative over two distinct years. Embark on a journey that unveils the evolution of the digital landscape, showcasing the power of longitudinal data analysis.""")
    st.markdown("[Previous demo in Dash](https://schema-obs-demo.onrender.com/) ")
    st.markdown("Link of the article relate to this demo : [Article link](https://hal.science/hal-04250523/document)")
    st.write("## About Common Crawl")
    st.write("Common Crawl is a monumental effort to index and archive the vast expanse of the World Wide Web. Through meticulous crawling, it captures web pages, providing a comprehensive snapshot of the internet's content at different points in time. Leveraging the open nature of Common Crawl data, our research delves into the depths of this treasure trove, extracting valuable insights that bridge the gap between past and present.")
    st.write("## Key Features")
    st.write("""1. Temporal Evolution Analysis
Dive into a comparative analysis of web content spanning two different years. Witness how the digital landscape has transformed, identify emerging trends, and understand the dynamics that have shaped the online world over time.

2. Data Visualization Showcase
Experience the power of data visualization as we present captivating representations of key trends and patterns. Our interactive visualizations bring to life the wealth of information hidden within the Common Crawl dataset, making complex data accessible and engaging.

3. Innovative Research Findings
Discover groundbreaking research findings derived from the analysis of Common Crawl data. Our team has unearthed compelling correlations, identified influential factors, and examined the nuances that define the evolution of web content over the selected time periods.""")
    st.write("## How to Navigate")
    st.write("""Temporal Selection: Choose the years you wish to explore using the interactive timeline.
Category Insights: Delve into specific content categories to uncover niche trends.
Data Filters: Tailor your exploration by applying filters based on keywords, domains, or geographical regions.""")
    st.write("## Join Us on this Journey")
    st.write("""Embark on a captivating exploration of the internet's history. Whether you are a researcher, data enthusiast, or simply curious about the evolution of the digital landscape, our Web Data Time Travel Demo promises a unique and enlightening experience.""")
    st.write("## Begin Your Journey")
    st.write("""Click on the Summary menu in the side to commence your exploration of Common Crawl data across time. Uncover the past, understand the present, and glimpse into the future of the World Wide Web.""")

def content_new_style():
    loadTreemapImage ="assets/images/Treemap.png"
    st.write("Treemap")
    st.image(loadTreemapImage)
    st.markdown("---")
    loadVerticalTableAndChart ="assets/images/VerticalTableAndChart.png"
    st.write("Vertical Table and Chart (Histogramme)")
    st.image(loadVerticalTableAndChart)

# Comparison page Content
def content_comparison():

    # Content
    st.title("""In this page we compare the two Dataset from 2022 and 2023""") 

    select=st.selectbox("",target_classes)
    regexSelect =extraire_contenu_apres_backslash(select)
    st.write("Evolution of the ",regexSelect," between 2022 and 2023")
    regexSelect = regexSelect +"_plot.svg"
    regexSelect ="assets/plots//" +regexSelect

    coll1, coll2 = st.columns(2)

    with coll1:
        st.image(regexSelect)
   


    with coll2:
        st.image(regexSelect)
 

    col1, col2 , col3= st.columns(3)

    with col1:
        st.write("Average:5")
        st.write("Coverage:3")
        st.write("Count:100")

    
    
    with col2:
        st.write("Average evolution: 20%")
        st.write("Coverage evolution: 30%")
        st.write("Count evolution:100%")
        


    with col3:
        st.write("Average:7")
        st.write("Coverage:5")
        st.write("Count:200")

    
    




    
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
    #nomFichierAOuvrir = "assets/plots/3DModel_plot.svg"
    #st.image(nomFichierAOuvrir)
    #st.write('chemin complet nomFichierAOuvir:',nomFichierAOuvrir)
    select=st.selectbox("",target_classes)
    regexSelect =extraire_contenu_apres_backslash(select)
    regexSelect = regexSelect +"_plot.svg"
    regexSelect ="assets/plots//" +regexSelect
    st.image(regexSelect)
    st.markdown("---")
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
            "width": "100%",
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
        select2=st.selectbox("",target_classes)
        regexSelect =extraire_contenu_apres_backslash(select2)
        regexSelect = regexSelect +"_plot.svg"
        regexSelect ="assets/plots//" +regexSelect
        st.image(regexSelect)
        st.markdown("---")

# Run the app
if __name__ == '__main__':
    main()