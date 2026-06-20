import streamlit as st  
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3


DB_PATH = "../db/weather_site.db"


def load_table(name):
    '''Load table from the database'''
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql(f"SELECT * FROM {name}", conn)  # noqa: S608 — table name is internal
    return df


def load_all():
    '''Creates dataframe for use in Streamlit'''
    tables = ["weather", "sun", "world_weather", "city_locations"]
    return {t: load_table(t) for t in tables}


def solar_noon_to_float(sn):
    '''Converts time to a float based on a scale that coincides with sun distance
    Time has a max of around 1:45, which equates to about 13.7 as calculated below'''
    sn = sn.split(' ')[0].split(':')
    if sn[0] == '1':
        sn[0] = '13'
    sn[1] = int(sn[1]) / 60
    sn = (int(sn[0]) + sn[1]) / .137
    print(sn)
    return sn


def plot_year_lines(df, years, x_col, y_col, title, markers=False):
    '''Plot multiple lines on graph'''
    subset = df[df['year'].isin(years)].copy()
    return px.line(subset, x=x_col, y=y_col, color='year', title=title, markers=markers)


def plot_sun_distance_with_temp_highs(sun_df, weather_df, year, show_temp_line=False):
    '''Set up the bar chart for sun distance as well as the option to add high temps'''
    sun_bar = px.bar(sun_df, x='date', y='mil_miles', title="Summer Sun's Distance From NYC")
    sun_bar.update_layout(yaxis_range=[93, 95], yaxis_title='Distance (million miles)')
    if show_temp_line:
        weather_year = weather_df[weather_df['year'] == year].copy()
        if not weather_year.empty:
            # Create the line graph to go on top of bar graph
            sun_bar.add_trace(go.Scatter(
                x=weather_year['full_date'],
                y=weather_year['temp_high'],
                mode='lines+markers',
                name=f'{year} temp_high',
                yaxis='y2'
            ))
            # Create labels to identify the line graph
            sun_bar.update_layout(
                yaxis2=dict(
                    title='Temp High (°F)',
                    overlaying='y',
                    side='right',
                )
            )
    return sun_bar


def city_locations_join():
    '''Join the city locations and world weather databases to compare temps to longitude
    and elevation of cities'''
    with sqlite3.connect(DB_PATH) as conn:
        query = """
        SELECT ww.city, ww.temp_in_F, cl.longitude_numeric, cl.elevation_numeric
        FROM world_weather ww
        LEFT JOIN city_locations cl ON cl.city = ww.city
        ORDER BY ww.city
        """
    df = pd.read_sql_query(query, conn)
    df.info()
    print(df.head())
    return df


data = load_all()
weather = data['weather']
sun = data['sun']
world_weather = data['world_weather']
city_locations = data['city_locations']

month_numerical = {
    'June': '06',
    'July': '07',
    'August': '08',
    'September': '09'
}

# Add columns to weather database to better set up the timeline on the graph
weather['month_day'] = weather['full_date'].apply(lambda x: x.split('-')[1] + '-' + x.split('-')[2])
weather.month_day = pd.to_datetime(weather.month_day, format='%m-%d').dt.strftime('%B-%d')
weather['month_numerical'] = weather.month_day.apply(lambda x: month_numerical[x.split('-')[0]])
weather_month = weather.groupby(['year', 'month_numerical'], as_index=False).agg({'temp_high': 'mean', 'temp_low': 'mean', 'wind': 'mean'})

# Create sidebar with selectors
st.sidebar.header('Weather Site App')
st.sidebar.subheader('NYC Summer Highs')
st.sidebar.markdown('Select the years you want to display in the charts. You can select multiple years to compare them against each other.')
selected_years = st.sidebar.multiselect(
    'Select Years',
    sorted(weather['year'].unique()),
    default='2015'
)
st.sidebar.subheader('NYC Sun Distance & Solar Noon')
st.sidebar.markdown('Select the year you want to display in the charts.')
selected_year = st.sidebar.selectbox('Select Year', sorted(weather['year'].unique()))
show_temp_line = st.sidebar.checkbox('Overlay selected year temp_high line on the bar chart', value=False)
selected_year_sun_data = sun[sun['year'] == selected_year]
st.sidebar.subheader('World Temps')
long_elev_switch = st.sidebar.checkbox('Switch between Longitude and Elevation', value=False)

tab1, tab2, tab3 = st.tabs([
    "NYC Summer Temperature Highs",
    "NYC Sunlight",
    "Current World Temperatures",
])


# Add charts to tabs. Use the above functions to generate the plots
with tab1:
    line_chart = plot_year_lines(
        weather,
        selected_years,
        x_col='month_day',
        y_col='temp_high',
        title='NYC Summer Temperature Highs'
    )
    line_chart.update_layout(xaxis={'title': 'NYC Summer Months'}, yaxis={'title': 'Temperature Highs'})
    st.plotly_chart(line_chart)

    line_chart_2 = plot_year_lines(
        weather_month,
        selected_years,
        x_col='month_numerical',
        y_col='temp_high',
        title='Monthly Average NYC Summer Temperature Highs',
        markers=True
    )
    line_chart_2.update_layout(xaxis={'title': 'NYC Summer Months'}, yaxis={'title': 'Average High Temp'})
    st.plotly_chart(line_chart_2)

# Adjust the sun table to sort info needed for bar graphs
sun_length_distance = selected_year_sun_data.sort_values(by='length', ascending=True)
sun_solar_noon = selected_year_sun_data
sun_solar_noon.solar_noon = sun_solar_noon.solar_noon.apply(lambda x: solar_noon_to_float(x))
sun_solar_noon = sun_solar_noon.sort_values('solar_noon', ascending=True)
sun_solar_noon.mil_miles = sun_solar_noon.mil_miles.apply(lambda x: float(x)).astype(float, 2)


with tab2:
    bar_chart = plot_sun_distance_with_temp_highs(
        selected_year_sun_data,
        weather,
        selected_year,
        show_temp_line=show_temp_line,
    )
    st.plotly_chart(bar_chart)

    bar_chart_2 = px.bar(sun_solar_noon, x='date', y=['mil_miles', 'solar_noon'], 
                       barmode='group', title="Solar Noon Vs. Sun's Distance",
                       labels={'date': 'Summer Date', 'value': 'Sun: Million of Miles, Solar Noon: Percentage Max 1:45'}).update_layout(yaxis_range=[93, 96])
    bar_chart_2.update_layout(yaxis_range=[93, 96])
    st.plotly_chart(bar_chart_2)

city_joined = city_locations_join()

# Create logic to switch between elevation and longitude comparison. Scatter plot for current temps
if long_elev_switch:
    xval = 'elevation_numeric'
else:
    xval = 'longitude_numeric'
with tab3:
    world_temps = px.scatter(city_joined, x=xval, y='temp_in_F', color='city',
    title="Current World Temps Along Lines Of Latitude", hover_data=["temp_in_F"],
    labels={'longitude_numeric': 'Longitude', 'elevation_numeric': 'Elevation', 'temp_in_F': 'Temperature in Farenheit'})
    st.plotly_chart(world_temps)
