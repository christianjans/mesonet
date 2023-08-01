import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from activity_analyzer import MasksManager
from chan_lab.helpers.image_series_collection import (
    ImageSeriesCollection,
    ImageSeriesCollectionArgs,
)

PUPIL_EVENT_FRAME = 313
MESOSCALE_EVENT_FRAME = 88
PUIPIL_FILENAME = "/Users/christian/Downloads/fc2_save_2023-02-09-135224-0000.avi"
MESOSCALE_FILENAME = "/Users/christian/Documents/summer2023/matlab/my_data/flash1/02_awake_8x8_30hz_36500fr_FR30Hz_BPF1-5Hz_GSR_DFF0-G4-fr1-36480_FR30Hz_BPF1-5Hz_GSR_DFF0-G4-fr1-36480.raw"
PUPIL_START_FRAME_INDEX = PUPIL_EVENT_FRAME - MESOSCALE_EVENT_FRAME + 1 - 1

PUPIL_EVENT_FRAME = 0
MESOSCALE_EVENT_FRAME = 0
PUPIL_FILENAME = ""
MESOSCALE_FILENAME = "/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_eye-r/imMean.mat"
PUPIL_START_FRAME_INDEX = PUPIL_EVENT_FRAME - MESOSCALE_EVENT_FRAME + 1 - 1

ISOFLURANE_ARGS = [
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_eye-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_fl-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_hl-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_whisker-l/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_eye-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_fl-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_hl-r/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
    ImageSeriesCollectionArgs(
        file="/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_whisker-l/imMean.mat",
        fps=30.0,
        image_width=256,
        image_height=256,
        frame_index_offset=0,
        kwargs={"property": "imMean", "transpose_axes": (2, 0, 1)},
    ),
]
ISOFLURANE_REGION_POINTS = [
    "/Users/christian/Documents/summer2023/MesoNet/mesonet_outputs/isoflurane1_mouse6_eye-r_atlas_brain/dlc_output/region_points.pkl",
    "/Users/christian/Documents/summer2023/MesoNet/mesonet_outputs/isoflurane1_mouse6_fl-r_atlas_brain/dlc_output/region_points.pkl",
    "/Users/christian/Documents/summer2023/MesoNet/mesonet_outputs/isoflurane1_mouse6_hl-r_atlas_brain/dlc_output/region_points.pkl",
    "/Users/christian/Documents/summer2023/MesoNet/mesonet_outputs/isoflurane1_mouse6_whisker-l_atlas_brain/dlc_output/region_points.pkl",
    "/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_eye-r/Eye_R.mat",
    "/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_fl-r/HL_R.mat",
    "/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_hl-r/HL_R.mat",
    "/Users/christian/Documents/summer2023/matlab/my_data/isoflurane1_mouse6_whisker-l/HL_R.mat",
]
ISOFLURANE_TITLES = [
    "Eye-R MesoNet",
    "FL-R MesoNet",
    "HL-R MesoNet",
    "Whisker-L MesoNet",
    "Eye-R MATLAB",
    "FL-R MATLAB",
    "HL-R MATLAB",
    "Whisker-L MATLAB",
]
ISOFLURANE_ROWS = 2


class Controller:
    pass


