# Calculate Pie using Pythogoras theorem
In this article I have presented what is possibly one of the oldest and simplest methods to calculate the value of Pie. The principle relies on inscribing a square within a cirlce of radius 1 unit and then doubling the sides in every iteration. The permiter of the polygon inscribed within the circle tends towards **2*PIE*radius**

---


# 4 sides
![4-sides.png](docs/images/4-sides.png)

---

# 8 sides
![8-sides.png](docs/images/8-sides.png)

---

# 16 sides
![16-sides.png](docs/images/16-sides.png)

---

# Perimeter with 4 sides
Let us try and derive a formula for the permiter of an inscribed polygon. We will use recursion.

![4-sides-pythagoras.png](docs/images/4-sides-pythagoras.png)

---

# From 4 sides to 8 sides

![4-to-8-sides.png](docs/images/4-to-8-sides.png)


# From 4 sides to 8 and 8 sides to 16 - how to determine the perimeter?

![4-to-8-sides-calculation.png](docs/images/4-to-8-sides-calculation.png)

---

# Where are we ?

We begin with a **square** with side **s0** -->   sub-divide to get an **octagon** with side **s1** --> sub-divide to get an **16 sided regular polygon** with side **s3**

We now have a recursive formula which given the regular polygon length **s(n)** yieds **s(n+1)** 

![summary-table.png](docs/images/summary-table.png)

---

# Final results

![results-table.png](docs/images/results-table.png)
