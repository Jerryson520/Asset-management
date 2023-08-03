![image](https://github.com/Jerryson520/Asset-management/assets/67813088/d669f108-d43a-4cee-b163-c1502b0b8864)![image](https://github.com/Jerryson520/Asset-management/assets/67813088/0d218537-a861-42dd-b578-a1903cf6ca5c)# Asset-management

## For single trade category:
### Basic strategy
1. Fixed Fractional method
   $$  Contract Number= int(\frac{Total Asset * f\%}{Stop Loss}) $$

2. Fixed Ratio method
   if 现有资金 < 初始资金: 

   $$ 合约数 = 1 $$

   if 现有资金 > 初始资金:

   $$ 合约数 = int(\frac{1 + \sqrt{(1 + 8 * \frac{总资金 - 初始资金}{\Delta})}}{2}) $$
   
3. Volatility Ratio method
   $$ 合约数 = int(\frac{Vol\% * 总资金}{ATR(period) * Vp}) $$


### More advanced techniques
1. Diminishing fractional method
2. 保守-激进资金组合
3. Equity curve trading

### Monte-Carlo Simulations (rate of return & withdrawal distributions)