class View(ttk.Frame):
    def __init__(self,
                 parent: tk.Tk,
                 mesoscale_filename: str,
                 pupil_filename: str):
        super().__init__(parent)

        self.n_plots = len(ISOFLURANE_ARGS)
        assert self.n_plots % ISOFLURANE_ROWS == 0
        self.collection = ImageSeriesCollection(ISOFLURANE_ARGS[0],
                                                *ISOFLURANE_ARGS[1:])
        self.masks = []
        for i, region_points_file in enumerate(ISOFLURANE_REGION_POINTS):
            masks_manager = MasksManager(region_points_file,
                                         ISOFLURANE_ARGS[i].image_width,
                                         ISOFLURANE_ARGS[i].image_height)
            mask = np.logical_or.reduce(masks_manager.masks)
            mask = np.ma.masked_where(mask == 0, mask)
            self.masks.append(mask)

        self.min_slider_value = 1
        self.max_slider_value = 201
        self.slider_value = self.min_slider_value

        self.slider_label = ttk.Label(self, text="")
        self.slider_label.grid(row=0, column=0)

        self.slider = ttk.Scale(self,
                                from_=self.min_slider_value,
                                to=self.max_slider_value,
                                command=self.slider_changed,
                                value=self.slider_value,
                                length=600)
        self.slider.grid(row=1, column=0, sticky=tk.EW)
        self.grid_rowconfigure(1, weight=1)

        parent.bind("<Left>", lambda _: self.slider.set(self.slider.get() - 1))
        parent.bind("<Right>", lambda _: self.slider.set(self.slider.get() + 1))

        self.plots = []
        self.figure = Figure(figsize=(200, 100), dpi=5)
        for i in range(self.n_plots):
            self.plots.append(self.figure.add_subplot(
                    ISOFLURANE_ROWS, self.n_plots // ISOFLURANE_ROWS, i + 1))
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.get_tk_widget().grid(row=2, column=0)

        self.slider_changed(str(self.slider_value))

        # self.mesoscale_image_series = ImageSeriesCreator.create(
        #         mesoscale_filename, 256, 256, "all", property="imMean",
        #         transpose_axes=(2, 0, 1))
        # self.pupil_video_series = VideoSeries(pupil_filename)
        # self.min_slider_value = 1 + PUPIL_START_FRAME_INDEX
        # self.max_slider_value = self.mesoscale_image_series.image_array.shape[0]
        # self.slider_value = self.min_slider_value

        # self.slider_label = ttk.Label(self, text="")
        # self.slider_label.grid(row=0, column=0)

        # self.slider = ttk.Scale(self,
        #                         from_=self.min_slider_value,
        #                         to=self.max_slider_value,
        #                         command=self.slider_changed,
        #                         value=self.slider_value,
        #                         length=600)
        # self.slider.grid(row=1, column=0, sticky=tk.EW)
        # self.grid_rowconfigure(1, weight=1)

        # parent.bind("<Left>", lambda _: self.slider.set(self.slider.get() - 1))
        # parent.bind("<Right>", lambda _: self.slider.set(self.slider.get() + 1))

        # self.figure = Figure(figsize=(200, 100), dpi=5)
        # self.plot1 = self.figure.add_subplot(1, 2, 1)
        # self.plot1.imshow(self.mesoscale_image_series.get_frame(self.slider_value - self.min_slider_value))
        # self.plot2 = self.figure.add_subplot(1, 2, 2)
        # self.plot2.imshow(self.pupil_video_series.get_frame(self.slider_value - 1))
        # self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        # self.canvas.get_tk_widget().grid(row=2, column=0)

        # self.slider_changed(str(self.slider_value))

    def slider_changed(self, value: str):
        self.slider_value = int(float(value))

        # label_text = (
        #     f"Frame {self.slider_value}/{self.max_slider_value} "
        #     f"({self.slider_value / self.pupil_video_series.fps:.3f} s)"
        # )
        label_text = (
            f"Frame {self.slider_value}/{self.max_slider_value} "
            f"({self.slider_value / 30.0:.3f} s)"
        )
        self.slider_label.config(text=label_text)

        images = self.collection.get_frames(self.slider_value - 1)
        for i in range(self.n_plots):
            self.plots[i].clear()
            self.plots[i].set_title(ISOFLURANE_TITLES[i])
            self.plots[i].imshow(images[i])
            self.plots[i].imshow(self.masks[i], alpha=0.3, cmap="autumn")

        self.canvas.draw()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Event Analyzer App")

        view = View(self, MESOSCALE_FILENAME, PUIPIL_FILENAME)
        view.grid(row=0, column=0, padx=10, pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
