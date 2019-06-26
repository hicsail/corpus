from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sys

if __name__ == '__main__':

    df = pd.read_csv(sys.argv[1], index_col="author_keywords")
    authors = list(df.index.values)
    sim_matrix = cosine_similarity(df, df)
    sim_author_df = pd.DataFrame(data=sim_matrix, index=authors, columns=authors)
    sim_author_df.to_csv(sys.argv[2])

