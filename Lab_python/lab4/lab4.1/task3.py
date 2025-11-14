import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('lightblue')

body = plt.Circle((0, 0), 2.5, color='black', ec='black', linewidth=2)
ax.add_patch(body)

belly = plt.Circle((0, 0), 1.8, color='white', ec='black', linewidth=1)
ax.add_patch(belly)

head = plt.Circle((0, 3), 1.5, color='black', ec='black', linewidth=2)
ax.add_patch(head)

face = plt.Circle((0, 3), 1.1, color='white', ec='black', linewidth=1)
ax.add_patch(face)

eye_left = plt.Circle((-0.4, 3.3), 0.25, color='black')
eye_right = plt.Circle((0.4, 3.3), 0.25, color='black')
ax.add_patch(eye_left)
ax.add_patch(eye_right)

ax.add_patch(plt.Circle((-0.35, 3.35), 0.07, color='white'))
ax.add_patch(plt.Circle((0.45, 3.35), 0.07, color='white'))

beak = plt.Polygon([[0, 2.9], [-0.2, 2.7], [0.2, 2.7]], color='orange', ec='black')
ax.add_patch(beak)

wing_left = plt.Circle((-2.2, 0.5), 0.8, color='black', ec='black')
wing_right = plt.Circle((2.2, 0.5), 0.8, color='black', ec='black')
ax.add_patch(wing_left)
ax.add_patch(wing_right)

foot_left = plt.Circle((-0.7, -2.2), 0.5, color='orange', ec='black')
foot_right = plt.Circle((0.7, -2.2), 0.5, color='orange', ec='black')
ax.add_patch(foot_left)
ax.add_patch(foot_right)

plt.xlim(-5, 5)
plt.ylim(-3, 6)
plt.title('Пингвин', fontsize=14, pad=20)
plt.tight_layout()
plt.show()
