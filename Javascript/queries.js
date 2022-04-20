import gql from 'graphql-tag';


const FACTORY_ADDRESS = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'


export const GLOBAL_DATA = (block) => {
  const queryString = ` query uniswapFactories {
      uniswapFactories(
       ${block ? `block_gt: { number: ${block}}` : ``} 
       where: { id: "${FACTORY_ADDRESS}" }) {
        id
        totalVolumeUSD
        totalVolumeETH
        untrackedVolumeUSD
        totalLiquidityUSD
        totalLiquidityETH
        txCount
        pairCount
      }
    }`
  return queryString
  // return gql(queryString)
}


export const FACTORIES = (block) => {
  const queryString = ` {
 uniswapFactory(id: "${FACTORY_ADDRESS}", block: {number: "${block}"}){
  id
  pairCount
  totalVolumeUSD
  untrackedVolumeUSD
  totalLiquidityUSD
  txCount
  mostLiquidTokens{
  id
  date
  token{
      id
      symbol
      name
  }
  dailyVolumeUSD
  dailyTxns
  totalLiquidityUSD
  priceUSD
  }
 }
}`
  return queryString
  // return gql(queryString)
}

export const TOKEN_DAY = (date) => {
  const queryString = ` 
  {
    pairDayDatas(first: 100,
    where: {
        pairAddress: "0xa478c2975ab1ea89e8196811f51a7b7ade33eb11",
        date_gt: ${date}
    }
    ) {
        date
        dailyVolumeToken0
        dailyVolumeToken1
        dailyVolumeUSD
        reserveUSD
        token0{
            symbol
        }
        token1{
            symbol
        }
    }
    }`


  return queryString
  // return gql(queryString)
}

