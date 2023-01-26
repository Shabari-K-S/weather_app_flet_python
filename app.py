#   importing necessary package

import flet
from flet import *
import requests
import datetime
from geopy.geocoders import Nominatim

loc = Nominatim(user_agent="GetLoc")

getLoc = loc.geocode("Salem Tamilnadu")

#    api key form open weather api

api_key = "fae0e5d7335931ef042ba652175b05da"

lon0=getLoc.longitude
lat0=getLoc.latitude

base_url = "http://api.openweathermap.org/data/2.5/onecall?lat="
complete_url = base_url + str(lat0) + "&lon=" + str(lon0) + "&exclude=minutely,hourly,alearts&unit=metric&appid=" + api_key
_current = requests.get(complete_url)


days = [ "Mon", "Tue", "Wed" ,"Thu", "Fri", "Sat", "Sun"]

def main(page: Page):

    page.horizontal_alignment='center'
    page.vertical_alignment='center'

    # animation

    def _expand(e):
        if e.data == 'true':
            _c.content.controls[1].height = 530
            _c.content.controls[1].update()
        else:
            _c.content.controls[1].height = 660 * 0.39
            _c.content.controls[1].update()
        pass


    # current weather

    def _current_temp():
        _current_temp = _current.json()['current']['temp']
        _current_weather = (_current.json()['current']['weather'][0]['main'])
        _current_description = _current.json()['current']['weather'][0]['description']
        _current_wind = _current.json()['current']['wind_speed']
        _current_humidity = _current.json()['current']['humidity']
        _current_feels = _current.json()['current']["feels_like"]
        firstdayimage = _current.json()['daily'][0]['weather'][0]['icon']
        return [_current_temp, _current_weather, _current_description, _current_wind, _current_humidity, _current_feels, firstdayimage]

    # current extra
    
    def _current_extra():

        _extra_info = []


        _extra = [
            [
                round(_current.json()['current']['visibility'] /1000),
                " Km",
                "Visibility",
                "./assets/visibility.png"
            ],
            [
                round(_current.json()['current']['pressure'] * 0.03, 2),
                " inHg",
                "Pressure",
                "./assets/pressure.png"
            ],
            [
                datetime.datetime.fromtimestamp(
                    _current.json()["current"]['sunset']
                ).strftime("%I:%M %p"),
                "",
                "Sunset",
                "./assrts/sunset.png"
            ],
            [
                datetime.datetime.fromtimestamp(
                    _current.json()["current"]['sunrise']
                ).strftime("%I:%M %p"),
                "",
                "Sunrise",
                "./assrts/sun.png"
            ],
        ]

        for data in _extra:
            _extra_info.append(
                Container(
                    bgcolor='white10',
                    border_radius=12,
                    alignment=alignment.center,
                    content=Column(
                        alignment='center',
                        horizontal_alignment='center',
                        spacing=25,
                        controls=[
                            Container(
                                alignment=alignment.center,
                                content=Image(
                                    data[3],
                                    color='white'
                                ),
                                width=32,
                                height=32
                            ),
                            Container(
                                content=Column(
                                    alignment = 'center',
                                    horizontal_alignment='center',
                                    spacing=0,
                                    controls=[
                                        Text(
                                            str(data[0]) + data[1],
                                            size=14
                                        ),
                                        Text(
                                            data[2],
                                            size=9,
                                            color='white45'
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            )
        
        return _extra_info

    # top container

    def _top():
        
        _today = _current_temp()

        _today_extra = GridView(
            max_extent=150,
            expand=1,
            run_spacing=5,
            spacing=5
        ) 

        for info in _current_extra():
            _today_extra.controls.append(info)

        top = Container(
            width=310,
            height=660 * 0.40,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors = ["Lightblue900","Lightblue600"]
            ),
            border_radius=35,
            animate=animation.Animation(duration=450,curve='decelerate'),
            on_hover=lambda e: _expand(e),
            padding=15,
            content=Column(
                alignment='start',
                spacing=10,
                controls=[
                    Row(
                        alignment='center',
                        controls=[
                            Text(
                                'Salem, TN',
                                size=16,
                                weight='w500'
                            )
                        ]
                    ),
                    Container(padding=padding.only(bottom=5)),
                    Row(
                        alignment='center',
                        spacing=30,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                        width=100,
                                        height=100,
                                        image_src=f"icon/{_today[-1]}@2x.png"
                                    )
                                ]
                            ),
                            Column(
                                spacing=5,
                                horizontal_alignment='center',
                                controls=[
                                    Text(
                                        "Today",
                                        size=12,
                                        text_align='center'
                                    ),
                                    Row(
                                        vertical_alignment='start',
                                        spacing=0,
                                        controls=[
                                            Container(
                                                content=Text(
                                                    str(_today[0] - 273.15)[0:4],
                                                    size=42
                                                )
                                            ),
                                            Container(
                                                Text(
                                                    "°",
                                                    size=28,
                                                    text_align='center'
                                                )
                                            )
                                        ]
                                    ),
                                    Text(
                                        _today[1] + " - Overcast",
                                        size = 10,
                                        color = 'white45',
                                        text_align= 'center'
                                    )
                                ]
                            )
                        ]
                    ),
                    Divider(height=8,thickness=1,color="white12"),
                    Row(
                        alignment='spaceAround',
                        controls=[
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src = "./assets/wind.png",
                                                color='white'
                                            ),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(_today[3])+" km/h",
                                            size=11
                                        ),
                                        Text(
                                            "Wind",
                                            size=9,
                                            color='white40'
                                        )
                                    ]
                                )
                            ),
                            Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src = "./assets/humidity.png",
                                                color='white'
                                            ),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(_today[4])+"%",
                                            size=11
                                        ),
                                        Text(
                                            "Humiditiy",
                                            size=9,
                                            color='white40'
                                        )
                                    ]
                                )
                            ),Container(
                                content=Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        Container(
                                            alignment=alignment.center,
                                            content=Image(
                                                src = "./assets/thermometer.png",
                                                color='white'
                                            ),
                                            width=20,
                                            height=20
                                        ),
                                        Text(
                                            str(int(_today[-2] - 273.15))+"℃",
                                            size=11
                                        ),
                                        Text(
                                            "Feels like",
                                            size=9,
                                            color='white45'
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    _today_extra,
                ]
            )
        )

        return top


    # bottom data

    def _bot_data():
        
        _bot_data = []
        for i in range(1,8):
            _bot_data.append(
                Row(
                    spacing=5,
                    alignment='spaceBetween',
                    controls=[
                        Row(
                            expand=1,
                            alignment='start',
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Text(
                                        days[
                                            datetime.datetime.weekday(
                                                datetime.datetime.fromtimestamp(
                                                    _current.json()['daily'][i]['dt']
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                        Row(
                            expand=1,
                            controls=[
                                Container(
                                    content=Row(
                                        alignment='start',
                                        controls=[
                                            Container(
                                                width=30,height=30,
                                                alignment=alignment.center_left,
                                                content=Image(
                                                    src=f"./assets/icon/{_current.json()['daily'][i]['weather'][0]['icon']}@2x.png"
                                                )
                                            ),
                                            Text(
                                                _current.json()['daily'][i]['weather'][0]["main"],
                                                size = 11,
                                                color='white45',
                                                text_align='center'
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                        Row(
                            expand=1,
                            alignment='end',
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    content=Row(
                                        alignment='center',
                                        spacing=5,
                                        controls = [
                                            Container(
                                                width=30,
                                                content=Text(
                                                    str(int(_current.json()['daily'][i]['temp']['max']-273.15))+"℃",
                                                    text_align='start'
                                                    )
                                            ),
                                            Container(
                                                width=40,
                                                content=Text(
                                                    str(int(_current.json()['daily'][i]['temp']['min']-273.15))+"℃",
                                                    text_align='end'
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        
        return _bot_data

    # bottom container
    
    def _bottom():
        _bot_column = Column(
            alignment='center',
            horizontal_alignment='center',
            spacing=25,
        )

        for data in _bot_data():
            _bot_column.controls.append(data)

        bottom = Container(
            padding = padding.only(top = 280, left = 20, right = 20, bottom = 20),
            content=_bot_column,
        )

        return bottom

    _c = Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor='black',
        padding=10,
        content=Stack(
            width=300, height=550, 
            controls=[
                _bottom(),
                _top(),
            ]
        )
    )

    page.add(_c)

if __name__ == "__main__" :
    flet.app(target=main, assets_dir="assets")
