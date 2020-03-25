import krpc
import time

conn = krpc.connect()
vessel = conn.space_center.active_vessel

ph = vessel.flight().surface_altitude


class PID:
    def __init__(self):
        self.pv = 180  # 设定值
        self.kp = -0.03  # 比例控制系数
        self.ki = 0.01  # 积分系数
        self.kd = -5.5  # 微分系数
        self.sysOut = 0  # 系统输出

        self.per = []  # 误差

    def pid(self, h):
        global ph  # 初次测量高度
        er = h - self.pv  # 初次误差
        # print("er:", er)
        p = 0.25 + self.kp * er  # p控制
        d = self.kd * (h - ph) * 0.1  # d控制
        # i = self.ki * sum(self.per) * 0.1
        # print("i:", i)
        out = p + d  # pd总输出
        self.sysOut = out
        ph = h



if __name__ == "__main__":
    vessel.control.activate_next_stage()
    # time.sleep(1)
    while True:
        h = vessel.flight().surface_altitude
        print(h)
        pid = PID()
        pid.pid(h)
        vessel.control.throttle = pid.sysOut
        # if(vessel.control.gear == True):
        #     vessel.control.gear = False
        # if pid.sysOut < 0 :
        #     vessel.control.gear = True