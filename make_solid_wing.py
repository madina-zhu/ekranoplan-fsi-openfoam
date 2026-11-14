import re

# Читаем координаты
with open('constant/geometry/wing_coords.txt', 'r') as f:
    lines = f.readlines()

coords = []
for line in lines:
    nums = re.findall(r'-?\d+\.?\d*e?-?\d*', line)
    if len(nums) >= 2:
        coords.append((float(nums[0]), float(nums[1])))

# Разделяем на верхнюю и нижнюю дуги
# В файле NACA точки идут от носа к хвосту (верх), потом от хвоста к носу (низ).
# Нам нужно разделить их и отсортировать по X.
mid = len(coords) // 2
upper = coords[:mid]
lower = coords[mid:]

# Сортируем верхнюю дугу по X (от носа к хвосту)
upper = sorted(upper, key=lambda p: p[0])
# Сортируем нижнюю дугу по X (от хвоста к носу)
lower = sorted(lower, key=lambda p: p[0], reverse=True)

# Объединяем: верх (от носа до хвоста) + низ (от хвоста до носа)
profile = upper + lower

n = len(profile)
z_th = 0.05

stl = "solid wing\n"

# 1. Нижняя поверхность (Z=0)
for i in range(n-1):
    x1, y1 = profile[i]
    x2, y2 = profile[i+1]
    stl += f"  facet normal 0 0 -1\n    outer loop\n      vertex {x1} {y1} 0\n      vertex {x2} {y2} 0\n      vertex {x1} {y1} 0\n    endloop\n  endfacet\n"

# 2. Верхняя поверхность (Z=z_th)
for i in range(n-1):
    x1, y1 = profile[i]
    x2, y2 = profile[i+1]
    stl += f"  facet normal 0 0 1\n    outer loop\n      vertex {x1} {y1} {z_th}\n      vertex {x2} {y2} {z_th}\n      vertex {x1} {y1} {z_th}\n    endloop\n  endfacet\n"

# 3. Закрываем торцы (боковые стенки)
# Вход (передняя кромка)
stl += f"  facet normal -1 0 0\n    outer loop\n      vertex {profile[0][0]} {profile[0][1]} 0\n      vertex {profile[-1][0]} {profile[-1][1]} 0\n      vertex {profile[0][0]} {profile[0][1]} {z_th}\n    endloop\n  endfacet\n"
stl += f"  facet normal -1 0 0\n    outer loop\n      vertex {profile[-1][0]} {profile[-1][1]} 0\n      vertex {profile[-1][0]} {profile[-1][1]} {z_th}\n      vertex {profile[0][0]} {profile[0][1]} {z_th}\n    endloop\n  endfacet\n"

# Выход (задняя кромка)
stl += f"  facet normal 1 0 0\n    outer loop\n      vertex {profile[-2][0]} {profile[-2][1]} 0\n      vertex {profile[0][0]} {profile[0][1]} 0\n      vertex {profile[-2][0]} {profile[-2][1]} {z_th}\n    endloop\n  endfacet\n"
stl += f"  facet normal 1 0 0\n    outer loop\n      vertex {profile[0][0]} {profile[0][1]} 0\n      vertex {profile[0][0]} {profile[0][1]} {z_th}\n      vertex {profile[-2][0]} {profile[-2][1]} {z_th}\n    endloop\n  endfacet\n"

stl += "endsolid wing\n"

with open('constant/geometry/wing.stl', 'w') as f:
    f.write(stl)

print("Готово! Файл wing.stl перезаписан (правильная сортировка точек).")
