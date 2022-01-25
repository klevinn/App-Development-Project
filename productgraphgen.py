import matplotlib.pyplot as plt

#manually update it

#data for plotting
x = ["product", "product1", "product2", "product3", "product4", "product5"]
y = [0, 10, 5, 12, 2, 20]

plt.bar(x, y)

plt.xlabel('Product Name')
plt.ylabel('Number Sold')
plt.title('Product Sales')

plt.savefig("static/images/graph.png")