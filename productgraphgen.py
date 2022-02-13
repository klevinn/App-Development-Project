#For Staff
import shelve
import matplotlib.pyplot as plt

def graph():
    prod_dict ={}
    db = shelve.open('user', 'c')

    try:
        if 'ProductSales' in db:
            prod_dict = db['ProductSales']
        else:
            db["ProductSales"] = prod_dict
    except:
        print("Error in retrieving User from user.db")
    db.close()

    #data for plotting
    x = []
    y = []
    for i in prod_dict:
        x.append(i)
        y.append(prod_dict[i])

    plt.bar(x, y)

    plt.xlabel('Product Name')
    plt.ylabel('Number Sold')
    plt.title('Product Sales')

    plt.savefig("static/images/graph.png")

graph()