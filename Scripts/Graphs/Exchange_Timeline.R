library(ggplot2)

raw1 <- read.csv("C:/Honors_Thesis/Monthly_Exchange_Statistics.csv")
row.names(raw1) <- raw1$Exchange

raw_dates <- raw1[c('Start.Date','End.Date')]

plot(raw_dates)