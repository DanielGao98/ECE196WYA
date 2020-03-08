from simple_pid import PID
import matplotlib.pyplot as plt
pid = PID(0.001,0.1,0.001, setpoint=0)
val = 10
data = []
while abs(val)>1:
    print(val)
    diff = pid(val)
    print(f'diff={diff}')
    val = val+diff
    data.append(val)
plt.plot(data)
plt.show()