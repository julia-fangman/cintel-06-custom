# Import necessary libraries
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui

ui.page_opts(title="Titanic Dashboard", fillable=True)

with ui.sidebar(title="About The Titanic Dashboard", style="background-color: #FFC0CB;"):
    ui.markdown("""
    Welcome to the Titanic Dashboard! Explore insights into the Titanic dataset using the filter controls provided.
    
    Filter passengers by age, sex, and ticket class. View the number of passengers, average age, and fare. Visualizations depict the relationship between age and fare, along with detailed passenger data.

    Feel free to interact with the dashboard and explore further!
    """)

    ui.input_slider("age", "Age", 0, 100, 100)
    ui.input_checkbox_group(
        "sex",
        "Sex",
        ["male", "female"],
        selected=["male", "female"],
    )
    ui.input_checkbox_group(
        "ticket_class",
        "Class",
        ["First", "Second", "Third"],
        selected=["First", "Second", "Third"],
    )
    ui.a(
        "GitHub Source",
        href="https://github.com/julia-fangman/cintel-06-custom/blob/main/app.py",
        target="_blank",
        style="color: black; display: block; margin-top: 20px;",
    )
    ui.a(
        "GitHub App",
        href="https://github.com/julia-fangman/cintel-06-custom",
        target="_blank",
        style="color: black;",
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="background-color: #FFC0CB;"):
        "Number of passengers"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="background-color: #FFC0CB;"):
        "Average age"

        @render.text
        def avg_age():
            return f"{filtered_df()['age'].mean():.1f} years"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="background-color: #FFC0CB;"):
        "Average fare"

        @render.text
        def avg_fare():
            return f"${filtered_df()['fare'].mean():.2f}"


with ui.layout_columns():
    with ui.card(full_screen=True, style="background-color: #FFC0CB;"):
        ui.card_header("Age and Fare")

        @render.plot
        def age_fare():
            return sns.scatterplot(
                data=filtered_df(),
                x="age",
                y="fare",
                hue="class",
            )

    with ui.card(full_screen=True, style="background-color: #FFC0CB;"):
        ui.card_header("Passenger Data")

        @render.data_frame
        def passenger_data():
            cols = [
                "class",
                "sex",
                "age",
                "sibsp",
                "parch",
                "fare",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


@reactive.calc
def filtered_df():
    filt_df = sns.load_dataset("titanic")
    filt_df = filt_df[filt_df["class"].isin(input.ticket_class())]
    filt_df = filt_df[filt_df["sex"].isin(input.sex())]
    filt_df = filt_df.loc[filt_df["age"] < input.age()]
    return filt_df


