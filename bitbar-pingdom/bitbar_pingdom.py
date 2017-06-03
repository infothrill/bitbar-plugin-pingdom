#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Bitbar pingdom</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.author>Paul Kremer</bitbar.author>
# <bitbar.author.github>infothrill</bitbar.author.github>
# <bitbar.desc>Show status of pingdom checks.</bitbar.desc>
# <bitbar.image>http://www.hosted-somewhere/pluginimage</bitbar.image>
# <bitbar.dependencies>python, virtualenv</bitbar.dependencies>
# <bitbar.abouturl>http://url-to-about.com/</bitbar.abouturl>

import sys

from operator import attrgetter

from backports import configparser  # https://pypi.python.org/pypi/configparser

import pypingdom


class MyConfigParser(configparser.ConfigParser):
    def getlist(self, section, option, fallback=None):
        value = self.get(section, option, fallback=fallback)
        return list(filter(None, (x.strip() for x in value.split())))


def main():
    config = MyConfigParser()
    config.read("bitbar_pingdom.conf")
    uptime_url = "https://my.pingdom.com/reports/responsetime#check=%s&daterange=1days&tab=uptime_tab"
    icons = {
        'up': config.get("icons", "black", fallback="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAABAlJREFUWAm9V81LVFEUv/PpTNOIiWLEWANCaCBhUzAQkrQxTJAWQoG7/oRa1y7IAhcuokUtRIQ2IRREf0EJLoOgKJlGsIYYBWEcnXnv9ftd77HnNO81Dz8OnDn3nnPu+b73qVIN4DhOiKxisZhcWVlJYB8BhskXbDjiuaX+8vJyDDThqSQCKsv6qKnbV5jO3AxxTl4zvsiD0GZ2hHeQrHlWzjtYE48FIvBCbARWsxm/UW/fXjLYx/TYUJdOLCNPgZ42vN+g64av24q1bfb+hJPur6Gl7kDz4CwAi8AdYA1YCoVC7yKRyC2sBTyrIf0HTXAAo3LCg7qdP4WO7nc4HHYSiYSTTCYdOJYZcBDIG+iwOgSpxu6u4bcF3/qEDgAOX2BHR1ZbW1sVlNmL41o8HnfzliGLAQnuBHY5rl/PMhkdVsdGhndt236IdS0Wi4V2dnZifX19kVwut9Hf319BJVJra2tRBMljDOws1j3I8C3W9MFAA4NEHsfJ70AHWeqsR0dH16enp+9gfjoKhcKpmZmZ6xMTE5+pg2A5ExxA6l8AJfi2Ylfl3189G9Fo9AZENFYnzefz1vz8PAdxH+Dp7kRgP8HkbLAdDqrwwCh5zplfZLoC9Xr9Io2gBcxMDQwMvJ6amvqIZRwl1q/lyMhIore3tzw0NPSsvb1dVatVfQUhz/EMwLMFfgHIoROYbIVAVDqdJn7dtals8Dn1Tnd3tw6us7PzSyaToTjEeUAAaaMrtsz2L/ELQLT4NVPordrc3FSVSuWcEfArqSuQSqX0xJfL5TOlUkmLUTGF4LaMrsyT2GyJSt8eQ5szsE06PDy8tbi4KMO1ZwjBxMfHx79RBzNAx5yBR0ZBbO3pt7KQQ9M0BqxhIPkMO2NjYz9mZ2dH4ZR/LyTm5uYuT05OfjB6HFatB3oJSPCstF9pGACNPQHeN+soWmFblhUeHBxU2Wy2iL2FNyC7tLQEFWUh6xrKz+f9FfA2kO8AAwoMUgEGoCtgqGXaoa+l8FCdbfRctwmU70YHkOCZ/X+F+vj+HwYSxksYR+YR9NrGt8DG6xjGLeG1jMP5EnhXobcBZPb6SoI2BcmyqbCBSUNswQIcRdCGm8CTRqcC+gn4ErLnuClkt1T6oAEoOH0P43PADDLvoaNarfYLtAAUaMk5lYMEIMaTZrEKx6vCNJT2OHAtD12QAOTGcNAI/EiJI84GkYMZBEL8e98rCO0Q10rk/BIqlJ3lJXAmJFuuGUAg4Cwpnz/JtCNcr2uwqjPEhG90dXWdN158r5dfJHCskwPle+EL2gmyvgKte8ADO/f15iFszLRx73HscNlsB794R+OcPZG+HG7cza019XfcATQPzcU1/5rLFXRJgi2RWNTnpqk/qOecF9e+vyUAAAAASUVORK5CYII="),
        'down': config.get("icons", "red", fallback="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAABCZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjU8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjE0NDwvdGlmZjpYUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgICAgPHRpZmY6WVJlc29sdXRpb24+MTQ0PC90aWZmOllSZXNvbHV0aW9uPgogICAgICAgICA8ZXhpZjpQaXhlbFhEaW1lbnNpb24+MzI8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpDb2xvclNwYWNlPjE8L2V4aWY6Q29sb3JTcGFjZT4KICAgICAgICAgPGV4aWY6UGl4ZWxZRGltZW5zaW9uPjMyPC9leGlmOlBpeGVsWURpbWVuc2lvbj4KICAgICAgICAgPGRjOnN1YmplY3Q+CiAgICAgICAgICAgIDxyZGY6U2VxLz4KICAgICAgICAgPC9kYzpzdWJqZWN0PgogICAgICAgICA8eG1wOk1vZGlmeURhdGU+MjAxNzowNDoxOSAxMjowNDo0NzwveG1wOk1vZGlmeURhdGU+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+UGl4ZWxtYXRvciAzLjQuMjwveG1wOkNyZWF0b3JUb29sPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4K8U9GOgAABGpJREFUWAm1Vt+LFVUc/5yZe++62pohJoiLPyKhXUlKhUoC9UUkEAyN2kd7iV79A9zeewyih3wQvCkrYiClL2qIUA8WQSqZmLaGbJG7av7auTOnz2fOHHf2cmfu3N38wpkz8z3f8/18z/fXGYM2srDGwFiLlf1AzQKbI2CY8wEOR1r372WzdAGbasA/ocGNx2WycMKlIv/bYh4rkNY8w6OI14nv13uZO+nxPLpobuQUfJLtP0BfVwvL3NByuyz2hho5VvpqMRp04rfLzflbJ84DWCxfZNH3EsfLFs+/4BU7Q0bT0Hpe6WyxekGpABd9vCRnUX8jRtA8DTN+BGaaIzoJ89dtmG8twt1eV95Yz/Oz1ydsnmprzeBcyy+2zxL28bUIPm3C7peMjijLNau+vIIdwMmlePF9g4kH8obBaMLljuSwOy7NML0BBP+S4PuYdckAED0gdgzUJcmEaC0E4ocZ7xXg4mt4/U2Di5HfP6Nx9ltprJyFakrhhwInUNTHKNwD+tYTfASYGgnDO2+xY90nj8YFDTrkCrAR+OkzB/VeKcZsc3JfM3EabpyBuX6YZXaCMddMb0zSqA8slixRAlrUtpN3RWvHmBNNmMTJNYakUqHIqZ71WrgAbMtK7dftt4E1cjHdXt/FENDpOw3irwympgzuThq0zgDPbaFHJp7QG4uBaYfS2uPmc4U4hQvA/azJJBukhB+8EwgDHDeIvrcYbshLbjCbce8OpT5fSplHqZGMDyxDIVpWeHeUGDDgNy2UJTqSK3bzm1RSaaLqcBWiC0tkrq7jkxuNFNMi5qtIl1ln4k3VleraLcFJJ7rKTbfYES0LQbRG1cB3u+KP9Nu5gOh0huhS5k33lX+WeOCpWJoLfKSyCey7Fo0hg2tPvAd01SokNODjP7ltUbZ1GczP7vXveRmQbuZRVGLJkbT/RKeY+TvUydyobwIuf9cE1tLK+C5AUVF4zM1bC5tRlRA8tZ55ENDXCYEG30Z8ajAYH0dYi6ei1upviCRwrkeshAV7YY4yWX9US2Y3zELlzMk/qxiQl09bLith+gKPlyTJIJJpVUjC36eW2rHAVwC/17H4I9WBS8CxWTryHz0ZQCA2IQT/0sXaSNBEiUHQgCFK3c6a/WEY/bvVI7qdXoZUNkCnJHhtBKZJf4Zfw77DxkRnsAcDD9cDv7wKc9Ag+YKfLEW5fqzQ9don6skAt8WcriE+ZNG/kl5fTh4LJJwweHwz7QBkVAWXvsoGSNiRpefVGR/d4qRBcn1IlxdwNmZ5dj2529ebAYyCyDDkOqXqfigDcr/tBGYeZmIS6kJq4/yPk9WdyN8FzksUyi4YuVykVjzG02qMpm3Z8Xt5bguZxDcKDFibNY/ghFQyywfY4dhjaucdRHFz6WaCTu5kirAzDf4e53/gZt73+/kDuk5Lnp+JPdupHaz9+9miZ9pVVhYbeSsW/9nMyxD3U+HjMi9VlTZ3xJtJjEo65iVUCctds0UlWh1fZS5dRTv+A2Brhz+97++jAAAAAElFTkSuQmCC"),
        'warning': config.get("icons", "warning", fallback="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAWJQAAFiUBSVIk8AAABCZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iCiAgICAgICAgICAgIHhtbG5zOmV4aWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vZXhpZi8xLjAvIgogICAgICAgICAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICAgICAgICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyI+CiAgICAgICAgIDx0aWZmOlJlc29sdXRpb25Vbml0PjI8L3RpZmY6UmVzb2x1dGlvblVuaXQ+CiAgICAgICAgIDx0aWZmOkNvbXByZXNzaW9uPjU8L3RpZmY6Q29tcHJlc3Npb24+CiAgICAgICAgIDx0aWZmOlhSZXNvbHV0aW9uPjE0NDwvdGlmZjpYUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6T3JpZW50YXRpb24+MTwvdGlmZjpPcmllbnRhdGlvbj4KICAgICAgICAgPHRpZmY6WVJlc29sdXRpb24+MTQ0PC90aWZmOllSZXNvbHV0aW9uPgogICAgICAgICA8ZXhpZjpQaXhlbFhEaW1lbnNpb24+MzI8L2V4aWY6UGl4ZWxYRGltZW5zaW9uPgogICAgICAgICA8ZXhpZjpDb2xvclNwYWNlPjE8L2V4aWY6Q29sb3JTcGFjZT4KICAgICAgICAgPGV4aWY6UGl4ZWxZRGltZW5zaW9uPjMyPC9leGlmOlBpeGVsWURpbWVuc2lvbj4KICAgICAgICAgPGRjOnN1YmplY3Q+CiAgICAgICAgICAgIDxyZGY6U2VxLz4KICAgICAgICAgPC9kYzpzdWJqZWN0PgogICAgICAgICA8eG1wOk1vZGlmeURhdGU+MjAxNzowNDoxOSAxNDowNDo1NDwveG1wOk1vZGlmeURhdGU+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+UGl4ZWxtYXRvciAzLjQuMjwveG1wOkNyZWF0b3JUb29sPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KR+ehRQAABI1JREFUWAmtVl1oXEUU/nb3ZnebNP5jY0n9LU2o2mqi4A+CSrFo8cFQpI/aiEoe8pInfRJ88UHULhZRUKSorSjVQMUUoVIqWMGKohVtS01o+9Bquxtjkt3s7l2/b+6duL3dudldMzCcO+ec+b4zZ2bOnQQirVZDIpFAjXIFTTX2cij1bZrs9jtOCot2jz3FOcU4XzIa51if5TLWcyUFWq+wJNI10lt7K7IRjtUpRW21EMDOrzW7LW2R1U8icUq9Xqdv6pKN9FG/6NiuIKq/ZExw+Sa50qqMHHdR9EjH/hf1eUoTiCTHvuRSTfucpXPsCRU5fczJ5/c9k69g9JsTeGB6Hqtk68ogv7EXRwZexjv0+0yk1Ovkm2CjQVg8yqwC8OhYiTrZsXXWuPY+Xs1NYEzfKa57RYdZKYq8qOWQ6sE+7NvwErYRc5ZzlTFnJgy3wOKaDSC/A+/u+hbbBdidRXm2hGTVB0PQvqDCLFTnFgLd2mtx5LEduJe+ZTvfxaEi4WwmQoLXzmA4N4btXHU5nULy73lkBq4H7luLQrID/s+TuOrr3+F1pFD1PBRPnMPg3E68SeDn2HVGGm6FiJ2H0EZOmd7zLH47N4ObVmZQ/qeEjtFNKGAYI5z/ZYhxJ/ZiZ+4T9Gc8VBYqvCnEHt2NW5mFX4nh3ApTiBRJg2av2sMi70qjKvKhAe7pMB4l8G72Anue/QCGcP/oIzhbqsC7vBMLBu8LbA1xnTxOAycG2TmAjQaE+ynZ+zj2kvCwMqMshV036QKexlvXrAR4PszBO/o9Bs1cnt9QXiLiAggmTaOThwxMK67Wze/H8RDFJ6mtgCY46o/1qzIweN2S/By6zajNAIK5TLvPUHjAcH6WqkncEIKqItr/hbkN1K+eOh9YeUPAMzMf+jrPWlwGQqSg7KYS5jTjwjiGSLyeqy/ZDFAWqUtjD0ZOsR6S2LQ7bsNP/z8ArlIgs7zjGV65Dw4jiw8xQcLN7Nmw34WvcDA3jpu5XdXCPINRexKfGgl3MYqtA2ay/99VLZWRTHvwc/uw5qHjmLi9D6f43KhOncSN4z+aglSlvczKmN2yAR8zMz8wQGdJFv7SAYRLsEIltzuDhYPHkGLxWSM9ifzONCoV2kTecxn+uOUFPI8XzSznDZC1pQC4F3qqJWdKSOtQdnFLSA5lhmXYpH39dfhu02t4gvrCUqtvKQCtkrfB2zqIj1Tp9h/FlpkieOsBpn2urwe/bB7Be4l1eBuvK9L41GueWtMZ4OHyVdBXP4P9iSuxiwS9HK5iV8U8ywCn8Aa/2Joll2/TAcjZtD/Na1n7fppj9cVGYuFVaVOsTbWmAyB4UEyuQEnIHGvPLZEOmqqi812hOdEmTL3jXEEEhH5g91LhD8ZffA/qAJrVUpqyHCVoYqyK7QwgeMk8hc8FxOvVzUfHNHf9UAgc2MNBK2Ixm27uAI6OplRT3l07hDHKdbJYfSukbftGyaLjtoHDicE+L4FCUl01ZUN73nbqnTQksL9Vp89yGhrySbmcJHFYTXHRSb9a1xWNw7/IJgxhXaSsG/wLn7GziHBl6BkAAAAASUVORK5CYII=")
        }
    check_colors = {
        "down": config.get("colors", "down", fallback="red"),
        "paused": config.get("colors", "paused", fallback="#7c7c7c"),
        "up": config.get("colors", "up", fallback="green"),
        "warning": config.get("colors", "warning", fallback="orange")
        }
    warning_tags = config.getlist("tags", "warning", fallback="")
    ignore_tags = config.getlist("tags", "ignore", fallback="")

    client = pypingdom.Client(username=config.get("pingdom.com", "username"),
                              password=config.get("pingdom.com", "password"),
                              apikey=config.get("pingdom.com", "apikey"),
                              email=config.get("pingdom.com", "email"))
    checks = client.get_checks()
    count_total = len(checks)
    checks = [c for c in checks if not any(tag in [x['name'] for x in c.tags] for tag in ignore_tags)]
    count_ignored = count_total - len(checks)

    servertime = client.servertime()
    count_down = 0
    count_down_warning = 0
    count_up = 0
    count_paused = 0
    for check in checks:
        if check.status == "down":
            count_down += 1
            if any(tag in [x['name'] for x in check.tags] for tag in warning_tags):
                count_down_warning += 1
        elif check.status == "paused":
            count_paused += 1
        elif check.status == "up":
            count_up += 1
    overall_status = "up"
    if count_down > 0:
        if count_down_warning == count_down:
            overall_status = "warning"
        else:
            overall_status = "down"
    else:
        overall_status = "up"
    print("|image=%s" % (icons[overall_status]))
    print("---")
    print("up/down/paused/ignored: %s/%s/%s/%s|color=black href=https://my.pingdom.com/newchecks/checks" % (count_up, count_down, count_paused, count_ignored))
    for check in sorted(sorted(checks, key=attrgetter('name')), key=attrgetter('status')):
        if check.status in ("down", "paused"):
            url = uptime_url % check._id
            if any(tag in [x['name'] for x in check.tags] for tag in warning_tags):
                color = "warning"
            else:
                color = check.status
            print("%s | color=%s href=%s" % (check.name, check_colors[color], url))
            print("--" + check.host)
            _last_outage = client.get_summary_outage(check._id, order="asc")['summary']['states'][-1]
            _status_since = _last_outage['timeto'] - _last_outage['timefrom']
            m, s = divmod(_status_since, 60)
            h, m = divmod(m, 60)
            print("--%s since %dh %02dm %02ds" % (_last_outage['status'], h, m, s))
            if 'lasttesttime' in check:
                print("--last test: " + str(servertime - check.lasttesttime) + " sec ago")
            if 'lasterrortime' in check:
                print("--last error: " + str(servertime - check.lasterrortime) + " sec ago")
            if 'lastresponsetime' in check:
                print("--response time: " + str(check.lastresponsetime) + " ms")
            if 'tags' in check and len(check.tags):
                print("--tags: | color=black")
                for tag in check.tags:
                    print("--" + tag['name'])
    print("Refresh... | refresh=true")


if __name__ == "__main__":
    sys.exit(main())
