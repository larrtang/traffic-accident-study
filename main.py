import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression


def save_LA_data():
    daily_weather = pd.read_csv("LA Chi Daily Weather Temp Max Min Precip.csv")
    daily_weather['Date'] = pd.to_datetime(daily_weather['Date'])
    #chi_accidents = pd.read_csv("Chicago Traffic_Crashes_-_Crashes Weather.csv")
    la_accidents = pd.read_csv("LA Traffic_Collision_Data_from_2010_to_Present.csv")
    la_accidents['Date Occurred'] = pd.to_datetime(la_accidents['Date Occurred'])
    #print(daily_weather)

    date_range = pd.date_range(start='1/1/2012', end='10/10/2015')
    weather = daily_weather.loc[daily_weather['Date'] == date_range[0]]
    print(weather)

    num_accidents = []
    avg_temps = []
    precip = []

    for date in date_range:
        #print(date)
        num_accidents_onday = len(la_accidents.loc[la_accidents['Date Occurred'] == date].index)
        num_accidents.append(num_accidents_onday)

        weather = daily_weather.loc[daily_weather['Date'] == date]
        print(weather)
        avg_temps.append((float(weather.iloc[0]["Los Angeles; Temperature (max)"])+float(weather.iloc[0]["Los Angeles; Temperature (min)"]))/2.0)
        precip.append(float(weather.iloc[0]["Los Angeles; Precipitation"]))

    la_data = pd.DataFrame(data={'Date':date_range, 'num_accidents': num_accidents, 'avg_temp': avg_temps, 'precipitation': precip})

    print(la_data)
    la_data.to_csv('LA_2012-2015_data.csv')

def save_CHI_data():
    daily_weather = pd.read_csv("LA Chi Daily Weather Temp Max Min Precip.csv")
    daily_weather['Date'] = pd.to_datetime(daily_weather['Date'])
    #chi_accidents = pd.read_csv("Chicago Traffic_Crashes_-_Crashes Weather.csv")
    chi_accidents2012 = pd.read_csv("Chicago 2012 CrashExtract.csv", parse_dates=True, error_bad_lines=False)
    chi_accidents2013 = pd.read_csv("Chicago 2013 CrashExtract.csv", parse_dates=True, error_bad_lines=False)
    chi_accidents2014 = pd.read_csv("Chicago 2014 CrashExtract.csv", parse_dates=True, error_bad_lines=False)
    chi_accidents2015 = pd.read_csv("Chicago 2015 CrashExtract.csv", parse_dates=True, error_bad_lines=False)
    chi_accidents = []
    chi_accidents.append(chi_accidents2012)
    chi_accidents.append(chi_accidents2013)
    chi_accidents.append(chi_accidents2014)
    chi_accidents.append(chi_accidents2015)
    #for c in chi_accidents:
    #    print c.iloc[:,37], c.iloc[:,51]
    #print chi_accidents.columns
    #print chi_accidents['CRASH_DATE']

    #print chi_accidents['CRASH_DATE_EST_I']
    #return 
    #chi_accidents['CRASH_DATE'] = pd.to_datetime(chi_accidents['CRASH_DATE']).dt.date
    #print chi_accidents['CRASH_DATE']
    date_range = ['{dt.month}/{dt.day}/{dt.year}'.format(dt = d) for d in pd.date_range(start='1/20/2012', end='10/10/2015', freq='D').date]
    #weather = daily_weather.loc[daily_weather['Date'] == date_range[9]]
    #print date_range[9]
    #print chi_accidents.loc[chi_accidents['CRASH_DATE'] == date_range[9]]

    num_accidents = []
    avg_temps = []
    precip = []

    for date in date_range:
        print(date)
        num_accidents_onday = 0
        for a in chi_accidents:
            chi = pd.DataFrame(a.loc[a.iloc[:,51] == 'Chicago'])
            num_accidents_onday += len(chi.loc[chi.iloc[:,37] == date].index)
        print num_accidents_onday
        num_accidents.append(num_accidents_onday)

        weather = daily_weather.loc[daily_weather['Date'] == date]
        #print(weather)
        avg_temps.append((float(weather.iloc[0]["Chicago; Temperature (max)"])+float(weather.iloc[0]["Chicago; Temperature (min)"]))/2.0)
        precip.append(float(weather.iloc[0]["Chicago; Precipitation"]))

    chi_data = pd.DataFrame(data={'Date':date_range, 'num_accidents': num_accidents, 'avg_temp': avg_temps, 'precipitation': precip})

    #print(chi_data)
    chi_data.to_csv('chi_2012-2015_data.csv')




