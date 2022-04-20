
from os import times
from sqlite3 import Timestamp
from time import time


UNISWAP_URL = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2'

UNISWAP_FACTORY_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
UNISWAP_START = 1543640400


COMPOUND_URL = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
DECENTRALAND_URL = "https://api.thegraph.com/subgraphs/name/decentraland/marketplace"
AAVE_URL = "https://api.thegraph.com/subgraphs/name/aave/protocol-v2"
BALANCER_URL = "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer"
ONE_INCH_URL = "https://api.thegraph.com/subgraphs/name/nelsongaldeman/simplefi-1inch-mainnet"
AXIE_URL = "https://api.thegraph.com/subgraphs/name/upshot-tech/nft-analytics-axie-infinity"


def factory_data(block_num):
    queryStr = '''
    query uniswapFactories {
      uniswapFactories(block: { number: %s } 
       where: { id: "%s" }) {
        id
        totalVolumeUSD
        totalVolumeETH
        untrackedVolumeUSD
        totalLiquidityUSD
        totalLiquidityETH
        txCount
        pairCount
      }
    }
    ''' % (block_num, UNISWAP_FACTORY_ADDRESS)

    return queryStr


def day_data(skip_num):
    queryStr = '''
    query uniswapDayDatas {
        uniswapDayDatas(first: 100, skip: %s, where: { date_gt: 1543640400}, orderBy: date, orderDirection: asc) {
            id
            date
            dailyVolumeETH
            dailyVolumeUSD
            dailyVolumeUntracked
            totalVolumeUSD
            totalLiquidityUSD
            mostLiquidTokens{
                token{
                    name
                }
                dailyTxns
            }
            txCount
        }
    }
    ''' % (skip_num)

    return queryStr


def uniswap_swaps(timestamp):
    queryStr = """
    {
        swaps(first:1000, where: { timestamp_gte: %s}) {
            sender
            to
            timestamp
        }
    }""" % timestamp
    return queryStr


def compoundUsers(pg):
    skp = pg*100
    query_Str = '''
    {
        accounts(first: 1000, skip:%s) {
            id
            countLiquidated
            countLiquidator
            hasBorrowed
            health
            totalBorrowValueInEth
            totalCollateralValueInEth
            tokens{
            symbol
            }
        }
    }''' % skp

    return query_Str


def compoundUser_byID(id):
    query_Str = '''
    {
        account(id: "%s") {
                countLiquidated
            countLiquidator
            hasBorrowed
            totalBorrowValueInEth
            totalCollateralValueInEth
            tokens{
            symbol
            }
        }
    }''' % id

    return query_Str


def compoundTransfers(timestamp):
    query_str = '''
    {
        transferEvents(first: 1000, where: { blockTime_gte: %s }, orderBy: blockNumber, orderDirection: asc ) {
            amount
            to
            from
            blockTime
            cTokenSymbol
        }
    }''' % (timestamp)

    return query_str


def decentraland_sales(timestamp):
    query_str = '''
    {
        sales(first: 1000, where: { timestamp_gte: %s }, orderBy: timestamp, orderDirection: asc ) {
            buyer
            seller
            price
            timestamp
        }
    }''' % timestamp
    return query_str


def aave_all_transaction_types(timestamp):
    query_str = """
    {
        userTransactions(first: 1000, where: { timestamp_gte: %s}){
            user{
            id
            }
            pool{
            id
            }
            timestamp
        }
    }""" % timestamp

    return query_str


def aave_borrow_transactions(timestamp):
    query_str = """
    {
        borrows(first: 1000, where: { timestamp_gte: %s}){
            user{
                id
            }
            caller{
                id
            }
            timestamp
        }
    }""" % timestamp
    return query_str


def balancer_user_transactions(timestamp):
    query_str = """
    {
        transactions(first: 1000, where: { timestamp_gte: %s}) {
            poolAddress{
                id
            }
            userAddress{
                id
            }
            timestamp
        }
    }""" % timestamp
    return query_str


def one_inch_transactions(timestamp):
    query_str = """
    {
        transactions(first: 1000, where: { timestamp_gte: %s}){
            from{
                id
            }
            to{
                id
            }
            timestamp
        }
    }""" % timestamp
    return query_str


def axie_transactions(timestamp):
    query_Str = """
    {
    transferEvents(first: 1000, where:{ timestamp_gte: %s}) {
        from{
            id
        }
        to{
            id
        }
        timestamp 
    }
    }""" % timestamp
