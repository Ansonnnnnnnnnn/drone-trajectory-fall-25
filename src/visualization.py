"""Utility to visualize photo plans.
"""
import numpy as np
import typing as T
import plotly.graph_objects as go
from src.data_model import Waypoint


def plot_photo_plan(photo_plans: T.List[Waypoint]) -> go.Figure:
    """Plot the photo plan on a 2D grid.

    Args:
        photo_plans: List of waypoints for the photo plan.

    Returns:
        Plotly figure object.
    """
    x = [wp.x for wp in photo_plans]
    y = [wp.y for wp in photo_plans]
    hover_text = [
        f"x={wp.x}, y={wp.y}, z={wp.z}<br>speed={wp.speed}, yaw={wp.yaw}°"
        for wp in photo_plans
    ]

    fig = go.Figure()

    # Connect points with line
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers+text',
        text=[f"{i}" for i in range(len(photo_plans))],  # waypoint index
        textposition="top right",
        hovertext=hover_text,
        hoverinfo="text",
        line=dict(color='blue', width=2),
        marker=dict(size=8, color='red'),
        name="Drone Path"
    ))

    fig.update_layout(
        title="Drone Waypoints (2D Plot)",
        xaxis_title="X",
        yaxis_title="Y",
        showlegend=True,
        width=800,
        height=600,
        template="plotly_white"
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)  # Equal aspect ratio

    return fig
