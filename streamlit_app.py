import json
import pytz
from datetime import datetime

import pandas as pd
import streamlit as st


st.set_page_config(layout="wide")


class Analysis:
    def __init__(self) -> None:

        self.file = self.upload_file()

    def upload_file(self):
        container = st.container(height=None, border=True)

        with container:
            file = st.file_uploader(
                label="Upload a JSON File", label_visibility="visible")

        return file

    def display(self):

        if self.file is not None:

            ts = datetime.fromtimestamp(
                int(int(self.file.name.split(".")[0])/1000)).replace(tzinfo=pytz.utc)
            tz = pytz.timezone('Asia/Hong_Kong')
            ts_hk = ts.astimezone(tz)
            st.write(ts_hk)

            data_str = self.file.getvalue()
            data_json = json.loads(data_str)

            sensor_data_df = pd.DataFrame(data_json["sensor_data"]["data"])

            sensor_data_df_T = sensor_data_df.T

            sensor_data_df_T["index"] = list(range(len(sensor_data_df_T)))

            # st.write(df_T)

            container = st.container(height=None, border=True)
            with container:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(label="Battery", value=data_json["battery_per"])

                with col2:
                    st.metric(label="rssi", value=data_json["rssi"])

                with col3:
                    st.metric(label="Device",
                              value=data_json["sensor_data"]["mac_address"])

            container = st.container(height=None, border=True)
            with container:

                st.line_chart(sensor_data_df_T, x="index")

        return None


analysis = Analysis()
analysis.display()
