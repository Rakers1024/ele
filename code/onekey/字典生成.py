min = 17306600000
max = 17306700000
#生成字典
with open('../../data/onekey/字典'+str(min)+'-'+str(max)+'.txt', 'w') as f:
    for i in range(min, max+1):
        f.write(str(i)+"\n")
print("成功")