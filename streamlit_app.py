import json
import pytz
from copy import deepcopy
from datetime import datetime

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(layout="centered")


class Datafile:
    def __init__(self, file) -> None:
        # file object: uploaded from streamlit file upload function
        data_str = file.getvalue()
        self.data_json = json.loads(data_str)

        self.ts = datetime.fromtimestamp(
            int(int(file.name.split(".")[0])/1000)
        )
        # .replace(tzinfo=pytz.utc)

    def get_timestamp_unix(self):
        return self.ts

    def get_timestamp_utc_hk(self):
        ts_hk = self.ts.astimezone(pytz.timezone('Asia/Hong_Kong'))
        return ts_hk

    def get_device_id(self):
        return self.data_json["sensor_data"]["mac_address"]

    def get_battery_value(self):
        return self.data_json["battery_per"]

    def get_connection_value(self):
        return self.data_json["rssi"]

    def get_data_df(self):
        # json -> df
        data_df = pd.DataFrame(self.data_json["sensor_data"]["data"])
        # transpose
        data_df_T = data_df.T
        # add an index column
        data_df_T["index"] = list(range(len(data_df_T)))

        return data_df_T


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
                st.metric(
                    label="Device", value=datafile.get_device_id())

            with col2:
                st.metric(
                    label="rssi", value=datafile.get_connection_value())

            with col3:

                st.metric(
                    label="Battery", value=datafile.get_battery_value())

        # == Row 3 == #

        data_df = datafile.get_data_df()

        container = st.container(height=None, border=True)
        with container:
            st.line_chart(data_df, x="index")

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

        st.write(dff)

        fig, ax = plt.subplots()  # figsize=(6, 3)
        ax.grid()
        ax.plot(_x, dff["connection"], marker="o", markersize=None)
        ax.set_xticks(ticks=_x, labels=dff["time"])
        ax.set_ylabel("Rssi value")
        ax.set_xlabel("Time")
        ax.set_title(f"Device: {device}")

        st.pyplot(fig, use_container_width=True)

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
