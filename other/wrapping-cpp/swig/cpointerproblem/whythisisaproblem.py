import test
import test2

print "We can call the function test.f completely as we would expect"
for i in range(10):
    print test.f(i)

print "On the other hand, passing that function to myfun does not work!"
#print test.myfun(test.f)

print "See changes between test.i and test2.i to see how to fix this"
print test2.myfun(test2.f)
