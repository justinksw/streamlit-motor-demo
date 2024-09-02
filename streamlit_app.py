import numpy as np
import pandas as pd
import streamlit as st

from src.read_json import Datafile
from src.plot import Plot

st.set_page_config(layout="centered")


class Index:
    def __init__(self) -> None:
        st.title("Upload File(s) to Start")
        st.write("")
        self.files = self.upload_file()

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            files = st.file_uploader(
                label="Upload **one or multiple** JSON File(s)",
                type="json",
                accept_multiple_files=True,
                label_visibility="visible"
            )
        return files

    def display_single_file(self, file):
        # == Load file == #
        datafile = Datafile(file)

        # == Row 1 == #
        st.write(datafile.get_timestamp_utc_hk())

        # == Row 2 == #
        container = st.container(height=None, border=True)
        with container:
            col1, col2, col3 = st.columns([0.65, 0.15, 0.2])

            with col1:
                st.metric(label="Device", value=datafile.get_device_id())
            with col2:
                st.metric(label="rssi", value=datafile.get_connection_value())
            with col3:
                st.metric(label="Battery", value=datafile.get_battery_value())

        # == Row 3 == #
        data_df = datafile.get_data_df()

        container = st.container(height=None, border=True)

        with container:

            _x = list(range(len(data_df)))

            y = [
                data_df["x"],
                data_df["y"],
                data_df["z"],
            ]

            labels = ["X", "Y", "Z"]

            plot = Plot()

            fig = plot.line_fig(
                x=_x,
                y=y,
                label=labels,
                title=f"Triaxial data",
                xlabel="Sample point number",
                ylabel="Acceleration [g]",
            )

            st.plotly_chart(fig)

        return None

    def get_multiple_file_df(self):
        data = {
            "filename": [],
            "devices": [],
            "ts": [],
            "connection": [],
        }

        for f in self.files:
            datafile = Datafile(f)
            data["filename"].append(f.name.split(".")[0])
            data["devices"].append(datafile.get_device_id())
            data["ts"].append(datafile.get_timestamp_utc_hk())
            data["connection"].append(datafile.get_connection_value())

        df = pd.DataFrame(data)
        df = df.sort_values(by=["ts"])

        df['time'] = pd.to_datetime(df['ts']).dt.time

        # prevent upload same files multiple times
        df = df.drop_duplicates(subset=["filename"], keep="last")

        return df

    def display_multiple_file(self):

        st.write("")
        st.title("Multiple files")

        df = self.get_multiple_file_df()

        devices = df["devices"].unique()

        device = st.selectbox(
            label="There may be multiple devices",
            options=devices
        )

        dff = df[df["devices"] == device]

        _x = list(range(len(dff)))

        plot = Plot()

        fig = plot.line_fig(
            x=_x,
            y=dff["connection"],
            title=f"Device: {device}",
            xlabel="Time",
            ylabel="Rssi value",
            xticks_val=_x,
            xticks_label=dff["time"],
            mode="lines+markers"
        )

        st.plotly_chart(fig)

        return None

    def display(self):

        if self.files:

            if len(self.files) == 1:
                self.display_single_file(self.files[0])

            elif len(self.files) > 1:
                self.display_multiple_file()

        return None


index = Index()
index.display()
