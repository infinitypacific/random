import matplotlib.pyplot as plt

alphabet = "abcdefghijklmnopqrstuvwxyz"
pstring = input("Enter a string: ").lower()

plt.figure()
plt.bar([*alphabet], [pstring.count(i) for i in alphabet])
plt.xlabel = 'Letter'
plt.ylabel = 'Frequency'
plt.title('Character Distribution')
plt.show()


#funny character frequency graph/counter CC BY-SA-NC 4.0