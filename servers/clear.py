from db.redis_store import *

if __name__ == '__main__':
    df = initialize_dataframe()
    store_dataframe(df)
