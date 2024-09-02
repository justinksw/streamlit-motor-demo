import plotly.graph_objects as go


class Plot:

    @staticmethod
    def line_fig(x, y, **kwargs):

        if not isinstance(y, list):
            y = [y]

        # "label / name" of each y
        _labels = kwargs.get('label', [None for i in y])

        _title = kwargs.get('title')
        _xlabel = kwargs.get('xlabel')
        _ylabel = kwargs.get('ylabel')

        _mode = kwargs.get('mode', 'lines')  # markers lines

        _fontsize = kwargs.get('fontsize', 16)

        _xticks_val = kwargs.get('xticks_val')
        _xticks_label = kwargs.get('xticks_label')

        xticks_dict = dict()
        if _xticks_val:
            xticks_dict = dict(
                showgrid=True,
                tickmode='array',
                tickvals=_xticks_val,
                ticktext=_xticks_label,
                tickfont=dict(
                    size=_fontsize,
                ),
            )

        fig = go.Figure()

        for i in range(len(y)):
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y[i],
                    name=_labels[i],
                    mode=_mode,
                )
            )

        fig.update_layout(

            title=dict(
                text=_title,
                font=dict(size=_fontsize+2),
            ),

            xaxis_title=dict(
                text=_xlabel,
                font=dict(
                    size=_fontsize,
                ),
            ),

            yaxis_title=dict(
                text=_ylabel,
                font=dict(
                    size=_fontsize,
                ),
            ),

            xaxis=xticks_dict,
            yaxis=dict(
                tickfont=dict(
                    size=_fontsize,
                ),
            ),

        )

        return fig
