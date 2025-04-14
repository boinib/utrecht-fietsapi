def filter_data(df, query, min_free):
    df_filtered = df[df["facilityName"].str.contains(query, case=False)]
    df_filtered = df_filtered[df_filtered["freePlaces"] >= min_free]
    return df_filtered
