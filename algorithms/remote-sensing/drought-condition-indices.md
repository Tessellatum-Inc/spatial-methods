# Drought condition indices

VCI = 100 (NDVI - NDVI_min)/(NDVI_max - NDVI_min); TCI = 100 (LST_max - LST)/(LST_max - LST_min). VHI = alpha*VCI + (1-alpha)*TCI, with alpha in [0,1]. Constant denominators are undefined and return missing values.

For SPI, the implementation fits a gamma distribution G to positive precipitation and combines it with observed zero fraction q: H(x)=q+(1-q)G(x). SPI=Phi^-1(H(x)), where Phi is the standard normal CDF. Fit is performed independently along a selected time axis. This is not calendar-month-specific SPI; seasonal rainfall requires seasonal/monthly calibration. Missing observations remain missing and insufficient samples yield missing output.

These indicators require consistent sensors, an explicitly chosen reference period and local validation. They do not independently establish drought impacts, crop losses or an insurance payout trigger.