def plot_LA_data():
    data = pd.read_csv("LA_2012-2015_data.csv")
    data = data.loc[data['precipitation'] > 0]
    plt.figure(figsize=(11,9))
    
    plt.title('Precipitation and Accidents Over Time')
    plt.plot(data['Date'], data['num_accidents'], 'b', label='# accidents')
    plt.plot(data['Date'], data['avg_temp'], 'g', label='average Temp (C)')
    plt.plot(data['Date'], data['precipitation'], 'r', label='precipitation',linewidth=2.0)
    plt.legend()
    plt.show()

def plot_LA_data_scatter():
    data = pd.read_csv("LA_2012-2015_data.csv")
    data = data.loc[data['precipitation'] > 0]
    plt.figure(figsize=(11,9))
    X = pd.DataFrame(data['precipitation'])
    Y = pd.DataFrame(data['num_accidents'])
    
    model = LinearRegression()
    model.fit(X, Y)
    line = model.predict(X)
    plt.scatter(data['precipitation'], data['num_accidents'])
    plt.plot(data['precipitation'], line, color='green', linewidth=3)
    plt.title('LA Precipitation vs Accidents between 2012 to 2015')
    plt.xlabel('Precipitation')
    plt.ylabel('# Accidents')
    plt.show()


def plot_CHI_data():
    data = pd.read_csv("chi_2012-2015_data.csv")
    data = data.loc[data['precipitation'] > 0]
    plt.figure(figsize=(11,9))
    
    plt.title('Precipitation and Accidents Over Time')
    plt.plot(data['Date'], data['num_accidents'], 'b', label='# accidents')
    plt.plot(data['Date'], data['avg_temp'], 'g', label='average Temp (C)')
    plt.plot(data['Date'], data['precipitation'], 'r', label='precipitation',linewidth=2.0)
    plt.legend()
    plt.show()

def plot_CHI_data_scatter():
    data = pd.read_csv("chi_2012-2015_data.csv")
    data = data.loc[data['precipitation'] > 0]
    plt.figure(figsize=(11,9))
    
    X = pd.DataFrame(data['precipitation'])
    Y = pd.DataFrame(data['num_accidents'])
    
    model = LinearRegression()
    model.fit(X, Y)
    line = model.predict(X)

    plt.scatter(data['precipitation'], data['num_accidents'])
    plt.plot(data['precipitation'], line, color='green', linewidth=3)
    plt.title('Chicago Precipitation vs Accidents between 2012 to 2015')
    plt.xlabel('Precipitation')
    plt.ylabel('# Accidents')
    plt.show()

def avg_la():
    data = pd.read_csv("LA_2012-2015_data.csv")
    no_rain = data.loc[data['precipitation'] == 0]
    rain = data.loc[data['precipitation'] > 0]

    num_no_rain = len(no_rain.index)
    num_rain = len(rain.index)

    accidents_no_rain = no_rain.sum(axis=0)['num_accidents']
    accidents_rain = rain.sum(axis=0)['num_accidents']

    avg_no_rain = accidents_no_rain / num_no_rain
    avg_rain = accidents_rain / num_rain
    plt.title('Average number of accidents with or without rain in LA')
    plt.bar(['no rain', 'rain'], [avg_no_rain, avg_rain])
    plt.show()


def avg_chi():
    data = pd.read_csv("chi_2012-2015_data.csv")
    no_rain = data.loc[data['precipitation'] == 0]
    rain = data.loc[data['precipitation'] > 0]

    num_no_rain = len(no_rain.index)
    num_rain = len(rain.index)

    accidents_no_rain = no_rain.sum(axis=0)['num_accidents']
    accidents_rain = rain.sum(axis=0)['num_accidents']

    avg_no_rain = accidents_no_rain / num_no_rain
    avg_rain = accidents_rain / num_rain
    plt.title('Average number of accidents with or without rain in Chicago')
    plt.bar(['no rain', 'rain'], [avg_no_rain, avg_rain])
    plt.show()
def main():
    #save_LA_data()
    #plot_LA_data()
    #save_CHI_data()

    #plot_CHI_data()
    #plot_CHI_data_scatter()
    avg_chi()
if __name__ == "__main__":
    main()