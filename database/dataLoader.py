import mysql.connector


cnx = mysql.connector.connect(host="localhost", user="root", passwd="root", db="Catalog")
cursor = cnx.cursor(buffered=True)

with open("Data.txt", "r") as data_set:
    lines = data_set.readlines()

sql = "INSERT INTO `electronics`(`link`, `company`, `brand`, `price`, `ram_size`) VALUES "
for line in lines:
    # Split the line on whitespace
    data = line.split(",")
    link = data[0].strip()
    company = data[1].strip()
    brand = data[2].strip()
    price = data[3].strip()
    ram_size = data[4].strip()
    if ram_size == "":
        ram_size = "0"
    product = data[5].strip()

    if product == "phone":
        sql += "(\"" + link + "\",\"" + company + "\",\"" + brand + "\"," + price + "," + ram_size + "),\n"

print sql