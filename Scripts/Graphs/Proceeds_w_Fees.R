library(ggplot2)
library(extrafont)
library(scales)
loadfonts()
case1_stats <- read.csv("C:/Honors_Thesis/Case1_Monthly_Trade_Stats.csv")
case2_stats <- read.csv("C:/Honors_Thesis/Case2_Monthly_Trade_Stats.csv")

case1_stats$Date <- as.Date(case1_stats$Date)
case2_stats$Date <- as.Date(case2_stats$Date)
case1_stats$DollarVolumeBoughtTC <- case1_stats$DollarVolumeBought*1.0025
case1_stats$DollarVolumeSoldTC <- case1_stats$DollarVolumeSold*.9975
case1_stats$WeightedAverageSpreadTC <- (1-(case1_stats$DollarVolumeBoughtTC/case1_stats$DollarVolumeSoldTC))#/(case1_stats$DollarVolumeBought)
case2_stats$DollarVolumeBoughtTC <- case2_stats$DollarVolumeBought*1.0025
case2_stats$DollarVolumeSoldTC <- case2_stats$DollarVolumeSold*.9975
case2_stats$WeightedAverageSpreadTC <- (1-(case2_stats$DollarVolumeBoughtTC/case2_stats$DollarVolumeSoldTC))#/(case1_stats$DollarVolumeBought)
case2_stats$Proceeds <- case2_stats$Proceeds/1000
case1_stats$Proceeds <- case1_stats$Proceeds/1000
case1_stats$FeeProceeds <- (case1_stats$DollarVolumeSoldTC-case1_stats$DollarVolumeBoughtTC)/1000
case2_stats$FeeProceeds <- (case2_stats$DollarVolumeSoldTC-case2_stats$DollarVolumeBoughtTC)/1000

spreads <- ggplot()+
  geom_line(aes(case1_stats$Date,case1_stats$FeeProceeds,color='Case 1'),color='red') +
  geom_line(aes(case2_stats$Date,case2_stats$FeeProceeds,color='Case 2'),color='blue') +
  geom_line(aes(case1_stats$Date,case1_stats$Proceeds),color='darkred') +
  geom_line(aes(case2_stats$Date,case2_stats$Proceeds),color='darkblue') +
  geom_hline(yintercept = c(0))+
  geom_vline(xintercept = as.numeric(as.Date('2010-07-01')))+
  scale_x_date(limits = as.Date(c('2010-07-01','2017-03-02')),expand=c(0,0))+
  scale_y_continuous(limits = c(0,1000),expand = c(0,0),labels=dollar)+
  labs(x="Year",y="Dollars Arbitraged (MM)")+
  theme(panel.background = element_rect(fill = "white",
                                        colour = "white",
                                        size = 0.5, linetype = "solid"),
        panel.grid.major.y = element_line(size = 0.5, linetype = 'solid',
                                          colour = "grey")) +
  scale_fill_manual()+
  ggtitle("Monthly Proceeds") +
  theme(axis.text = element_text(family="CM Roman", size = 14))+
  theme(plot.title = element_text(family = "CM Roman", color="black", size=22, hjust=.5)) +
  theme(axis.title = element_text(family = "CM Roman", color="black", face="bold", size=18))

ggsave("Monthly_ProceedsTC.pdf", spreads, width=10, height=6)
