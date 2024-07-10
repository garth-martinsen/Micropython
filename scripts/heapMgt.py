import gc

for i in range(5):
    members = []
    members.append(i)
    
members.clear()
print("members list: ",members)

# Memory functions
gc.enable()
allocated = gc.mem_alloc()
free = gc.mem_free()
#Run a garbage collection.
collect = gc.collect()
gc.disable()

print("Allocated: ",allocated)
print("Free: ",free)
total = allocated + free
print("Total Heap bytes: ",total)
print("Heap used% : ", allocated/free *100)
print("collected: ", collect)


print("Global Variables: ", globals())

help(vfs)
