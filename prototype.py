#!/usr/bin/python
# author: @bkupfer
import MySQLdb

# Getting initial T value from user
T = 0 # maximum time ([mins])
try:
	f = open('prototype.data', 'r')
	line = f.readline()
	T = int(line[2:])
except:
	f = open('prototype.data', 'w')
	T = int(raw_input("Ingrese tiempo (en [mins]) deseado en dedicar a la toma de inventario. "))
	f.write("T=" + str(T))
	f.close()
print "Tiempo total destinado (en [mins]) a la toma de inventario " + str(T) + " [mins]."

# Generating list
t = 1 # avg. estimated time per 1 item
print "Generando lista tentativa de items para toma de inventario"

# Open database connection
db = MySQLdb.connect("localhost","root","encryption","losvinedos")
cursor = db.cursor()
# score_increase = 1
output = ""

# Percentajes of time destinated for each {a,b,c} item clases
limit_a = 65
limit_b = 20
limit_c = 15
# Time in [mins] destinated for each {a,b,c} item clases
time_a = T * limit_a / 100
time_b = T * limit_b / 100
time_c = T * limit_c / 100

sku_increment = []
sku_decrese = []
# class A
cursor.execute("SELECT * FROM losvinedos.kardex WHERE class = 'A' ORDER BY score DESC")
results = cursor.fetchall()
i = 0
for row in results:
	if i < time_a:
		output += str(row[0]) + '\t' + str(row[1] + '\n')
		sku_decrese.append(row[0])
		i += t
	else: 
		sku_increment.append(row[0])
		
# class B
cursor.execute("SELECT * FROM losvinedos.kardex WHERE class = 'B' ORDER BY score DESC")
results = cursor.fetchall()
i = 0
for row in results:
	if i < time_b:
		output += str(row[0]) + '\t' + str(row[1] + '\n')
		sku_decrese.append(row[0])
		i += t
	else: 
		sku_increment.append(row[0])

# class C
cursor.execute("SELECT * FROM losvinedos.kardex WHERE class = 'C' ORDER BY score DESC")
results = cursor.fetchall()
i = 0
for row in results:
	if i < time_c:
		output += str(row[0]) + '\t' + str(row[1] + '\n')
		sku_decrese.append(row[0])
		i += t
	else: 
		sku_increment.append(row[0])

# Set new scores
sql_inc = "UPDATE losvinedos.kardex SET score=(score+1) WHERE sku="
for sku in sku_increment:
	cursor.execute(sql_inc + str(sku))
sql_dec = "UPDATE losvinedos.kardex SET score=0 WHERE sku="
for sku in sku_decrese:
	cursor.execute(sql_dec + str(sku))

db.commit()
db.close()

# Give output to user
print "\nLista de items a ser inventareados:"
print "SKU\tItem"
print output

