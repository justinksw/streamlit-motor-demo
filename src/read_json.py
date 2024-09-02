import json
import pytz
from datetime import datetime

import pandas as pd


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
