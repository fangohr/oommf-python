import test


print "We can call the function test.f completely as we would expect"
for i in range(10):
    test.f(i)

print "On the other hand, passing that function to myfun does not work!"
print myfun(test.f)
