# Lifetime-Mahjong-Performance
Most Fridays I play mahjong with my friends for penny a point stakes. As an excuse to practice some time series analysis and once and for all establish who is the best, here is out lifetime performance and payout data. The data is divided into Season 1 (when Noah lived in Maryland) and Season 2 (all games after Noah moved). 

For more in depth data check Processing.ipynb

### Most Recent Night: 02/06/2026 (9 Hands played)
| Player | Net Profit | Highest Hand | Hands Won | Δ Avg Points per hand |
| :--- | :--- | :--- | :--- | :--- |
| Connor | $\color{green}{+240}$ | 320 | 3 | $\color{green}{+2.29}$ |
| Helio | $\color{green}{+220}$ | 256 | 2 | $\color{red}{-0.69}$ |
| Oscar | $\color{red}{-160}$ | 64 | 3 | $\color{red}{-29.33}$ |
| Sam | $\color{red}{-300}$ | 32 | 1 | $\color{green}{+0.38}$ |

## Current Season Performance 
Big props to Helio for crushing it during the October games, and being our current leader.

Big props to Sam for continuing to play with us. 
![results graph](https://github.com/Conair94/Lifetime-Mahjong-Performance/blob/main/Season%202%20Data/net_profit.png)

Here we have a graph of only guests and their performance. 
![guest results graph](https://github.com/Conair94/Lifetime-Mahjong-Performance/blob/main/Season%202%20Data/net_profit_guests.png)

This histogram shows the distribution of winning hand sizes (Fan).
![fan distribution](https://github.com/Conair94/Lifetime-Mahjong-Performance/blob/main/Season%202%20Data/fan_distribution.png)

Histograms of winning hand sizes (Points) for self-drawn and non-self-drawn hands.
![self drawn points](https://github.com/Conair94/Lifetime-Mahjong-Performance/blob/main/Season%202%20Data/win_points_self_drawn.png)
![non self drawn points](https://github.com/Conair94/Lifetime-Mahjong-Performance/blob/main/Season%202%20Data/win_points_non_self_drawn.png)

## Season 2 Player Statistics
**Average Games per Night:** 6.33  
**Dealer Win Rate:** 17.50%  
**Self-Draw Win Rate:** 25.68%  

[View Raw Data (CSV)](Season%202%20Data/player_stats.csv)

| Player | Games Played | Win Rate | Avg Win Fan | Avg Win Points | Avg Loss Points | Net Profit | Expected Points Per Hand |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Connor | 74 | 28.38% | 7.5 | 141.7 | -42.0 | $\color{green}{748}$ | 10.11 |
| Helio | 74 | 28.38% | 9.4 | 199.6 | -38.0 | $\color{green}{2178}$ | 29.43 |
| Sam | 74 | 8.11% | 5.5 | 109.3 | -48.9 | $\color{red}{-2670}$ | -36.08 |
| Guest (aggregate) | 74 | 35.14% | 4.6 | 86.5 | -52.2 | $\color{red}{-256}$ | -3.46 |
| Ruohan | 23 | 34.78% | 4.5 | 72.0 | -59.7 | $\color{red}{-320}$ | -13.91 |
| Oscar | 12 | 41.67% | 3.6 | 54.4 | -52.6 | $\color{red}{-96}$ | -8.0 |
| Drew | 10 | 20.00% | 7.0 | 224.0 | -50.0 | $\color{green}{48}$ | 4.8 |
| Nick | 9 | 55.56% | 5.2 | 92.8 | -68.0 | $\color{green}{192}$ | 21.33 |
| Brandon | 8 | 12.50% | 4.0 | 64.0 | -30.9 | $\color{red}{-152}$ | -19.0 |
| Lixin | 6 | 50.00% | 4.3 | 74.7 | -37.3 | $\color{green}{112}$ | 18.67 |
| Alice | 6 | 33.33% | 4.5 | 100.0 | -60.0 | $\color{red}{-40}$ | -6.67 |

## Top 5 Largest Hands
| Date | Player | Fan | Points | Self Drawn |
| :--- | :--- | :--- | :--- | :--- |
| 10/3/2025 | Helio | 32 | 960 | Yes |
| 1/28/2026 | Helio | 23 | 256 | No |
| 12/12/2025 | Connor | 19 | 320 | No |
| 8/29/2025 | Connor | 18 | 320 | No |
| 2/6/2026 | Connor | 17 | 320 | No |

## Rules
We play MCR rules with a few house rules that add some scoring rules:
1. If you win a fully concealed vertically symmetric hand and simultaneously flip your entire stack of 14 tiles 180 degrees to face the table without dropping any tiles it becomes a limit hand.
2. If you win on replacement once its 8 Fan, twice is 24 Fan, thrice is Limit.
3. If you win on replacement or last tile AND the winning tile is a 1 dot or 5 dot, then this is a Limit hand. (plucking the moon from bottom of the ocean, plucking the plum from the rooftop)
4. You can win a 7 pairs with 2 identical pairs (aka 5 pairs and a concealed kong) but you may not call it as a concealed kong and it must always be a fully concealed hand (can never win 7 pairs if a set is called).
5. If you win a hand that is two limit hand worths, then its double limit (I.e. earthly all-green) 

## Current betting spreads 
Oscar beats Helio
5:2

Sam wins 
7:1

Helio wins
3:2

There is a blowout (only one person is positive) 
4:1

I recently came into possession of many Moroccan geodes and we are running a betting special, 

Win over 5$ and get a free geode. 

## Fan to Points

| Fan        | Points/Cents          | Nickname  |
| ------------- |:-------------:| -----:|
| 0 | 32 | Chicken Hand |
| 1 | 2  |  |
| 2 | 4  |  |
| 3 | 8  | Min-Hand |
| 4,5,6 | 16  |  |
| 7,8,9 | 32 |  |
| 10-15 | 64 |  |
| 16-23 | 80 |  |
| 24-43 | 160  |  |
| 44-63 | 240  |  |
| 64-87 | 360  |  |
| 88 | 500  | Limit Hand |


### Tile Nicknames
TBD
