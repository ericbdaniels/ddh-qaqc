import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent

readme_text = dbc.Container(
    [
        dcc.Markdown("# DDH-QAQC: Simple Drill Hole Data Exploration and QAQC"),
        html.Hr(),
        dcc.Markdown(
            """
    ### File Requirements
    
    > #### ASSAY Required Columns
    >  * *DHID* - Drill hole id. Integer values only
    >  * *FROM* - Depth values describing the top of each interval. All values must be numeric.
    >  * *TO* - Depth values describing the bottom of each interval. All values must be numeric.
    
    > #### COLLAR Required Columns
    >  * *DHID* - Drill hole id. Integer values only
    >  * *X* - Easting Coordinate. All values must be numeric.
    >  * *Y* - Northing Coordinate. All values must be numeric.
    >  * *Z* - Elevation Coordinate. All values must be numeric.

    > #### SURVEY Required Columns
    >  * *DHID* - Drill hole id. Integer values only
    >  * *DEPTH* - Down hole depth. All values must be numeric.
    >  * *AZIMUTH* - Azimuth. All values must be numeric from 0 to 360
    >  * *DIP* - Dip. All values must be numeric from -90 to 90.
    """
        ),
    ]
)
