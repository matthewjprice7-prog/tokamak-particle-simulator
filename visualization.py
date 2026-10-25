"""
3D visualization for the Fusion Simulator.

Uses Plotly for interactive 3D rendering of particle trajectories,
reactor geometry, and magnetic field lines. Each plotting function
takes numpy arrays (produced by the simulator) and returns an
interactive Plotly figure that opens in your browser.

Plotly renders using WebGL in the browser -- you can rotate, zoom,
and pan the 3D view with your mouse.
"""

import numpy as np
import plotly.graph_objects as go


def plot_orbit(r, title="Particle Orbit", show_markers=True):
    """
    Plot a 3D particle trajectory.

    Parameters
    ----------
    r : numpy array, shape (N, 3)
        Particle positions over time. Each row is [x, y, z].
    title : str
        Title for the plot.
    show_markers : bool
        If True, mark the start (green) and end (red) of the trajectory.

    Returns
    -------
    plotly.graph_objects.Figure
        Interactive 3D figure. Call fig.show() to open in browser.
    """
    # The main trajectory line
    # Scatter3d with mode='lines' draws a connected 3D line through all points
    orbit_trace = go.Scatter3d(
        x=r[:, 0], y=r[:, 1], z=r[:, 2],
        mode='lines',
        line=dict(color='blue', width=2),
        name='Orbit'
    )

    traces = [orbit_trace]

    if show_markers:
        # Start point (green)
        start_trace = go.Scatter3d(
            x=[r[0, 0]], y=[r[0, 1]], z=[r[0, 2]],
            mode='markers',
            marker=dict(size=5, color='green'),
            name='Start'
        )
        # End point (red)
        end_trace = go.Scatter3d(
            x=[r[-1, 0]], y=[r[-1, 1]], z=[r[-1, 2]],
            mode='markers',
            marker=dict(size=5, color='red'),
            name='End'
        )
        traces.extend([start_trace, end_trace])

    # Build the figure with all traces
    fig = go.Figure(data=traces)

    # Configure the 3D layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (m)',
            yaxis_title='Y (m)',
            zaxis_title='Z (m)',
            # Equal aspect ratio so the helix isn't distorted
            aspectmode='data'
        ),
        # Legend in top-right corner
        legend=dict(x=0.85, y=0.95)
    )

    return fig


def save_figure(fig, filename="orbit.html"):
    """
    Save a Plotly figure as a standalone HTML file.

    The HTML file can be opened in any browser -- no Python required.
    Useful for sharing results or keeping a record of a simulation run.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The figure to save.
    filename : str
        Output filename (should end in .html).
    """
    fig.write_html(filename)
    print(f"Saved interactive plot to {filename}")

    # ------------------------------------------------------------
# Tokamak torus mesh
# ------------------------------------------------------------

def _make_torus_mesh(R, a, n_toroidal=60, n_poloidal=30, opacity=0.15):
    """
    Generate a torus mesh for tokamak visualization.
    """

    phi = np.linspace(0, 2*np.pi, n_toroidal)
    theta = np.linspace(0, 2*np.pi, n_poloidal)

    phi, theta = np.meshgrid(phi, theta)

    phi = phi.flatten()
    theta = theta.flatten()

    # Parametric torus equations
    x = (R + a*np.cos(theta)) * np.cos(phi)
    y = (R + a*np.cos(theta)) * np.sin(phi)
    z = a*np.sin(theta)

    # Triangle indices
    i_indices = []
    j_indices = []
    k_indices = []

    for ti in range(n_poloidal - 1):
        for pi in range(n_toroidal - 1):

            p0 = ti * n_toroidal + pi
            p1 = ti * n_toroidal + (pi + 1)
            p2 = (ti + 1) * n_toroidal + pi
            p3 = (ti + 1) * n_toroidal + (pi + 1)

            i_indices.extend([p0, p0])
            j_indices.extend([p1, p2])
            k_indices.extend([p2, p3])

    torus_trace = go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=i_indices,
        j=j_indices,
        k=k_indices,
        opacity=opacity,
        color='lightblue',
        name='Tokamak Vessel'
    )

    return torus_trace


# ------------------------------------------------------------
# Plot orbit + tokamak
# ------------------------------------------------------------

def plot_tokamak(r, R, a, title="Particle Orbit in Tokamak"):

    # Get orbit traces
    orbit_fig = plot_orbit(r, title=title)

    traces = list(orbit_fig.data)

    # Add torus
    torus_trace = _make_torus_mesh(R, a)

    traces.append(torus_trace)

    # Build final figure
    fig = go.Figure(data=traces)

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='X (m)',
            yaxis_title='Y (m)',
            zaxis_title='Z (m)',
            aspectmode='data'
        )
    )

    return fig
