import json

import pandas as pd
import streamlit as st


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

            data_str = self.file.getvalue()
            data_json = json.loads(data_str)

            df = pd.DataFrame(data_json["data"])

            df_T = df.T

            df_T["index"] = list(range(len(df_T)))

            # st.write(df_T)

            container = st.container(height=None, border=True)
            with container:

                st.line_chart(df_T, x="index")

        return None


analysis = Analysis()
analysis.display()
