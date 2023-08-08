# Asset-management

## For single trade category:
### Basic Position Management Strategy
1. Fixed Fractional method
   
   $$  Contract Number= int(\frac{Total Asset * f\%}{Stop Loss}) $$

2. Fixed Ratio method
   
   If Current Asset < Original Asset:

$$ Contract Number = 1 $$

   If Current Asset > Original Asset:

$$ Contract Number = int(\frac{1 + \sqrt{(1 + 8 * \frac{Current Asset - Original Assset}{\Delta})}}{2}) $$
   
3. Volatility Ratio method
   
$$ Contract Number = int(\frac{Vol\% * 总资金}{ATR(period) * Vp}) $$


### More advanced techniques
1. Diminishing fractional method
2. 保守-激进资金组合
3. Equity curve trading

### Market Timing Strategy

1. Moving Average Crossovers strategy
   
### Monte-Carlo Simulations (rate of return & withdrawal distributions)


