import numpy as np
import plotly.graph_objects as go

def create_plasticity_chart(LL, PI):

    # A-line and U-line
    LL_range = np.linspace(20, 100, 200)
    A_line = 0.73 * (LL_range - 20)
    U_line = 0.9 * (LL_range - 8)

    fig = go.Figure()

    # A-line
    fig.add_trace(go.Scatter(
        x=LL_range, y=A_line,
        mode='lines',
        name='A-line'
    ))

    # U-line
    fig.add_trace(go.Scatter(
        x=LL_range, y=U_line,
        mode='lines',
        name='U-line',
        line=dict(dash='dash')
    ))

    # LL = 50 vertical line
    fig.add_vline(x=50, line_dash="dot")

    # Soil point
    if LL is not None and PI is not None:
        fig.add_trace(go.Scatter(
            x=[LL],
            y=[PI],
            mode='markers',
            name='Soil Sample',
            marker=dict(size=10)
        ))

    fig.update_layout(
        title="Casagrande Plasticity Chart",
        xaxis_title="Liquid Limit (LL)",
        yaxis_title="Plasticity Index (PI)",
        xaxis=dict(range=[0, 100]),
        yaxis=dict(range=[0, 60]),
        height=600
    )

    return fig
