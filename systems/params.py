def read():
    sim = {}
    clus = {}
    fil = open('../catalogs/cfhsimcat.txt')
    all = fil.readlines()
    for l in all:
        if l[:3] == 'ASW':
            s = l.split()
            gid = s[1]
            sim[gid] = [s[0],s[-1]]
    fil = open('../catalogs/simcat_q.txt')
    all = fil.readlines()
    for k,l in enumerate(all):
        if k > 2:
            s = l.split()
            gid = s[0]
            sim[gid].append(('source',s[16],s[17]))
            sim[gid].append(('SIE',s[13],s[11],s[12]))
            sim[gid].append(('ext shear',s[14],s[15]))
    fil = open('../catalogs/simcat_g.txt')
    all = fil.readlines()
    for k,l in enumerate(all):
        if k > 1:
            s = l.split()
            gid = s[0]
            sim[gid].append(('source',s[16],s[17]))
            sim[gid].append(('SIE',s[13],s[11],s[12]))
            sim[gid].append(('ext shear',s[14],s[15]))
    fil = open('../catalogs/simcat_c.txt')
    all = fil.readlines()
    for k,l in enumerate(all):
        if k > 2:
            s = l.split()
            gid = s[0]
            sim[gid].append(('source',s[13],s[14]))
    fil = open('../catalogs/clus_member.txt')
    all = fil.readlines()
    for k,l in enumerate(all):
        if k > 1:
            s = l.split()
            cid = s[0]
            gal = ('NFW',s[4],s[5],s[2],s[3],s[8],s[9])
            if cid in clus:
                clus[cid].append(gal)
            else:
                clus[cid] = [s[1],gal]
    for cid in clus:
        c = clus[cid]
        sim[c[0]].append(c[1:])
    tidy = {}
    for gid in sim:
        s = sim[gid]
        if s[0] != 'ASW0001gae':
            tidy[s[0]] = s[1:]
    return tidy

