import matplotlib
matplotlib.use('TkAgg')  # PyCharm 推荐后端

import matplotlib.pyplot as plt

# 示例数据
data1 = [20516.27, 18379.38, 17500.12, 16200.45, 15000.78,
         14500.22, 14000.33, 13500.99, 13000.44, 12500.88]

data2 = [18500.11, 17800.66, 16000.77, 15500.88, 14800.99,
         14200.10, 13800.11, 13200.22, 12900.33, 12400.44]

x = list(range(len(data1)))

# 创建图形
plt.figure(figsize=(10, 6))

# 折线图
plt.plot(x, data1, marker='o', label='Data 1', color='blue')
plt.plot(x, data2, marker='s', label='Data 2', color='orange')

# 为每个点添加数值标签
for i in range(len(x)):
    plt.text(x[i], data1[i], f'{data1[i]:.2f}', ha='left', va='bottom', fontsize=8, color='blue')
    plt.text(x[i], data2[i], f'{data2[i]:.2f}', ha='left', va='top', fontsize=8, color='orange')

# 设置标题、图例等
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Two Line Charts with Value Labels')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
