import rdflib
from rdflib import URIRef


g = rdflib.Graph()
result = g.parse("http://d-nb.info/gnd/118707507/about/rdf")

print("graph has %s statements." % len(g))


for subj, pred, obj in g:
   if (subj, pred, obj) not in g:
       raise Exception("It better be!")


for s, p, o in g:
    print((s, p, o))

for stmt in g.subject_objects(URIRef("http://d-nb.info/standards/elementset/gnd#preferredNameForThePerson")):
    print str(stmt[1])

s = g.serialize(format='n3')
print "Hier"
for entry in list(g[rdflib.URIRef('http://d-nb.info/gnd/118707507')]):
    print str(entry)

print "Hier2"
for entry in list(g[rdflib.URIRef('http://d-nb.info/standards/elementset/gnd#preferredNameForThePerson')]):
    print str(entry)
