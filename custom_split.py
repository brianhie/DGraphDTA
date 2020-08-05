import json

if __name__ == '__main__':
    row2split = {}
    with open('data/davis_full/split.txt') as f:
        for line in f:
            fields = line.rstrip().split('\t')
            prot = fields[1]
            if 'ABL1(E255K)' in prot:
                prot = 'ABL1(E255K)'
            elif 'ABL1(M351T)' in prot:
                prot = 'ABL1(M351T)'
            elif 'ABL1(Y253F)' in prot:
                prot = 'ABL1(Y253F)'
            else:
                prot = prot.replace('-phosphorylated', 'p')
                prot = prot.replace('-nonphosphorylated', '')
            if prot.startswith('EGFR'):
                if prot == 'EGFR(A750P/L747-E749del)':
                    prot = 'EGFR(L747E749del)'
                elif prot == 'EGFR(P753S/L747-S752del)':
                    prot = 'EGFR(L747S752del)'
                else:
                    prot = prot.replace('-', '').replace('/', '')
            if prot.startswith('GCN2'):
                prot = prot.replace('.', '').replace('/', '')
            if prot.startswith('KIT'):
                prot = prot.replace('/', '-')
            if 'falcip' in prot or 'tuber' in prot:
                prot = prot.replace('.', '')
            if prot.startswith('RPS') or prot.startswith('RSK'):
                prot = prot.replace('Kin.Dom', 'KinDom')
            row = '\t'.join([ fields[0], prot ])
            split = fields[2]
            row2split[row] = split

    train_idx, valid_idx = [], []
    with open('data/davis_full/unrolled.txt') as f:
        for idx, line in enumerate(f):
            row = line.rstrip()
            split = row2split[row]
            if split == 'train':
                train_idx.append(idx)
            elif split == 'valid':
                valid_idx.append(idx)
            else:
                raise ValueError('Invalid split type')

    with open('data/davis_full/folds/train_fold_setting1.txt', 'w') as of:
        json.dump([ train_idx, valid_idx ], of)
