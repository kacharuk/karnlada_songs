import os
import re
m4a_dir = os.path.join('output')
mp3_dir = os.path.join('output','mp3')
m4as = [f for f in os.listdir(m4a_dir) if f.lower().endswith('.m4a')]
mp3s = [f for f in os.listdir(mp3_dir) if f.lower().endswith('.mp3')]

def canonical_stem(name):
    # strip extension
    stem = os.path.splitext(name)[0]
    # remove trailing -N numeric suffix (e.g., "song-2")
    stem = re.sub(r'-\d+$', '', stem)
    return stem

mp3_stems = set(canonical_stem(f) for f in mp3s)
missing = []
for f in m4as:
    stem = canonical_stem(f)
    if stem not in mp3_stems:
        missing.append(f)

print('Total m4a:', len(m4as))
print('Total mp3:', len(mp3s))
print('Missing mp3 for these m4a files:')
for f in missing:
    print(f)
