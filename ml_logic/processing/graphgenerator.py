import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TideGraphGenerator:

    def __init__(self, tides_x, tides_y):
        self.tides_x = tides_x
        self.tides_y = tides_y
        self.plot = self.create_tide_graphs()

    def create_tide_graphs(self, relevant_levels = [8, 11]):

        fig = make_subplots()

        # Fill between relevant levels
        fig.add_trace(go.Scatter(x=self.tides_x + self.tides_x[::-1],
                                 y=[relevant_levels[0]]*len(self.tides_x) + [relevant_levels[1]]*len(self.tides_x),
                                 fill='toself',
                                 fillcolor='rgba(199, 238, 255, 0.5)',
                                 line=dict(color='rgba(255,255,255,0)'),
                                 showlegend=False,
                                 hoverinfo='skip'))

        # Plot the main tide line
        fig.add_trace(go.Scatter(x = self.tides_x, y = self.tides_y,
                                 mode ='lines', name = 'hauteur',
                                 line = dict(color = '#0B4C82', width = 2),
                                 showlegend = False,
                                 hovertemplate='%{x|%H:%M}<br>%{y:.2f}m'))

        # Show relevant tide levels for surf
        for level in relevant_levels:
            intersections = []
            for i in range(1, len(self.tides_y)):
                if (self.tides_y[i-1] < level <= self.tides_y[i]) or (self.tides_y[i-1] > level >= self.tides_y[i]):
                    x_interp = self.tides_x[i-1] + (self.tides_x[i] - self.tides_x[i-1]) * ((level - self.tides_y[i-1]) / (self.tides_y[i] - self.tides_y[i-1]))
                    intersections.append((x_interp, level))
                    text_position = 'top center' if level == 7.5 else 'bottom center'
                    fig.add_trace(go.Scatter(x=[x_interp], y=[level], mode='markers+text',
                                             text=[f'<br>{x_interp.strftime("%H:%M")}<br>'],
                                             textposition=text_position,
                                             marker=dict(color='#0B4C82', size=7),
                                             showlegend=False,
                                             hoverinfo='skip'))

        # Finetune formatting
        fig.update_yaxes(tickformat=',.0f', range=[max(min(self.tides_y), 0) - 0.5, max(self.tides_y) + 0.5])
        fig.update_xaxes(tickformat='%Hh', dtick=3600000)

        fig.update_layout(
            font=dict(family="Quicksand, sans-serif", size=14, weight="bold"),
            xaxis=dict(showgrid=True, gridcolor='#F2EFEF', tickcolor='gray', linecolor='lightgrey'),
            yaxis=dict(showgrid=True, gridcolor='#F2EFEF', tickcolor='gray', linecolor='lightgrey', ticksuffix='m'),
            plot_bgcolor='rgba(255, 255, 255, 1)',
            showlegend=False,
            margin=dict(l=10, r=10, t=20, b=10),
            width=840,
            height=400,
            #height=265,
            paper_bgcolor='rgba(0,0,0,0)'
            )

        return fig
