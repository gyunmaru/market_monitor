# %%
import yfinance as yf
import plotly as py
from plotly.offline import init_notebook_mode, iplot
from plotly.tools import FigureFactory as FF
import os
import pandas as pd
import plotly.graph_objects as go
import base64
from xhtml2pdf import pisa

# %%

"""
functions 
"""


def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        source_html,                # the HTML to convert
        dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err


# %%
tickers = ['^GSPC', '^FTSE', '^HSI', '^N225',
           '^VIX',
           '^FVX', '^TNX', '^TYX',
           'BTC-USD', 'ETH-USD']

# %%
if not os.path.exists("./dled_data.csv"):
    data = yf.download(
        tickers=' '.join(tickers),
        period='1y',
        interval='1d',
        group_by='ticker',
        auto_adjust=True,
    )
    data.to_csv("./dled_data.csv")
else:
    data = pd.read_csv("./dled_data.csv", header=[0, 1],
                       skipinitialspace=True, index_col=0)

fetchd_tickers = data.columns.get_level_values(0).drop_duplicates()
data.iloc[:5, :5]

# %%

figures = []
for ft in tickers:
    df = data[[ft]].droplevel(0, axis=1)
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])]
                    )
    fig.update_layout(
        title=ft,
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="RebeccaPurple"
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    figures.append(fig)

    # fig.show()

# %%

width = 600
height = 300

template = (''
            '<img style="width: {width}; height: {height}"'
            ' src="data:image/png;base64,{image}">'
            # Optional caption to include below the graph
            # '{caption}'
            # '<br>'
            '<hr>'
            '')

# A collection of Plotly graphs
# figures

# Generate their images using `py.image.get`
images = [base64.b64encode(
    py.io.to_image(figure, width=width, height=height)
).decode('utf-8') for figure in figures]

report_html = ''
for image in images:
    _ = template
    _ = _.format(image=image,  width=width, height=height)
    report_html += _

# display(HTML(report_html))
convert_html_to_pdf(report_html, 'report-2.pdf')
