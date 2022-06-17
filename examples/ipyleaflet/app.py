import ipyleaflet as L
from htmltools import css
from ipyshiny import output_widget, reactive_read, register_widget
from shiny import App, Inputs, Outputs, Session, reactive, render, ui

app_ui = ui.page_fluid(
    ui.div(
        ui.input_slider("zoom", "Map zoom level", value=4, min=1, max=18),
        ui.output_ui("map_bounds"),
        style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
        ),
    ),
    output_widget("map"),
)


def server(input: Inputs, output: Outputs, session: Session):

    # Initialize and display when the session starts (1)
    map = L.Map(center=(52, 360), zoom=4)
    register_widget("map", map)

    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    # When zooming directly on the map, update the slider's value (2 and 3)
    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

    # Everytime the map's bounds change, update the output message (3)
    @output
    @render.ui
    def map_bounds():
        center = reactive_read(map, "center")
        if len(center) == 0:
            return

        lat = dms2str(dec2dms(center[0]))
        lon = dms2str(dec2dms(center[1]))

        return ui.p(f"Latitude: {lat}", ui.br(), f"Longitude: {lon}")


def dec2dms(x: float):
    is_positive = x >= 0
    x = abs(x)
    minutes, seconds = divmod(x * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    return (degrees, minutes, seconds)


def dms2str(dms: tuple[float, float, float], digits: int = 2):
    return f"{round(dms[0])}\u00b0 {round(dms[1])}' {round(dms[2], digits)}''"


app = App(app_ui, server)