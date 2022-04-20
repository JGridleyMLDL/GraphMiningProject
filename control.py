import pandas as pd
import utils
import make_query
import queries


def uniswap_swaps_df(start_block=1638334800, end_block=1648785600):
    n = start_block

    while int(n) < int(end_block):
        query = queries.uniswap_swaps(n)
        req = make_query.make_request(queries.UNISWAP_URL, query)

        if n == start_block:
            df = utils.convert_to_Dataframe_UNI(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe_UNI(req)],
                           ignore_index=True)

        n = df.loc[df.index[-1], "timestamp"]
        print("(UPDATE)\t Queried {0} transactions. Block Number: {1}".format(
            df.shape[0], n))

    return df


def compound_transfers_df(start_block=1638334800, end_block=1648785600):
    n = start_block

    while int(n) < int(end_block):
        query = queries.compoundTransfers(n)
        req = make_query.make_request(queries.COMPOUND_URL, query)

        if n == start_block:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)

        n = df.loc[df.index[-1], "blockTime"]
        print("(UPDATE)\t Queried {0} transactions. Block Number: {1}".format(
            df.shape[0], n))

    return df


def compound_users_df(num_users=5000):
    """RETIRED

    Args:
        num_users (int, optional): _description_. Defaults to 5000.

    Returns:
        _type_: _description_
    """
    n = 0

    while n*1000 < min(num_users, 5000):
        query = queries.compoundUsers(n)
        req = make_query.make_request(queries.COMPOUND_URL, query)

        if n == 0:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)

        print("(UPDATE)\t Queried {0} users.".format(
            df.shape[0]))
        n += 1
    return df


def decentraland_transactions_df(start_time=1577854800, end_time=1649217600):
    c = start_time

    while c <= end_time:
        query = queries.decentraland_sales(c)

        req = make_query.make_request(queries.DECENTRALAND_URL, query)

        if c == start_time:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)
        print("(UPDATE)\t Queried {0} transactions.".format(
            df.shape[0]))
        c = int(df["timestamp"].iloc[-1])

    return df


def aave_transactions_df(start_time=1638334800, end_time=1649217600):
    c = start_time

    while c <= end_time:
        query = queries.aave_all_transaction_types(c)

        req = make_query.make_request(queries.AAVE_URL, query)

        if c == start_time:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)
        print("(UPDATE)\t Queried {0} transactions.".format(
            df.shape[0]))
        c = int(df["timestamp"].iloc[-1])

    return df


def balancer_transactions_df(start_time=1638334800, end_time=1649217600):
    c = start_time

    while c <= end_time:
        query = queries.balancer_user_transactions(c)

        req = make_query.make_request(queries.BALANCER_URL, query)

        if c == start_time:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)
        print("(UPDATE)\t Queried {0} transactions.".format(
            df.shape[0]))
        c = int(df["timestamp"].iloc[-1])

    return df


def one_inch_txs_df(start_time=1638334800, end_time=1649217600):
    c = start_time

    while c <= end_time:
        query = queries.one_inch_transactions(c)

        req = make_query.make_request(queries.ONE_INCH_URL, query)

        if c == start_time:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)
        print("(UPDATE)\t Queried {0} transactions.".format(
            df.shape[0]))
        c = int(df["timestamp"].iloc[-1])

    return df


def axie_txs_df(start_time=1577854800, end_time=1649217600):
    c = start_time

    while c <= end_time:
        query = queries.axie_transactions(c)

        req = make_query.make_request(queries.AXIE_URL, query)

        if c == start_time:
            df = utils.convert_to_Dataframe(req)
        else:
            df = pd.concat([df, utils.convert_to_Dataframe(req)],
                           ignore_index=True)
        print("(UPDATE)\t Queried {0} transactions.".format(
            df.shape[0]))
        c = int(df["timestamp"].iloc[-1])

    return df


def get_and_save_data(folder, startTime, endTime):
    print("(START)\t Starting Uniswap Queries", end="\n")
    uni_df = uniswap_swaps_df(startTime, endTime)
    uni_df.to_csv(folder+"/uniswap_data.csv")
    print("(COMPLETE)\t Saved Uniswap Data")

    print("(START)\t Starting Compound Queries", end="\n")
    comp_df = compound_transfers_df(startTime, endTime)
    comp_df.to_csv(folder+"/compound_data.csv")
    print("(COMPLETE)\t Saved Compound Data", end="\n\n")

    print("(START)\t Starting Decentraland Queries", end="\n")
    dec_df = decentraland_transactions_df()
    dec_df.to_csv(folder+"/decentraland_data.csv")
    print("(COMPLETE)\t Saved Decentraland Data", end="\n\n")

    print("(START)\t Starting Aave Queries", end="\n")
    aave_df = aave_transactions_df(startTime, endTime)
    aave_df.to_csv(folder+"/aave_data.csv")
    print("(COMPLETE)\t Saved Aave Data", end="\n\n")

    print("(START)\t Starting Balancer Queries", end="\n")
    bal_df = balancer_transactions_df(startTime, endTime)
    bal_df.to_csv(folder+"/balancer_data.csv")
    print("(COMPLETE)\t Saved Balancer Data", end="\n\n")

    print("(START)\t Starting 1Inch Queries", end="\n")
    oi_df = one_inch_txs_df(startTime, endTime)
    oi_df.to_csv(folder+"/one_inch_data.csv")
    print("(COMPLETE)\t Saved 1Inch Data", end="\n\n")

    print("(START)\t Starting AXIE Queries", end="\n")
    ax_df = one_inch_txs_df()
    ax_df.to_csv(folder+"/axie_data.csv")
    print("(COMPLETE)\t Saved AXIE Data", end="\n\n")


if __name__ == "__main__":
    #d = compound_transfers_df(13950000, 14564487)
    # print(d.head)
    # d.to_csv("compound_txs.csv")

    #d = decentraland_transactions_df()
    # d.to_csv("decentraland_data/transactions_112020.csv")

    #print("(START)\t Starting AXIE Queries", end="\n")
    #ax_df = one_inch_txs_df()
    # ax_df.to_csv("user_prediction_data/axie_data.csv")
    #print("(COMPLETE)\t Saved AXIE Data", end="\n\n")

    get_and_save_data("user_prediction_data", 1625112000, 1648785600)
