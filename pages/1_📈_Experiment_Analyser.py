from math import pi
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio
from utils.db_connector import DBConnector
from utils.results import Results

pio.templates.default = "seaborn"
st.set_page_config(
    page_title="Experiment Analyser - PromptSLR",
    page_icon="📈",
    layout="wide",
)

db_connector = DBConnector()


def get_results_df(project_ids, metrics=None):
    results = []
    for project_id in project_ids:
        result = Results(project_id)
        results.append(
            {
                "ProjectID": project_id,
                "Completed Articles": result.tp + result.fp + result.tn + result.fn,
                "Articles with Error": result.fp + result.fn,
                "True Positive": result.tp,
                "False Positive": result.fp,
                "True Negative": result.tn,
                "False Negative": result.fn,
                "Accuracy": result.get_accuracy(),
                "Precision": result.get_precision(),
                "Recall": result.get_recall(),
                "F1 Score": result.get_f1_score(),
                "Specificity": result.get_specificity(),
                "MCC": result.get_mcc(),
                "Balanced Accuracy": result.get_balanced_accuracy(),
                "Miss Rate": result.get_miss_rate(),
                "F2 Score": result.get_fb_score(2),
                "WSS": result.get_wss(),
                "WSS@95": result.get_wss(recall=0.95),
                "NPV": result.get_npv(),
                "G Mean": result.get_g_mean(),
                "General Performance Score": result.get_gps(),
            }
        )
    df = pd.DataFrame(results)
    return df


def get_multiple_iterations_df(project_id):
    result = Results(project_id)
    df = result.get_moment_values_df()
    return df


st.title("📈 Experiment Analyser")
st.header("Choose the experiment you want to analyse")
experiment = st.multiselect(
    "Experiment",
    [f"{value} - {key}" for key, value in db_connector.get_projects().items()],
)
if experiment:
    project_lables, project_ids = zip(*[project.split(" - ") for project in experiment])

    st.subheader("Choose the metrics you want to analyse")
    metrics = st.multiselect(
        "Metrics",
        [
            "Completed Articles",
            "Articles with Error",
            "True Positive",
            "False Positive",
            "True Negative",
            "False Negative",
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "Specificity",
            "MCC",
            "Balanced Accuracy",
            "Miss Rate",
            "F2 Score",
            "WSS",
            "WSS@95",
            "NPV",
            "G Mean",
            "General Performance Score",
        ],
    )

    st.subheader("Choose the plot you want to see")
    plot = st.selectbox(
        "Plot", ["Bar", "Line", "Pie", "Scatter", "Radial", "Boxplot"], index=0
    )
    if metrics and plot:
        if plot == "Bar":
            st.subheader("Choose the x and y axis")
            x_axis = st.selectbox("X-Axis", metrics, index=0)
            if len(metrics) > 1:
                y_axis = st.selectbox("Y-Axis", metrics, index=1)
                df = get_results_df(project_ids)
                fig = px.bar(df, x=x_axis, y=y_axis, hover_name=project_lables)
                st.plotly_chart(fig)
            else:
                st.warning("Please select more than one metric to plot a bar chart")

        elif plot == "Line":
            st.subheader("Choose the x and y axis")
            x_axis = st.selectbox("X-Axis", metrics, index=0)
            if len(metrics) > 1:
                y_axis = st.selectbox("Y-Axis", metrics, index=1)
                df = get_results_df(project_ids)
                fig = px.line(df, x=x_axis, y=y_axis, hover_name=project_lables)
                st.plotly_chart(fig)
            else:
                st.warning("Please select more than one metric to plot a line chart")

        elif plot == "Pie":
            st.subheader("Choose the values")
            values = st.multiselect("Values", metrics)
            df = get_results_df(project_ids)
            df = df.drop(columns=[c for c in df.columns if c not in values])
            df = df.T
            df.columns = project_lables
            fig = px.pie(
                df,
                values=project_lables[0],
                names=df.index,
                title=f"Values for {project_lables[0]}",
            )
            st.plotly_chart(fig)

        elif plot == "Scatter":
            st.subheader("Choose the x and y axis")
            x_axis = st.selectbox("X-Axis", metrics, index=0)
            if len(metrics) > 1:
                y_axis = st.selectbox("Y-Axis", metrics, index=1)
                df = get_results_df(project_ids)
                fig = px.scatter(df, x=x_axis, y=y_axis, hover_name=project_lables)
                st.plotly_chart(fig)
            else:
                st.warning("Please select more than one metric to plot a scatter chart")

        elif plot == "Radial":
            df = get_results_df(project_ids)
            df = df.drop(columns=[c for c in df.columns if c not in metrics])
            df = df.T
            df.columns = project_lables
            df["metrics"] = df.index
            df = df.melt(
                id_vars="metrics", var_name="Experiment Name", value_name="value"
            )
            fig = px.line_polar(
                df,
                r="value",
                theta="metrics",
                line_close=True,
                markers=True,
                hover_name="Experiment Name",
                color="Experiment Name",
                color_discrete_sequence=px.colors.qualitative.Plotly,
            )
            st.plotly_chart(fig)

        # box plot
        elif plot == "Boxplot":
            # y_axis = st.selectbox("Y-Axis", metrics, index=1)
            df = get_multiple_iterations_df(project_ids[0])
            for i in [i.lower().replace(" ", "_") for i in metrics]:
                fig = px.box(df, y=i)
                st.plotly_chart(fig)
