from math import sin

import dearpygui.dearpygui as dpg

# todo : use init files to preserv the state between sessions
# todo : add window to inform on the data being used ("connected") + menu to connect


class Plot:
    def __init__(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title="Custom Plot", width=1000, height=600)
        return

    def open(self, path: str, prefix: str):

        # access data files

        # create dpg window
        self.__create_window()

        return

    def __create_window(self):
        dpg.setup_dearpygui()
        dpg.show_viewport()

        # ? where to create the menu
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Figures"):
                dpg.add_menu_item(label="Time series", callback=self.plot)

        dpg.start_dearpygui()
        dpg.destroy_context()
        return

    def plot(self):

        # creating data
        sindatax = []
        sindatay = []
        for i in range(0, 500):
            sindatax.append(i / 1000)
            sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))

        with dpg.window(label="Plot", height=400, width=800):
            # create plot
            with dpg.plot(label="Title of the plot", height=360, width=740):
                # optionally create legend
                dpg.add_plot_legend()

                # REQUIRED: create x and y axes
                dpg.add_plot_axis(dpg.mvXAxis, label="x")
                dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

                # series belong to a y axis
                dpg.add_line_series(sindatax, sindatay, label="data", parent="y_axis")


plt = Plot()
plt.open(path="data/", prefix="test")
