import sys, json, hashlib, os

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def main(manifest_path):
    with open(manifest_path,'r') as f:
        mani=json.load(f)
    missing=[]; changed=[]
    for rel,meta in mani.items():
        if not os.path.exists(rel):
            missing.append(rel)
            continue
        if sha256(rel)!=meta.get('sha256'):
            changed.append(rel)
    if missing:
        print('Missing files:', *missing, sep='\n - ')
    if changed:
        print('Changed files:', *changed, sep='\n - ')
    if not missing and not changed:
        print('All checksums OK.')
    return 0 if not (missing or changed) else 1

if __name__=='__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else 'manifest.json'))
