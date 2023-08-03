# Asset-management

## For single trade category:
1. Fixed Fractional method
2. Fixed Ratio method
3. Volatility Ratio method

### Fixed Fractional method
$$  Contract Number= int(\frac{Total Asset * f\%}{Stop Loss}) $$

### Fixed Ratio method
if 现有资金 < 初始资金: 

$$ 合约数 = 1 $$

if 现有资金 > 初始资金:

$$ 合约数 = int(\frac{1 + \sqrt{(1 + 8 * \frac{总资金 - 初始资金}{\Delta})}}{2}) $$

### Volatility Ratio method
$$ 合约数 = int(\frac{Vol\% * 资金}{ATR(period) * Vp}) $$
