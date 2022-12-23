x1, y1, w1, h1 = map(float, input().split())
x2, y2, w2, h2 = map(float, input().split())

if x1 <= x2:
    coords1 = [x1, -y1, x1 + w1, -y1 - h1]
    coords2 = [x2, -y2, x2 + w2, -y2 - h2]
else:
    coords2 = [x1, -y1, x1 + w1, -y1 - h1]
    coords1 = [x2, -y2, x2 + w2, -y2 - h2]
# print(coords1, coords2)
if coords1[2] >= coords2[0] and coords1[3] <= coords2[1] and coords1[1] >= coords2[3]:
    print("YES")
else:
    print("NO")
