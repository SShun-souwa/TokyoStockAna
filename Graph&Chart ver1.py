import numpy as np
import plotly.graph_objs as go
#from plotly import graph_objs as go

xs = np.linspace(0, 10, 100)
sins = np.sin(xs)
randoms = np.random.rand(100)

fig = go.Figure(data=[
    go.Scatter(x=xs, y=sins, name="sin"),
    go.Scatter(x=xs, y=randoms, name="random"),
])

fig.show()