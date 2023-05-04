try:
    from win32api import GetMonitorInfo, MonitorFromPoint # need to install: pywin32==306
except ImportError as msg:
    print(msg)

class WorkSpaceMSWin:

    """"""

    def __init__(self):

        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        monitor_area = monitor_info.get("Monitor")
        work_area = monitor_info.get("Work")
        self.__height_of_bar = monitor_area[1] - work_area[1]
        if self.__height_of_bar == 0:
            self.__height_of_bar = monitor_area[3] - work_area[3]
        self.__width_of_bar = monitor_area[0] - work_area[0]
        if self.__width_of_bar == 0:
            self.__width_of_bar = monitor_area[2] - work_area[2]


    def get_h(self):
        return self.__height_of_bar

    def get_w(self):
        return self.__width_of_bar