import pickle
import bz2file as bz2


similarity = pickle.load(open('similarity.pkl', 'rb'))

with bz2.BZ2File('similarity.pbz2', 'w') as f:
    pickle.dump(similarity, f)

print("Compressed similarity matrix saved as similarity.pbz2")
